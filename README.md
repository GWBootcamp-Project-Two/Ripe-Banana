Welcome to RIPE BANANAS

/Users/Taslemun/Downloads/bb1.jpg


## Project Goal

A video streaming service is an on demand online entertainment source for movies, TV shows and other streaming media. These services provide an alternative to cable and satellite on demand service, often at a lower cost. Our goal is to have a simple, user friendly experience to finding a TV show or movie all in on application. The use of streaming services often requires fees and subscriptions to watch. Some services feature numerous devices such as smart TVs, tablets, computers, streaming media receivers and smartphones. There are other services that are ad-supported, or run on a freemium model and also offer some full feature movies at a cost. Also, there are other services that may be more limited in the type of devices, or tailored to a specific brand’s devices, much like iTunes for Apple devices. Having all this information in one area will make it a lot easier to find what you looking for in a jiffy. 

We have created a web application called "RIPE BANANAS" on the different streaming services available. You can browse through various TV shows and movies available online through this application and with one click you will be able to easy go on that site and watch your desirable media content. You can search by title, genre, the year it was released, and most importantly which service you can watch it on. The app was created for a quick and better user experience. 

## Question for our project:

Is there an application where we can find extensive comparison data on different streaming services and what they have to offer?

Answer: 

RIPEBANANAS! 
/Users/Taslemun/Downloads/rb-banana-branding/loho-v-y.png

# Process: 

/Users/Taslemun/Downloads/image.png


# Extraction of the Data

Our data is sourced from Reelgood.com, various streaming service websites and we got user review analysis extracted from Nielsen Insights and derived 10,000 synthetic data using the analysis provided to analyze various components surround streaming services and their users based on, gender, age, genre, titles of media and much more. 

### Transform

To transform the data we scraped, we cleaned and transformed it by using Python Jupyter Notebook and made various comparison visualizations using pandas. 

/Users/Taslemun/Desktop/Screen Shot 2021-02-10 at 10.48.17 PM.png

/Users/Taslemun/Desktop/Screen Shot 2021-02-10 at 10.49.10 PM.png

/Users/Taslemun/Desktop/Screen Shot 2021-02-10 at 10.49.32 PM.png

We used Leaflet and GEO mapping on JavaScript 

/Users/Taslemun/Desktop/Screen Shot 2021-02-10 at 10.50.04 PM.png

/Users/Taslemun/Desktop/Screen Shot 2021-02-10 at 10.50.18 PM.png


### Load 

For this project to efficiently work we used Python Jupyter Notebook to load the clean transformed data in to MongoDB & MySQL database. 
Python Flask powered a restful API were used to deploy the data into the web, and using API end point links were created. API links store our cleaned and transformed data in a json format and are publicly accessible for visitors of our website.

## Deployment 

The app is deployed in Heroku in order to access the page click the following link 

https://Ripe-Banana-6.herokuapp.com/

## The Ripe Bananas Team Members
* Desiree Herschnberger (Des)
* Redeat Bekele
* Sveena Sharma
* Taslemun Nahar (Tas)
* Thomas Keane (Tom)
* William Pappas (Billy)
