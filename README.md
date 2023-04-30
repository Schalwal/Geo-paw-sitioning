# Geo-paw-sitioning

Hi ifoHack 2023 Jury, staff, and participants! :wave: <br>
Welcome to our land price prediction repository, Geo-paw-sitioning :cat2: <br> We use machine 
learning (random forests) to predict land prices based on socio-economic factors. Our platform helps 
decision-makers in real estate, agriculture, and land-use planning to make informed 
choices. We'd love your feedback and collaboration to improve our models!

## Which features we used and how we found them

1. Census data
We use census data at neighborhood level which is computed as the mean of the values at grid-level. We implemented census as indicator for the socioeconomic status of the neighborhood which is again a good proxy for land prices. Since the census data set has a lot of features we run a PCA to reduce dimensionality. It reduces the number of features roughly by half.

2. Land Types
From the Landprices files we used the land types as features. 

3. Total distance of different edge types in each neighborhood:
For each neighborhood we use the total length of different kinds of paths such as total length of roads, walking lanes, cycling lanes and others. We thought that this variable influences livability of the neighborhood and thereby the landprice (e.g. a lot of roads could negatively affect the price). We do this by feeding the polygons of each neighborhood into osmnx and getting the cumulative length of all the edges of a certain type (we use ['drive', 'bike', 'walk', 'drive_service', 'all', 'all_private']).

4. Total count of amenities in each neighborhood:
For each neighborhood we use the count of different amenities (e.g. hospitals, restaurants). We thought that these variables are an indicator for populated and important regions with a higher demand for such services. We implemented this with osmnx where we get the count for all selected amenities in each neighborhood polygon. As amenities we used ["restaurant", "cafe", "school", "administration", "advertising", "archive", "bench", "ev charging", "financial advice", "gym", "hotel", "park", "library", "refugee housing", "student accommodation", "nursery", "preschool", "public building", "shop", "sport school", "hospital"].





