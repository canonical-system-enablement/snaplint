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

NAUGHTY_FILES=[
    '.o',       # object files
    '.a',       # static libs
    '.h',       # header files
    '.hpp',
]

NAUGHTY_DIRS=[
    '.git',
    '.bzr',
]

class DeveloperCruft(Rule):

    def __init__(self, path):
        super().__init__(path)

    def scan(self):
        print('Scanning {} for developer cruft...'.format(self.path), end=' ')

        fail_list=[]
        for f in Rule.get_file_list(self.path):
            for suffix in NAUGHTY_FILES:
                if f.endswith(suffix):
                    fail_list.append(f)

        for d in Rule.get_dir_list(self.path):
            for suffix in NAUGHTY_DIRS:
                if d.endswith(suffix):
                    fail_list.append(d)

        if fail_list:
            print('FAIL!')
            print('Development files found:')
            for f in fail_list:
                print(f)
            return False

        print('OK!')
        return True
