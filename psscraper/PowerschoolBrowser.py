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

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.firefox.webelement import FirefoxWebElement
import os

class PowerschoolBrowser():
    """Selenium wrapper for logging into and viewing powerschool websites.

    This wrapper acts as a "browser" in that it wraps around a Firefox
    webdriver. The main purpose for this "browser" is to get raw HTML data that
    can be processed separately for scraping.

    Attributes:
        website: string of the powerschool website this class was instantiated
        with.
        loginDir: string of the directory that points to the login page.
        homeDir: string of the directory that points to the home page (page
        that lists classes and grades).
    """

    def __init__(self, link, debug : bool = False, headless : bool = False):
        """Creates a PowerschoolBrowser instance that uses a powerschool
        website.

        Args:
            link:
                Full link to a powerschool website without a subdomain e.x.
                "https://powerschool.k12.us/". Optionally, "file://" may be
                used with a local mirror of the website. In either case, a
                forward slash must always be at the end of the link.
            debug:
                Optional; Boolean specifying whether or not debug information
                is printed.
            headless:
                Optional; Booleans specifying whetehr or not the firefox
                browser will be run headless.
        """

        options = webdriver.FirefoxOptions()


        if headless:
            options.set_headless()
            
        self.browser = webdriver.Firefox(firefox_options=options)
        self.browser.implicitly_wait(5)
        
        self.website = link
        if self.website[-1] != '/':
            self.website += '/'

        self.loginDir = "public/home.html"
        self.homeDir = "guardian/home.html"
        self.debug = debug

    def _print(self, msg : str):
        """Print if self.debug is True. Outputs in the following format:
        currentFile: msg

        Args:
            msg:
                String that is printed if self.debug is True.
        """

        if self.debug:
            print("{0}: {1}".format(os.path.basename(__file__), msg))

    def searchDir(self, directory : str):
        """Navigate to a subdirectory or file in the current powerschool
        website.

        Args:
            directory:
                String to a subdirectory or file e.x. "public/home.html". This
                string should not start with a forward slash nor have any
                backslashes.
        """

        website = self.website + directory
        self._print("Going to {0}".format(website))
        self.browser.get(website)

    def loggedIn(self) -> bool:
        """Whether or not the browser is currently logged in.

        Determines if the browser is logged in by searching for a tell-tale
        element that is found within all pages of the powerschool website.

        Returns: A boolean specifying whether or not the browser is currently
        logged in.
        """

        self._print("Checking if logged in...")
        try:
            # This element only exists in logged in pages.
            self.browser.find_element_by_id('parentPageTemp')
            self._print("Logged In!")
            return True
        except NoSuchElementException:
            self._print("Not logged in.")
            return False

    def getPageSource(self) -> str:
        """Return the source of the currently loaded page.

        Returns:
            If logged in, return a string that contains the RAW html data of
            this page. If not logged in, return None.
        """

        if self.loggedIn():
            return self.browser.page_source

        return None

    def login(self, username : str, password : str) -> bool:
        """Logs on to powerschool.

        Given a username and password, log into powerschool via the login page.
        This might take awhile depending on the internet speed.

        Args:
            username:
                Username of the student. This is space and case sensitive,
                meaning incorrectly inserting a space before or after the
                username or incorrectly copying the case will result in the
                browser not being able to login.
            password:
                Password for the account. This is space and case sensitive,
                meaning incorrectly inserting a space before or after the
                username or incorrectly copying the case will result in the
                browser not being able to login.

        Returns:
            True if the login succeeded, False otherwise.
        """

        self.searchDir(self.loginDir)
        self._print("Logging in as USER:{0} with PASS:{1}".format(username, password))
       
        self._print("Entering account info...")
        accountField = self.browser.find_element_by_id('fieldAccount')
        accountField.send_keys(username)

        self._print("Entering password...")
        passwordField = self.browser.find_element_by_id('fieldPassword')
        passwordField.send_keys(password)

        self._print("Clicking submit...")
        submitButton = self.browser.find_element_by_id('btn-enter-sign-in')
        submitButton.click()

        return self.loggedIn()

    def close(self):
        """Close the browser."""

        self._print("Closing browser...")
        self.browser.close()






