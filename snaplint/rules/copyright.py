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

from snaplint._rule import Rule

class CopyrightRule(Rule):
    '''Scan for copyright files in usr/share/doc within the snap. System
    Enablement Team policy requires that these files be present'''

    def __init__(self, path):
        super().__init__(path)

    def scan(self):
        '''Really dumb check that looks for at least one instance of 
        usr/share/doc/*/*copyright*
        '''
        print('Scanning {} for copyright compliance...'.format(self.path),
              end=' ')
        
        pattern = self.path + 'usr/share/doc/*/*copyright*'
        if not glob.glob(pattern, recursive=True):
            print('FAIL!')
            print('No copyright data found')
            return False

        print('OK!')
        return True

