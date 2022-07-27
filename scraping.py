# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployement
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping data and store results in a dictionary
    data = {
        "news_title": news_title, 
        "news_paragraph": news_paragraph, 
        "featured_image": featured_image(browser), 
        "facts": mars_facts(), 
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Set up parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    

    try: 
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first <a> tag and save it as  `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # User the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        

    except AttributeError:
        return None, None

    return news_title, news_p


### Featured Images



def featured_image(browser):

    # Visit URL
    url = "https://spaceimages-mars.com"
    browser.visit(url)


    # Fill and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup

    html = browser.html
    img_soup = soup(html, 'html.parser')


    # Find the relative image url
    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
              
    except AttributeError:

        return None


    # Use base URL to create an absolute
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url



def mars_facts():
    # Use read_html to scrap the facts table into a df
    try: 
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None

    # Assign columns and set index of df
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)


    # Convert df to html, add bootstrap
    return df.to_html(classes='table table-striped')



if __name__ == "__main__":
    print(scrape_all())