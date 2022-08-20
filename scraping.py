# import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# create a function that will initialize the browser, create a data dictionary, end the WebDriver, return the scraped data
def scrape_all():

    # Initiate headless driver for deployment
    # we are deploying our code into a usable web app, we don't need to watch the script work (hence headless = True)
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = True) 
    # When scraping, the "headless" browsing session is when a browser is run without the users seeing it at all.

    # create variable for what is returned from mars_news() function. 
    news_title, news_paragraph = mars_news(browser)

    # set news title and paragraph variables, this code tells Python that we'll be using our mars_news function to pull this data.
    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph" :news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    # end the automated browsing session.
    # this is very important because the automated browser would otherwise not know when to shutdown
    # the browser will therefore continure to listen for instructions and this can put a strain on the computer's memory or battery.
    browser.quit()

    return data

# from the scraping code, we need to create a function for each individual item that we are scraping.

def mars_news(browser): # browser is our global variable that we will use for our function

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'

    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1) 
    # more info: https://splinter.readthedocs.io/en/latest/matchers.html
    # the .is_element_present_by_css function checks for certain elements that are argued
    # div.list_text is the html tag and class for the article titles on the webpage 
    #  returns True since element is present

    # create an HTML object and parse with bs4
    html = browser.html

    news_soup = soup(html, 'html.parser')

    # add try-except block so that python can continue to run the rest of the code if there is nothing to update
    try:  
        # assigned slide_elem as the variable to look for the <div /> tag 
        # and its descendent (the other tags within the <div /> element)
        slide_elem = news_soup.select_one('div.list_text') # select_one() finds only the first tag that matches a selector

        # the period is used for assigning classes in div.list_text
        slide_elem

        # find the title of the article in the div tag of class list_text
        # The output should be the HTML containing the content title and anything else nested inside of that <div />.
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_= 'content_title').get_text()
        # There are two methods used to find tags and attributes with BeautifulSoup:
        # .find() is used when we want only the first class and attribute we've specified.
        # .find_all() is used when we want to retrieve all of the tags and attributes.

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

        # always include return function so python knows that function is completed

    except AttributeError: # note that if BaseException is put in place off AttributeError it will cover any error type0

        return None, None
    
    return news_title, news_p

# ### Featured Images

# create a function to scrape the image using code from the scraping.py file
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button on the webpage
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup 
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # add try-except block 
    try: 
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_ = 'fancybox-image').get('src')

        # create an absolute url that works. The above url is only partial
        img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    except AttributeError:

        return None

    return img_url
# NOTES: 
# We're using an f-string for this print statement because it's a cleaner way to create print statements; 
# they're also evaluated at run-time. This means that it, 
# and the variable it holds, doesn't exist until the code is executed and the values are not constant. 
# This works well for our scraping app because the data we're scraping is live and will be updated frequently.

# create function for mars facts:

def mars_facts(browser):

    # add try-except block:
    try:
        # use pandas read_html() function to return a list of all the tables present  in the html code of the website.
        # using the index [0] will return the first table found in the html. 
        df = pd.read_html('https://galaxyfacts-mars.com/')[0]

    except AttributeError:
        return None
    
    # create column names for df
    df.columns=['description', 'Mars', 'Earth']

    # .set_index() function, we're turning the Description column into the DataFrame's index. 
    # inplace=True means that the updated index will remain in place without having to reassign the DataFrame to a new variable.
    df.set_index('description', inplace = True)

    return df.to_html()

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

# Note:
# Live sites are a great resource for fresh data, but the layout of the site may be updated or otherwise changed. 
# When this happens it's likely the scraping code will break and need to be reviewed and updated to be used again.
# For example, an image may suddenly become embedded within an inaccessible block of code because the developers 
# switched to a new JavaScript library. 
# It's not uncommon to revise code to find workarounds or even look for a different, scraping-friendly site all together.

