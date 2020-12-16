# Import dependencies

import pandas as pd

def scrape():
    # Creating dictionary that will store every scraped data
  
    # Initiating browser
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    

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
 
        for y in article_list:
            if y[:11] == "InSight sol":
                latest_tweet = y
                main_dict["last_tweet"] = latest_tweet
                break

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
 

  
# MARS  
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
            
              # Finally, the values are appended as a dictionary into the list
            browser.visit("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")

    browser.quit()
    return main_dict