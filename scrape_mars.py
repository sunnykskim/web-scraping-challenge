from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time





def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    #scraped data dict.
    scraped_data = {}

    ## SCRAPING NEWS ARTICLE TITLE AND TEASER PARAGRAPH ## 

    # Visit nasa site to be scraped
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    time.sleep(2)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # # Get the story title
    title = soup.find('div', class_='content_title').get_text()

    # # Get the teaser paragraph
    teaserp = soup.find('div', class_='article_teaser_body').get_text()

    time.sleep(2)

    # # Store data in a dictionary
    scraped_data["news_title"] =  title
    scraped_data["teaser_p"] = teaserp

   
    ## SCRAPING MARS SPACE IMAGES ##

    # Visit site to be scraped
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(2)
    #click through full image button
    fullimgbutton = browser.find_by_id("full_image")
    fullimgbutton.click()
    time.sleep(2)
    #click through more info button
    browser.is_element_present_by_text("more info")
    moreinfo = browser.find_link_by_partial_text("more info")
    moreinfo.click()
    time.sleep(2)

    html = browser.html
    img_soup = bs(html, "html.parser")

    #get img url
    img_url = img_soup.select_one("figure.lede a img").get("src")
    #assign url to main_url
    main_url = 'https://www.jpl.nasa.gov'
    #combine 
    featured_image_url = main_url + img_url
    
    scraped_data["featured_image_url"] = featured_image_url



    ## SCRAPING MARS WEATHER ##

    # Visit site to be scraped
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(2)


    html = browser.html
    twitter_soup = bs(html, "html.parser")

    mars_weather = twitter_soup.find("p", "tweet-text").get_text()
    scraped_data["mars_weather"] = mars_weather


    ## SCRAPING MARS FACTS ##
    facts_url = 'https://space-facts.com/mars/'  

    mars_df = pd.read_html(facts_url)[0]
    marsfacts_html = mars_df.to_html()

    scraped_data["mars_facts_html"] = marsfacts_html


    ## SCRAPING MARS HEMISPHERES ##

    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    time.sleep(2)


    html = browser.html
    

    #make list to store hemisphere img url + title
    mars_hemisphere_urls = []
    
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        
        browser.find_by_css("a.product-item h3")[item].click()

        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        # title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Append Hemisphere Object to List
        mars_hemisphere_urls.append(hemisphere)
        
        scraped_data["mars_hemisphere"] = mars_hemisphere_urls

        # Navigate Backwards
        browser.back()

    return scraped_data






