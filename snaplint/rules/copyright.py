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

import glob
import os
import yaml

from snaplint._rule import Rule


class CopyrightRule(Rule):

    '''Scan for copyright files in usr/share/doc within the snap. System
    Enablement Team policy requires that these files be present'''

    def __init__(self, path):
        super().__init__(path)

    def _read_snapcraft_yaml(self):
        snapcraft = None

        snapcraft_path = os.path.join(self.path, '..', 'snapcraft.yaml')
        if os.path.exists(snapcraft_path):
            with open(os.path.join(self.path, '..', 'snapcraft.yaml')) as sc:
                snapcraft = yaml.load(sc)

        return snapcraft

    def _check_copyrights(self):
        missing_sps = []
        missing_parts = []
        snapcraft = self._read_snapcraft_yaml()

        copyright_path = self.path + 'usr/share/doc/{}/*copyright*'

        for part in snapcraft['parts']:
            if not glob.glob(copyright_path.format(part)):
                missing_parts.append(part)
            if 'stage-packages' in snapcraft['parts'][part]:
                for pkg in snapcraft['parts'][part]['stage-packages']:
                    if not glob.glob(copyright_path.format(pkg)):
                        missing_sps.append(pkg)
        return (missing_sps, missing_parts)

    def scan(self):
        '''Go through the parts and staged packages and make sure there is an
           entry in usr/share/doc/*copyright* for each one'''

        print('Scanning {} for copyright compliance...'.format(self.path),
              end=' ')

        missing_sps, missing_parts = self._check_copyrights()
        if missing_sps or missing_parts:
            print('FAIL')
            if missing_parts:
                print('Missing copyright data for the following parts:')
                for part in missing_parts:
                    print(part)
            if missing_sps:
                print(
                  'Missing copyright data for the following staged packages:')
                for pkg in missing_sps:
                    print(pkg)
            return False
        else:
            print('OK')
            return True
