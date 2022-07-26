# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless = False)

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Set up parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')

    try: 
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first <a> tag and save it as  `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_title


        # User the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        news_p

    except AttributeError:
        return None, None

    return news_title, news_p



    
    
    
    
    
    
    
### Featured Images


# Visit URL
url = "https://spaceimages-mars.com"
browser.visit(url)

def featured_image(browser):

    # Fill and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup

    html = browser.html
    img_soup = soup(html, 'html.parser')


    # Find the relative image url
    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        img_url_rel


        # Use base URL to create an absolute
        img_url = f'https://spaceimages-mars.com/{img_url_rel}'


        
    except AttributeError:

        return None

    return img_url



def mars_facts():
    try: 
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None

    # Assign columns and set index of df
       
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)


    # Convert df to html, add bootstrap
    return df.to_html()
