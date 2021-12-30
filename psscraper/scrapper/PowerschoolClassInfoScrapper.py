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


from psscraper.scrapper.PowerschoolScrapper import *

class PowerschoolClassInfoScrapper(PowerschoolScrapper):
    """Scrapes classroom information from the guardian/index.html.

    Attributes:
        None
    """

    def _getFileName(self):
        return __file__

    def getName(self) -> str:
        """Return name of student.

        Returns:
            The name of the student as a string. If it is not found, return
            None.
        """

        self._print("Finding student name...")

        nameElement = self.soup.find(id='firstlast')
        if nameElement != None:
            self._print("Student name found!")
            return nameElement.get_text().strip()

        self._print("Student name not found.")
        return None 


    def getCourseIDs(self) -> [str]:
        """Return list of classroom IDs.

        Returns:
            A list of strings that represent each individual classroom in the
            form of an ID. If no classrooms are found, return an empty list.
            E.x. ["ccid_3861348", ...].  These IDs can be used with other
            functions to get more information about a course. If no courses are
            found, return an empty list.
        """

        self._print("Looking for course elements...")
        self._print("Searching for course table...")
        courseTable = self.soup.find(class_='linkDescList')

        courseIDs = []

        if courseTable != None:
            self._print("Searching for individual course elements...")
            courses = courseTable.find_all('tr')
            self._print("Found {0} courses.".format(len(courses)))

            for element in courses:
                if 'id' in element.attrs:
                    self._print("Found course {0}".format(element['id']))
                    courseIDs.append(element['id'])
        else:
            self._print("Could not find course table.")

        return courseIDs

    def getCourseElement(self, classID : str) -> bs4.element:
        """Return course element give its ID.

        Args:
            classID:
                ID of the course as a string e.x. "ccid_3861348".

        Returns:
            bs4.element of the element that has classId as its html "id". This
            element is the parent to a container that contains all necessary
            information about a course. If the element is not found, return
            None.
        """

        self._print("Getting the course element for {0}.".format(classID))
        courseElement = self.soup.find(id=classID)
        if courseElement != None:
            self._print("Found course element for {0}".format(classID))
            return courseElement

        self._print("Could not find course element for {0}".format(classID))
        return None

    def getCourseInfo(self, classID) -> (str,str):
        """Return period and name info of a course given its ID

        Args:
            classID:
                ID of the course as a string e.x. "ccid_3861348".

        Returns:
            A tuple that represents a course's period and name:
            [0]: Period of the course
            [1]: Name of the course

            If the information is not found, return an empty tuple.
        """

        self._print("Getting course info of {0}".format(classID))

        courseElement = self.getCourseElement(classID)

        if courseElement != None:
            self._print("Searching for child elements in {0}...".format(classID))
            childElements = courseElement.find_all('td') 
            if len(childElements) >= 2:
                period = childElements[0].get_text().strip()
                name = childElements[1].get_text().split(u'\xa0')[0] # Line above <br>
                courseTuple = (period, name)
                self._print("Found {0} with info; Period: {1} Name: {2}".format(classID, period, name))

                return courseTuple

            else:
                self._print("Could not find any information from {0}".format(classID))

        return ()


    def getCourseDir(self, classID : str) -> str:
        """Gets the subdirectory to a course's grades given its ID.

        Args:
            classID:
                ID of the course as a string e.x. "ccid_3861348".

        Returns:
            Subdirectory to view the course's grades. This subdirectory can be
            used by PowerschoolBrowser to view the grades of a course with
            PowerschoolAssignmentScrapper. If it fails, returns None.
        """

        self._print("Getting course link of {0}.".format(classID))

        courseElement = self.getCourseElement(classID)

        if courseElement != None:
            linkElement = courseElement.find('a', class_='bold')
            link = "guardian/" + linkElement['href']
            self._print("Found course link: {0}".format(link))
            return link

        return None
