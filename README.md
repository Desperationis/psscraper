# psscraper
![login](preview/login.png)

A web scrapper library for powerschool websites that have a similar log in page to above. This library exposes an interface that allows you to log in, check your grades, and predict your grades.

## Installation
You can install this library, but not `main.py`, by using `pip3 install psscraper` which will automatically install the requirements that are listed below.

## Requirements
This entire library relies on using Python 3.x, [Selenium](https://github.com/SeleniumHQ/selenium), [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/), and Firefox's [geckodriver](https://github.com/SeleniumHQ/selenium) to log in and scrape pages. 

You can install selenium and BeautifulSoup by running `python3 -m pip install -r requirements.txt`. For the selenium driver, put `geckodriver` into PATH, otherwise the browser won't be able to open. 

## Predict grades using main.py
To log in using the included `main.py` to predict your grade for a class, you need to create a file named `credentials` (without .txt or anything) at the root of the project directory. Here, you will enter your credentials (without curly brackets) as follows:

    {username}
    {password}
    
After that, run `main.py` by calling `python3 main.py` in the root directory in the project. The output should look something like this (it's a GIF, wait for it):
![preview](preview/main.gif)

Here, "prediction" of your grades is adding a hypothetical assignment to a category and using basic math to predict your final grade based on how each category is weighed.

If you input `0` assignments to predict, you should get your actual grade. However, the number you get is special; It is one more decimal more precise than your current grade, and is obtained by actually adding up all your assignments and using math to get your final grade instead of scrapping the actual value. This provides two benefits:

* If you want to see how close to the edge your are from the next percent, you can use this number to see it; Powerschool rounds normally, so a `95.6%` would be a 96% and a `95.4%` would be a 95%.
* You can check if your teacher is purposefully lowering your grade. If you have suspicion your teacher is biased and is manually setting your grade lower, you can use this library to add up your assignments and see your actual grade. 

## Getting Started
Here is a basic script that will print all the classes you have:

    from psscraper import *
    import psscraper.scrapper.PowerschoolClassInfoScrapper
    
    # Log in to a powerschool website
    print("Logging in...")
    browser = psscraper.PowerschoolBrowser(Link="https://powerschool.nlmusd.k12.ca.us/", headless=True)
    browser.login("username", "password")

    # Parse home page for class IDs
    print("Parsing page for class IDs...")
    pageSource = browser.getPageSource()
    classInfoScrapper = psscraper.scrapper.PowerschoolClassInfoScrapper(pageSource)
    classIDs = classInfoScrapper.getCourseIDs()

    for classID in classIDs:
        # Get period and name for each class and print it
        courseInfo = classInfoScrapper.getCourseInfo(classID)
        className = " ".join(courseInfo)
        print(className)

To log in, you must first initialize `psscraper.PowerschoolBrowser` then use the `.login(username, password)` method to log in. 

After that, you can do whatever you want. To get information from actual pages from Powerschool, you feed in raw html data into a scrapper object (found in `psscraper.scrapper`) that will allow you to scrape as much information as you want. In this example, `psscraper.scrapper.PowerschoolClassInfoScrapper` is imported in order to scrap classroom information from `guardian/home.html` -- the page that is automatically switched to when you first log in. 

## Why is it slow?
This library is a browser-based web-scraper, meaning it literally opens up a browser, logs in, and scraps information with BeautifulSoup. This is because Powerschool does not have its own API, or at least doesn't provide it as open-source, to use to interact with your accounts. Because of this, the speed of this application is completely dependent on the speed of Firefox on your system and your internet connection. 

The beauty of this library however is that you can do anything you want with it. To speed the process up, you can cache your grades into a text file once you log in then write a separate program to read from that text file and use the information off of it really quickly. If you do this, you would only need to use this library whenever you want to update the grades on that text file. 




