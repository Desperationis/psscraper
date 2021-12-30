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


from psscraper import *
import time

print("""------------------------------------------------------------------------------
psscraper  Copyright (C) 2021  Diego Contreras

This program comes with ABSOLUTELY NO WARRANTY. This is free software, and you
are welcome to redistribute it under certain conditions; See LICENSE file.
------------------------------------------------------------------------------
""")


# Log in
print("Opening browser...")
browser = PowerschoolBrowser(link="yourpowerschoollink", headless=True)
print("Logging in...")
with open("credentials", "r") as credentialFile:
    lines = credentialFile.readlines()
    for line in lines:
        line = line.strip()

    browser.login(lines[0], lines[1])

# Choose a class to predict
classInfoScrapper = PowerschoolClassInfoScrapper(browser.getPageSource())
classIDs = classInfoScrapper.getCourseIDs()

print("\n\nChoose a class to predict a grade for:")

for index, classID in enumerate(classIDs):
    className = " ".join(classInfoScrapper.getCourseInfo(classID))
    print("[{0}] {1}".format(index, className))

classID = classIDs[int(input("Class num: "))]
className = " ".join(classInfoScrapper.getCourseInfo(classID))
link = classInfoScrapper.getCourseDir(classID)
browser.searchDir(link)

time.sleep(4) # Wait for assignments to load

# Sort assignments into categories
assignmentScraper = PowerschoolAssignmentScrapper(browser.getPageSource())
assignmentIDs = assignmentScraper.getAssignmentIDs()
assignmentGrades = {} # Category : [(grades)]

for assignmentID in assignmentIDs:
    category = assignmentScraper.getAssignmentCategory(assignmentID)
    grade = assignmentScraper.getAssignmentGrade(assignmentID)

    if category not in assignmentGrades:
        assignmentGrades[category] = []

    assignmentGrades[category].append(grade)

# Predict grade using weighing.
predictedGrade = 0
categoryWeighing = {}
indexToCategory = {}

print("\nThere are {0} categories total:".format(len(assignmentGrades)))
for index, key in enumerate(assignmentGrades):
    print("[{0}] {1}".format(index, key))
    indexToCategory[index] = key

print("")


for key in assignmentGrades:
    weighing = float(input("Enter the percent weight for \"{0}\": ".format(key)))
    categoryWeighing[key] = weighing

print("")

numAssignments = int(input("Enter the number of assignments you wish to predict: "))
for i in range(numAssignments):
    print("")
    earnedNum = input("Enter your predicted number of points on assignment {0}: ".format(i + 1))
    totalNum = input("Enter the total amount of points on assignment {0}: ".format(i + 1))
    category = indexToCategory[int(input("Enter the category of assignment {0} (use numbers above): ".format(i + 1)))]

    assignmentGrades[category].append((earnedNum, totalNum))



for key in assignmentGrades:
    totalNum = 0
    earnedNum = 0

    for grade in assignmentGrades[key]:
        if str.isdecimal(grade[0]):
            totalNum += float(grade[1])
            earnedNum += float(grade[0])

    if totalNum > 0:
        predictedGrade += (earnedNum / totalNum) * categoryWeighing[key]

predictedGrade = round(predictedGrade, 1)
print("\nYour predicted grade for {0} is {1}%".format(className, predictedGrade)) 



























browser.close()




