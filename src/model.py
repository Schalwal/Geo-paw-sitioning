import sys
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm

from sklearn import linear_model
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from scipy import stats

os.environ["USE_PYGEOS"] = "0"
import geopandas as gpd

pd.options.mode.chained_assignment = None

# Import Combined Raw Data and Ouput from PCA

df_combined = pd.read_csv("./res/Berlin.csv", index_col = "Unnamed: 0")
df_important_features_PCA = pd.read_csv("./res/berlin_important_features.csv", index_col = "Unnamed: 0")

df_combined_grouped = df_combined.drop(columns = ["Grid_Code", 'City_Code', "geometry", 'City_Name', 'City']).groupby("Neighborhood_Name").median().reset_index(drop = True)

print("Most important feature due to PCA is: " + df_important_features_PCA["features"][0] + " with a variance of "
 + str(df_important_features_PCA["explained_variance"][0]))

# Perform Random Forest Regressor to identify further important features of overall dataset

y_rand_regr = df_combined_grouped["Land_Value"].values.reshape(-1, 1)
X_rand_regr = df_combined_grouped.drop(columns = ["Land_Value"]).values #'hhtyp_multiplepers_wout_nuclear',

scaler = StandardScaler()

X_rand_regr_scaled = scaler.fit_transform(X_rand_regr)
y_rand_regr_scaled = scaler.fit_transform(y_rand_regr)

names = df_combined_grouped.drop(columns = ["Land_Value"]).columns
reg = RandomForestRegressor(random_state = 123455)
reg.fit(X_rand_regr_scaled, y_rand_regr_scaled)

df_important_features_berlin = pd.DataFrame(sorted(zip(map(lambda x: round(x, 4), reg.feature_importances_), names), 
             reverse=True), columns = ["value", "feature"]).head()
df_important_features_berlin

# Perform Linear Regression based on important features from the random forest regressor

y_regr = df_combined_grouped["Land_Value"].values.reshape(-1, 1)
X_regr = df_combined_grouped.drop(columns = ["Land_Value"])[df_important_features_berlin["feature"].tolist()].values

X_regr_scaled = scaler.fit_transform(X_regr)
y_regr_scaled = scaler.fit_transform(y_regr)

# show summary of OLS with R2

training_values = sm.add_constant(X_regr_scaled)
est = sm.OLS(y_regr_scaled, training_values)
est2 = est.fit()
print(est2.summary())

regr = linear_model.LinearRegression()
regr.fit(X_regr_scaled, y_regr_scaled)

print('Intercept: \n', regr.intercept_)
print('Coefficients: \n', regr.coef_)

# Perform 5 Fold CrossValidation

scores = cross_val_score(regr, X_regr_scaled, y_regr_scaled, cv = 5)
scores

# Calculate Accuracy

print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

#df_combined_export = df_combined.drop(columns = ["Grid_Code", 'City_Code', "geometry", 'City_Name', 'City']).groupby(["Neighborhood_Name", "Neighborhood_FID"]).median().reset_index()

#df_combined_export[["Land_Value"] + df_important_features_berlin["feature"].tolist() + ["Neighborhood_Name", "Neighborhood_FID"]].to_csv("Berlin_plotting.csv")