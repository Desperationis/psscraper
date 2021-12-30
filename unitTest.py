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


from PowerschoolBrowser import *
from Scrapper.PowerschoolClassInfoScrapper import *
from Scrapper.PowerschoolAssignmentScrapper import *
import os
import time

def formatPrint(msg):
    print(os.path.basename(__file__) + ": " + msg)

browser = PowerschoolBrowser(debug=False)

success = browser.login("username", "pass") # Better be careful here!
print("Success: {0}".format(success))

browser.searchDir(browser.homeDir)
classInfoScrapper = PowerschoolClassInfoScrapper(browser.getPageSource(), debug=False)

for courseID in classInfoScrapper.getCourseIDs():
    print(classInfoScrapper.getCourseInfo(courseID))

    courseLink = classInfoScrapper.getCourseDir(courseID)
    browser.searchDir(courseLink)

    time.sleep(3)

    assignmentScrapper = PowerschoolAssignmentScrapper(browser.getPageSource(), debug=True)
    for id in assignmentScrapper.getAssignmentIDs():
        print(assignmentScrapper.getAssignmentGrade(id))
        print(assignmentScrapper.getAssignmentDueDate(id))
        print(assignmentScrapper.getAssignmentCategory(id))
        print(assignmentScrapper.getAssignmentName(id))
    


browser.close()
