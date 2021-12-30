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

class PowerschoolAssignmentScrapper(PowerschoolScrapper):
    """Scrapes assignment information from a class from guardian/index.html.

    Attributes:
        None
    """
    
    def _getFileName(self):
        return __file__

    def getAssignmentElement(self, assignmentID : str) -> bs4.element:
        """Return assignment element given its ID.

        Args:
            assignmentID:
                ID of the assignment as a string e.x.
                "assignmentsection_1351289".

        Returns:
            bs4.element of the element that has assignmentID as its html "id".
            This element is the parent to a container that contains all
            necessary information about an assignment. If the element is not
            found, return None.
        """

        assignmentElement = self.soup.find(id=assignmentID)
        if assignmentElement == None:
            self._print("Could not find element for {0}".format(assignmentID))
            return None

        return assignmentElement


    def getAssignmentIDs(self) -> [str]:
        """Return list of IDs for a class' assignments.

        Returns a list of strings that represent each individual assignment in
        the form of an ID. This ID can be used with other functions in this
        class for more information.

        Returns:
            List of strings that represent an assignment e.x.
            "[assignmentsection_1351289, ...]". If no assignment are found,
            return None.
        """
        
        self._print("Looking for assignment elements...")
        self._print("Searching for assignment table...")

        assignmentIDs = []
        assignmentTable = self.soup.find(id="scoreTable")
            

        if assignmentTable != None:
            self._print("Found assignment table.")
            parentElement = assignmentTable.find('tbody', recursive=False)

            if parentElement != None:
                self._print("Found parent element for assignments.")

                for row in parentElement.find_all(class_="ng-scope", recursive=False):
                    assignmentIDs.append(row['id'])
                    self._print("Found assignment {0}".format(row['id']))
            else:
                self._print("Could not find parent element for assignments.")
        else:
            self._print("Could not find assignment table.")

        return assignmentIDs

    def getAssignmentGrade(self, assignmentID : str) -> (str, str, str, str):
        """Return grade info of an assignment given its ID

        Args:
            assignmentID:
                ID of the assignment as a string e.x.
                "assignmentsection_1351289".

        Returns:
            A tuple of 4 string elements. Each index represents the following:
            [0]: Points given on assignment
            [1]: Total point possible on assignment
            [2]: Percent awarded for the assignment.
            [3]: Letter grade awarded for the assignment.

            If the assignment was not found, an empty tuple is returned. If
            certain elements are simply not found, each element not found is
            set to None.
        """

        self._print("Finding assignment grades...")
        pointsPossible = None
        pointsTotal = None
        percent = None
        letterGrade = None

        self._print("Finding grade for {0}".format(assignmentID))
        assignmentElement = self.getAssignmentElement(assignmentID)
        if assignmentElement == None:
            return ()
        

        scoreElement = assignmentElement.find(class_="score")
        if scoreElement != None:
            self._print("Found element for scores.")
            rawString = scoreElement.find().get_text().strip()
            pointsPossible = rawString.split("/")[0]
            pointsTotal = rawString.split("/")[1]
        else:
            self._print("Could not find element for scores.")



        ngElements = assignmentElement.find_all(class_="ng-binding ng-scope")
        for ngElement in ngElements:
            if "showPercent" in ngElement['data-ng-if']:
                percent = ngElement.get_text().strip()
            
            elif "showLetterGrade" in ngElement['data-ng-if']:
                letterGrade = ngElement.get_text().strip()

        
        result = (pointsPossible, pointsTotal, percent, letterGrade)
        self._print("Found grades for {0}: {1}".format(assignmentID, result))
        return result


    def getAssignmentDueDate(self, assignmentID : str) -> str:
        """Give assignment due date given its ID.

        Args:
            assignmentID:
                ID of the assignment as a string e.x.
                "assignmentsection_1351289".

        Returns:
            String representing assignment due date. If the assignment is not
            found, return None.
        """

        self._print("Finding assignment due date for {0}".format(assignmentID))
        assignmentElement = self.getAssignmentElement(assignmentID)
        if assignmentElement == None:
            return None

        ngElements = assignmentElement.find_all(class_='ng-binding')
        for ngElement in ngElements:
            attrLen = len(ngElement.attrs)
            if attrLen == 1:
                dueDate = ngElement.get_text().strip()
                self._print("Found due date for {0}: {1}".format(assignmentID, dueDate))
                return dueDate

        self._print("Could not find due date element.")
        return None

    def getAssignmentCategory(self, assignmentID : str):
        """Returns the category an assignment is graded in.

        Args:
            assignmentID:
                ID of the assignment as a string e.x.
                "assignmentsection_1351289".

        Returns:
            The category the assignment is graded in. If the assignment is not
            found, return None.
        """

        self._print("Finding assignment category for {0}".format(assignmentID))
        assignmentElement = self.getAssignmentElement(assignmentID)
        if assignmentElement == None:
            return None

        categoryElement = assignmentElement.find(class_="psonly")
        if categoryElement != None:
            category = categoryElement.get_text().strip()
            self._print("Found element for assignment category. Category is {0}".format(category))
            return category

        self._print("Could not find element for assignment category.")
        return None


    def getAssignmentName(self, assignmentID : str):
        """Return name of an assignment given its ID.

        Args:
            assignmentID:
                ID of the assignment as a string e.x.
                "assignmentsection_1351289".

        Returns:
            Name of the assignment. If the assignment is not found, return
            None.
        """

        self._print("Finding name of {0}".format(assignmentID))
        assignmentElement = self.getAssignmentElement(assignmentID)
        if assignmentElement == None:
            return None

        nameElement = assignmentElement.find(class_="assignmentcol")
        if nameElement != None:
            name = nameElement.find().get_text().strip()
            self._print("Found element for assignment name. Name is: {0}".format(name))
            return name

        self._print("Could not find element for assignment name.")
        return None

