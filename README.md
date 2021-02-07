## 
<img src="/img/google-medic-update-1533729137.gif" height="500" width="900" />

?????? Check the main project out [here](https://eagledashboard-health.herokuapp.com)!

## Project Goal
How has the online search interest for top health issues or diseases changed over time? And how does the online search interest compare with the real-life leading causes of death?

To investigate this question, our team used the online health search data in the US from 2004 to 2017 provided by Google Trends as well as the real-life leading death-causing disease data provided by the US CDC Department. We chose the United States to as the representative population. And Google Trends data in particular allows us to see what people are searching for at a very local level. With regard to the booming technological advancements and the growing reliance people have had on Internet, we will make visualizations and draw insights from our data to understand in the past two decades how the online search patterns reflect the real-life health conditions for millions of Americans.

Overall, the online health search has been increasing and presumably will keep increasing, due to the growth of Telehealth and technologies, which will sustain a foreseeable phenomenon in the future, in the United States and probably similarly else where. In the more technologically advanced and more metropolitan regions, this growing trend of online health search is more conspicuous. 


## Research Question
How have the most online searched diseases changed over the past two decades in the United States?


## Data sources
* [Kaggle: Health searches by US Metropolitan Area, 2004-2017](https://www.kaggle.com/GoogleNewsLab/health-searches-us-county)
   
* [CDC Data: 10 leading causes of death per 100,000 population from 2004-2017](https://www.cdc.gov/nchs/fastats/deaths.htm)
   
## Architectural Diagram 
<img src="/img/Screen Shot 2020-10-01 at 12.21.00 AM.png" height="500" width="1200" />


## ?? ETL Process

### Extract 

Data sourced from [Reelgood.com](https:)
User review analysis extracted from Nielsen Insights and drived 10,000 synthetic data using the analysis provided. 
### Transform

Data scraped, cleaned and transformed by using Python Jupyter Notebook. [`UserReview_Analysis.ipynb`]()

### Load 

- This project used Python Jupyter Notebook to load transformed data in to , MongoDB & MySQL database. [`loadData.ipynb`]()
- Python Flask–powered RESTful API were used to deploy the data into the web, and API end point links created. API links store our cleaned and transformed data in json format and are publicly accessible for visitors of our website.

<img src="/img/Api_link/>

## Deployment 
The app is deployed in Heroku in order to access the page click the following link 

- https://Ripe-Banana-6.herokuapp.com/

You can find our presentation [slide here]

## Data Analysis and Visualization

#### Objectives
* How has the online health search volume changed over the years in general? Can we confirm that people are increasingly reliant on Telehealth? (Visualized with a Single Line Chart)
* How has the online health search volume changed in terms of the specific health conditions or the diseases over the years? (Visualized with a Multiple Line Chart, a Radar Chart, and a Boxplot)
* How have the online health search volume changing patterns varied geologically? Which states/cities have been more reliant on searching for health issues online? (Visualized the main observation with a Choropleth map and a Bar Chart in the main dashboard, and in more details in the Comparison dashboard with a Stadium Track Chart, a Bar Chart, a Choropleth map, and Scatterplots)
* How have the searches of the health conditions correlate with each other? (Visualized with a Correlation Matrix)
* What is the situation about the real-life leading diseases? How have the real-life leading causes of death coincide with people’s online health search trends? (Visualized with a Multiple Line Chart)

The following visualizations are [made](https://Ripe-Banana-6-health.herokuapp.com/static/dashbords/main.html):

### State and Region (Choropleth map)
<img src=" " />

### Plot
<img src=" " />

### Plot 
<img src=" "/>

### Plot 
<img src=" "/>


## Team members (Team Name)
* Desiree Herschnberger (Des)
* Redeat Bekele
* Sveena Sharma
* Taslemun Nahar (Tas)
* Thomas Keane (Tom)
* William Pappas (Billy)
