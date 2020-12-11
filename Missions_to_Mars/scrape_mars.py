# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd

def scrape():
    # Creating dictionary that will store every scraped data
    main_dict = {}

    # Initiating browser
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=True)
    
# NASA MARS NEWS
    news_paragraph = ""
    # Repeating process for the paragraph string because the first time it fails in load the complete code
    while news_paragraph == "":
        browser.visit("https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest")
        browser.is_element_present_by_tag('LI', wait_time=10)
        html = browser.html
        soup = bs(html, "html.parser")
        # Storing First image, header and brief from the first News element.
        # We get the second [1] element for the header because the first one with the same class is not related to any News
        try:
            news_header = soup.find_all("div",class_="content_title")[1].text.strip()
            news_paragraph =  soup.find("div",class_="article_teaser_body").text.strip()
        except:
            news_paragraph = ""
    main_dict["news_header"] = news_header
    main_dict["news_p"] = news_paragraph

# FEATURED IMAGE
#Use splinter to navigate the site and find the image 
# url for the current Featured Mars Image and assign 
# the url string to a variable called featured_image_url.
    browser.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    html = browser.html
    soup = bs(html, "html.parser")
    # Again, we need the main webpage to get the the complete url for the image working.
    jpl_mainpage = "https://www.jpl.nasa.gov"
    # We get the a tag with a unique id, and then we extract the first element containing the href link
    featured_image = soup.find_all("a", id="full_image")
    featured_image = jpl_mainpage + featured_image[0]["data-fancybox-href"]
    main_dict["ft_img"] = featured_image

# MARS WEATHER
    # Creating variable to do the while statement
    latest_tweet = "None"
    browser.visit("https://twitter.com/marswxreport?lang=en")
    # The html code keeps reloading until I get the correct data, since sometimes the code needed is not parsed on the first try
    while latest_tweet == "None":
        # Code to scroll down a little because the latest tweet for the weather is on the middle of the page, so it is not parsed on the initial code
        browser.execute_script("window.scrollTo(1, document.body.scrollHeight);")
        html = browser.html
        soup = bs(html, "html.parser")
        # I create a list to iterate from all the tags and get the text of them
        article_list = []
        # Every tweet that contains text has a span tag with a class "css-901oao", so first I find all the tags with this specifications
        articles = soup.find_all("span", class_="css-901oao")
        # Then I loop to obtain the text of each class with that name
        for x in articles:
            article_list.append(x.text)

        for y in article_list:
            if y[:11] == "InSight sol":
                latest_tweet = y
                main_dict["last_tweet"] = latest_tweet
                break
            else:
                latest_tweet = "None"

# MARS FACTS
# Visit the Mars Facts webpage here and use Pandas to scrape the table 
# containing facts about the planet including Diameter, Mass, etc.
# At this point, we use the following methodology, but it was difficult to transfer to MongoDB
# so we consider another method:
# url4 = "https://space-facts.com/mars/"
# facts = pd.read_html(url4)[0]
# facts.columns=["Variable", "Value"]
# facts.set_index("Variable")
    url = "https://space-facts.com/mars/"
    table = pd.read_html(url)[0]
    table = table.rename(columns={0:"Description",1:"Value"})
    # passing the table to an HTML table
    html_table = table.to_html(index=False)
    # replace the \n text with nothing so it can be stored on the dictionary
    html_table = html_table.replace("\n","")
    # making the table
    html_table = html_table.replace('<th>','<th class="text-center">')
    html_table = html_table.replace('<table','<table border="1" class="table-hover w.auto pr-2">')
    html_table = html_table.replace('border="1" class="dataframe">',"")
    # Transfer to dictionary 
    main_dict["Html_table"] = html_table

  
# Mars Hemispheres 
    # Going to the webpage
    browser.visit("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
    html = browser.html
    soup = bs(html, "html.parser")
    # Getting all the links for the webpage
    all_links = soup.find_all("a", class_="itemLink product-item")

    # Since every hemisphere has two equal links (one for the image and one for the title), I iterate to get only the even results: 2, 4, 6 and 8
    # On every iteration, I go into the browser and get all the results needed.
    # Enumerating to get iteration number
    for index, link in enumerate(all_links):
        # Checking if iteration is even
        if (index % 2) == 0:
            varnum = int(index / 2)
            # Entering the first link
            browser.visit("https://astrogeology.usgs.gov" + link["href"])
            
            # Saving the html code in soup
            html = browser.html
            soup = bs(html, "html.parser")
            
            # I find all the anchor elemnts and then get the link that matches with the text "Sample" which is the direct link to the image
            a_tags = soup.find_all("a")
            for x in a_tags:
                if x.text == "Sample":
                    main_dict[f"image{varnum}"] = x["href"]
                    break
            main_dict[f"title{varnum}"] = soup.find("h2", class_="title").text
            
            # Finally, the values are appended as a dictionary into the list
            browser.visit("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")

    browser.quit()
    return main_dict