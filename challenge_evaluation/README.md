# Geo-paw-sitioning

Hi ifoHack 2023 Jury, staff, and participants! :wave: <br>
Welcome to our land price prediction repository, Geo-paw-sitioning :cat2: <br> 
We use machine learning (random forests) to predict land prices based on
socio-economic factors, land types, and neighborhood-network analysis. Our platform 
helps decision-makers in real estate, agriculture, and land-use planning to make 
informed choices. We'd love your feedback and collaboration to improve our models!

## Team
- Ariz
- Felix
- Ferdinand
- Patrick
We have backgrounds in Economics, Data Science, Psychology, and Computer Sciences.

## Which data we used and which features we extracted

1. Census data
We used census data at neighborhood level which is computed as the mean of the values at grid-level (). We implemented census as indicator for the socioeconomic status of the neighborhood which is again a good proxy for land prices. Since the census data set has a lot of features we run a Principal Component Analysis to reduce dimensionality. It reduces the number of features roughly by half per city.

2. Land Prices
Within the Land Prices folder we splitted up the area types as additional features.

3. Open Street Map Data

Total distance of different edge types in each neighborhood:
For each neighborhood we use the total length of different kinds of paths such as total length of roads, walking lanes, cycling lanes and others. We thought that this variable influences livability of the neighborhood and thereby the landprice (e.g. a lot of roads could negatively affect the price). We do this by feeding the polygons of each neighborhood into osmnx and getting the cumulative length of all the edges of a certain type (we use ['drive', 'bike', 'walk', 'drive_service', 'all', 'all_private']).

Total count of amenities in each neighborhood:
For each neighborhood we use the count of different amenities (e.g. hospitals, restaurants). We thought that these variables are an indicator for populated and important regions with a higher demand for such services. We implemented this with osmnx where we get the count for all selected amenities in each neighborhood polygon. As amenities we used ["restaurant", "cafe", "school", "administration", "advertising", "archive", "bench", "ev charging", "financial advice", "gym", "hotel", "park", "library", "refugee housing", "student accommodation", "nursery", "preschool", "public building", "shop", "sport school", "hospital"].

## How we brought the features into production

With the extracted features we performed a Random Forest Regressor to identfy the most important factors that might drive the performance of the linear model most.

The calculated most important features are the independent variables for the linear model.
The linear model for the city of Berlin has an R² of 0.678.

## Visualisation

The results are presented in a Streamlit App that allow explorative geospatial data with included features for the cities of Berlin, Bremen, Dresden, Frankfurt and Cologne. Additionally it shows the overwhelming results from the Random Forest Regressor as Machine Learning tool as well as the results from the trained linear model.

## Model execution
Please run
```
python challenge_evaluation/model.py
```
from within the directory "Geo-paw-sitioning".





