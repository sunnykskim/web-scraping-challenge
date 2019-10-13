#!/usr/bin/env python
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd


# In[2]:


# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
get_ipython().system('which chromedriver')


# ## NASA Mars News

# In[3]:


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


# In[5]:


browser = init_browser()

# Visit nasa site to be scraped
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Scrape page into Soup
html = browser.html
soup = bs(html, "html.parser")

# # Get the story title
title = soup.find('div', class_='content_title').text

# # Get the teaser paragraph
teaserp = soup.find('div', class_='article_teaser_body').text
    
# # Store data in a dictionary
marsarticle = {"title": title,"teaserp": teaserp}
marsarticle


# ## JPL Mars Space Images - Featured Image

# In[ ]:


#https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars


# In[6]:


# Visit site to be scraped
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)
#click through full image button
fullimgbutton = browser.find_by_id("full_image")
fullimgbutton.click()
#click through more info button
browser.is_element_present_by_text("more info")
moreinfo = browser.find_link_by_partial_text("more info")
moreinfo.click()


# In[7]:


html = browser.html
img_soup = bs(html, "html.parser")


# In[8]:


#get img url
img_url = img_soup.select_one("figure.lede a img").get("src")
#assign url to main_url
main_url = 'https://www.jpl.nasa.gov'
#combine 
featured_image_url = main_url + img_url
featured_image_url


# ## Mars Weather
# 
# 
# 
# 

# In[9]:


# Visit site to be scraped
url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)


# In[10]:


html = browser.html
twitter_soup = bs(html, "html.parser")


# In[11]:


mars_weather = twitter_soup.find("p", "tweet-text").get_text()
mars_weather


# ## Mars Facts
# 

# In[12]:


#https://space-facts.com/mars/
url = 'https://space-facts.com/mars/'


# In[13]:


#pandas read html
mars_df = pd.read_html(url)[0]
mars_df


# In[14]:


mars_df.to_html()


# ## Mars Hemispherses
# 

# In[15]:


# Visit site to be scraped
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[16]:


html = browser.html
hemisphere_soup = bs(html, "html.parser")


# In[17]:


#make list to store hemisphere img url + title
mars_hemisphere = []


# In[20]:


#for loop to scrape img url(img wide-images) and img title (h2 titles)
for i in range (4):
    images = browser.find_by_tag('h3')
    images[i].click()
    html = browser.html
    soup = bs(html, 'html.parser')
    partial_url = soup.find("img", class_="wide-image")["src"]
    image_title = soup.find("h2",class_="title").text
    image_url = 'https://astrogeology.usgs.gov'+ partial_url
    image_dict = {"image_url":image_url, "title":image_title}
    mars_hemisphere.append(image_dict)
    browser.back()
    
mars_hemisphere


# In[ ]:




