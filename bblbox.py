#    This file is part of gnome-bubbles.
#
#    gnome-bubbles is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    gnome-bubbles is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with gnome-bubbles.  If not, see <http://www.gnu.org/licenses/>.

import string
import re

class Bblbox:
    def __init__(self, bblbox_to_load):
        self.bblx_file = bblbox_to_load
        self.url = ''
        self.name = ''
        self.description = ''
        self.raw_data = ''
        self.is_parsed = False

    def parse(self):
        with open(self.bblx_file, 'r') as f:
            read_data = f.read()
        f.closed

        for line in read_data.split('\n'):
            m = re.match(r'//\s*@(desc|name|url)\s*(['+string.printable+']+)', line)
            if m :
                if m.group(1) == 'desc':
                    self.description = string.strip(m.group(2))
                elif m.group(1) == 'name':
                    self.name = string.strip(m.group(2))
                elif m.group(1) == 'url':
                    self.url = string.strip(m.group(2))

        self.raw_data = read_data
        self.is_parsed = True

    def get_url(self):
        return self.url

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_data(self):
        return self.raw_data

