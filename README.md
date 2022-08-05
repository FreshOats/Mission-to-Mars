# Mission-to-Mars
### Web scraping using a NoSQL database
#### by Justin R. Papreck
---

## Overview
This project scraped data and images from NASA websites and images from other sourced related to Mars to create a website that updates with the latest Mars headlines, an image of the day as well as full-size images of the Martian hemispheres. The web scraping was performed using python with BeautifulSoup, Selenium, Splinter, the ChromeDriveManager, and MongoDB to store and retrieve the data. In order to present the data, Flask was used to create a webpage, and the HTML was modified to improve functionality and aesthetics. 

---
## Dependencies and Peripherals
BeautifulSoup, Splinter, ChromeDriveManager, Selenium, Pandas, MongoDB, PyMongo, Flask, Bootstrap

---
## Web Scraping
The functions coded were used to open the browser to the NASA Mars News Site and scrape the data using BeautifulSoup. Additionally the image of the day was retieved from spaceimages-mars.com. Mars facts were retrieved from a different facet of the Mars news site, and finally the hemisphere images were acquired from the marshemispheres website. Each of these scrapes haad a function defined to retreive the data: 

```
def mars_news(browser):
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
  
    try:
        slide_elem = news_soup.select_one('div.list_text')       
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_p = slide_elem.find(
            'div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p 
```

In the pages where multiple pages were required to get all of the data, Splinter was used to navigate through the page clicks. 

```
def featured_image(browser):
    url = "https://spaceimages-mars.com"
    browser.visit(url)

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url
```

To get the hemispheres, each image required multiple pages that had to be entered and returned from. 

```
def hemispheres(browser):
    hemisphere_image_urls = []
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    for i in range(0, 4):
        # Open link to next page for each hemisphere
        browser.links.find_by_partial_text('Hemisphere Enhanced')[i].click()
        html = browser.html

        # Locate the title text
        hemi_soup = soup(html, 'html.parser')
        img_title = hemi_soup.find('h2', class_='title').text

        # Get the relative path
        rel_path = []
        for link in hemi_soup.find_all('a'):
            rel_path.append(link.get('href'))

        # Create the full link path
        img_link = url + rel_path[3]

        # Append the dictionary of link and title the list
        hemisphere_image_urls.append({'img_url': img_link, 'title': img_title})

        # Return to the index page before cycling to the next image
        browser.links.find_by_partial_text('Back').click()

    return hemisphere_image_urls
```

Finally, after each of the components were composed, one function tied them together to store the data in a dictionary that could be read and presented by Flask:

```
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    


    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(), 
        "hemispheres": hemispheres(browser)
        
    }

    # Stop webdriver and return data
    browser.quit()
    return data
```

## Communicating with MongoDB
MongoDB was used becuase of the disorganized and nonuniform nature of the data. MongoDB communicated with the python and Flask applications through PyMongo via the app.py file. 

```
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set": mars_data}, upsert=True)
   return redirect('/', code=302)


if __name__ == "__main__":
   app.run()
```

## Updating the Website
The website was created and updated using Flask, and the HTML was modified using Bootstrap to improve the aesthetics. The sizes were adjusted for use of small screens such as phone screens. The hemisphere images were clipped into a circular shape by changing the class = "img-circle".
