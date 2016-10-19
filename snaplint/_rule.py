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

import os

class Rule:

    def __init__(self, path):
        self.path = path

    @classmethod
    def get_file_list(cls, path):
        '''Return a list of files in the snap'''
        file_list = []
        for root, dirs, files in os.walk(path):
            for f in files:
                file_list.append(os.path.relpath(os.path.join(root, f),
                                                 path))

        return file_list

    @classmethod
    def get_dir_list(cls, path):
        '''Return a list of directories in the snap'''
        dir_list = []
        for root, dirs, files in os.walk(path):
            for d in dirs:
                dir_list.append(os.path.relpath(os.path.join(root, d),
                                                path))
        return dir_list


    def scan(self):
        '''Override this method to implement your rule checking logic'''
        pass
