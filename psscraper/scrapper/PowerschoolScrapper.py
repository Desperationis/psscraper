# psscraper - A web scrapper library for powerschool websites.
# Copyright (C) 2021 Diego Contreras
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import bs4
import os

class PowerschoolScrapper:
    """Base class for powerschool scrappers. 

    Base class for all powerschool scrappers. This gives toggleable debug
    statements and automates HTML parsing.

    Attributes:
        None
    """

    def __init__(self, pageSource : str, debug : bool = False):
        """Creates an instance of PowerschoolScrapper.

        Args:
            pageSource:
                Raw HTML data of the page in string form.
            debug: 
                Whether or not debug statements will be printed out.
        """

        self.soup = bs4.BeautifulSoup(pageSource, 'html.parser')
        self.debug = debug

    def _print(self, msg : str):
        """Print if self.debug is True. Outputs in the following format:
        currentFile: msg

        Args:
            msg:
                String that is printed if self.debug is True.
        """

        if self.debug:
            print(os.path.basename(self._getFileName()) + ": " + msg)

    def _getFileName(self):
        """Virtual function that returns subclasses' file name for debug purposes.

        Returns:
            The file name of the subclass as a string.
        """

        return __file__














