#!/usr/bin/env python3
#
# Copyright (C) 2016 Canonical, Ltd.
# Author: Scott Sweeny <scott.sweeny@canonical.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from snaplint._rule import Rule

import os

from elftools.common.exceptions import ELFError
from elftools.elf.elffile import ELFFile

# Make things work easier on python3
from elftools.common.py3compat import (
        ifilter, byte2int, bytes2str, itervalues, str2bytes)

def _traverse_deps(root, elves):
    for lib in elves[root]['needed']:
        if lib in elves:
            elves[lib]['used'] = True
            _traverse_deps(lib, elves)
        else:
            continue

class LibraryRule(Rule):
    '''Examine the executables in the snap and make sure that only needed
    libraries are included'''

    def _get_elves(self):
        elves = {}
        roots = {}
        for filename in self.get_file_list():
            try:
                with open(os.path.join(self.path, filename), "rb") as fp:
                    try:
                        elf = ELFFile(fp)
                    except ELFError as e:
                        # Probably not an ELF file
                        continue
                    dynamic = elf.get_section_by_name(b'.dynamic')
                    if dynamic is None:
                        continue
                    needed = frozenset(tag.needed for tag in dynamic.iter_tags('DT_NEEDED'))
                    for tag in dynamic.iter_tags('DT_SONAME'):
                        soname = tag.soname
                        elves[soname] = {'filename': filename, 'needed': needed, 'used': False}
                        break
                    else:
                        roots[filename] = needed
            except Exception as error:
                # If we can't open the file just skip to the next one
                continue

        return (elves, roots)

    def __init__(self, path):
        super().__init__(path)

    def scan(self):
        '''Run ldd on any binary executables in the snap and check that
        only necessary shared libraries are included
        '''
        print('Scanning {} for unused shared libraries...'.format(self.path),
              end=' ')

        elves, roots = self._get_elves()

        for root in roots:
            for lib in roots[root]:
                if lib in elves:
                    elves[lib]['used'] = True
                    _traverse_deps(lib, elves)
                else:
                    continue

        # Popluate a list of unused libs
        unused = []
        for elf in elves:
            if elves[elf]['used'] is False:
                unused.append(elves[elf]['filename'])

        if unused:
            print('FAIL')
            print('Unused libraries found:')
            for lib in unused:
                print(lib)
            return False
        else:
            print('OK')
            return True
