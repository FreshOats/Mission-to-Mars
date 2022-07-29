#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from bs4 import SoupStrainer
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[24]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless = False)


# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Set up parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title').get_text()


# In[6]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# User the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[8]:


# Visit URL
url = "https://spaceimages-mars.com"
browser.visit(url)


# In[9]:


# Fill and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup

html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use base URL to create an absolute
img_url = f'https://spaceimages-mars.com/{img_url_rel}'


# ## Mars Facts

# In[13]:


# Read in html via pandas

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace = True)
df


# In[14]:


df.to_html()


# In[ ]:





# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# 

# In[25]:


# 1. Use browser to visit the URL
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[26]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

for i in range(0, 4):
    # Open link to next page for each hemisphere
    browser.links.find_by_partial_text('Hemisphere Enhanced')[i].click()
    html = browser.html

    # Locate the title text
    title_soup = soup(html, 'html.parser')
    img_title = title_soup.find('h2', class_='title').text

    # Get the relative path from the href using SoupStrainer
    rel_path = []
    for link in soup(html, parse_only=SoupStrainer('a')):
        if hasattr(link, 'href'):
            rel_path.append(link['href'])

    # Create the full link path
    img_link = url + rel_path[3]

    # Append the dictionary of link and title the list 
    hemisphere_image_urls.append({'img_url': img_link, 'title': img_title})

    # Return to the index page before cycling to the next image
    browser.links.find_by_partial_text('Back').click()


# In[28]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[23]:


# 5. Quit the browser
browser.quit()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




