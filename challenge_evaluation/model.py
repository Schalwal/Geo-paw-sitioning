# system and general imports
import sys
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm

os.environ["USE_PYGEOS"] = "0"
import geopandas as gpd

pd.options.mode.chained_assignment = None  # type: ignore

import logging

import warnings
from sklearn.exceptions import DataConversionWarning

warnings.filterwarnings(action="ignore", category=DataConversionWarning)

# statistical learning imports
from sklearn import linear_model
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from scipy import stats


def import_data(
    PCA_components_path: str, Berlin_data_path: str
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Import ouput from PCA and combined raw data
    """

    df_combined = pd.read_csv(Berlin_data_path, index_col=0)
    df_important_features_PCA = pd.read_csv(PCA_components_path, index_col=0)

    df_combined_grouped = (
        df_combined.drop(
            columns=["Grid_Code", "City_Code", "geometry", "City_Name", "City"]
        )
        .groupby("Neighborhood_Name")
        .median()
        .reset_index(drop=True)
    )
    logger.info(
        "Most important feature due to PCA is: \n%s ",
        str(df_important_features_PCA["features"][0]),
    )
    logger.info(
        "The portion of the overall variance of the zensus and land_value datasets explained by our model is: \n%s",
        str(df_important_features_PCA["explained_variance"][0]),
    )

    return df_combined_grouped, df_important_features_PCA


def random_forest_regressor_features(df_PCA_features: pd.DataFrame) -> pd.DataFrame:
    """
    Performing random forest regression to identify the most important features of overall dataset
    """

    y_rand_regr = (df_PCA_features["Land_Value"].values).reshape(-1, 1)  # type: ignore
    X_rand_regr = df_PCA_features.drop(columns=["Land_Value"]).values

    X_rand_regr_scaled = scaler.fit_transform(X_rand_regr)
    y_rand_regr_scaled = scaler.fit_transform(y_rand_regr)

    names = df_PCA_features.drop(columns=["Land_Value"]).columns
    reg = RandomForestRegressor(random_state=123455)
    reg.fit(X_rand_regr_scaled, y_rand_regr_scaled)

    df_most_imp_features_berlin = pd.DataFrame(
        sorted(
            zip(map(lambda x: round(x, 4), reg.feature_importances_), names),
            reverse=True,
        ),
        columns=["value", "feature"],
    ).head()
    return df_most_imp_features_berlin


def data_preparation(
    df_PCA_features: pd.DataFrame, df_RF_features: pd.DataFrame
) -> tuple[np.ndarray, np.ndarray]:
    """
    Selecting features, normalizing and splitting data
    """

    y_regr = df_PCA_features["Land_Value"].values.reshape(-1, 1)
    X_regr = df_PCA_features.drop(columns=["Land_Value"])[
        df_RF_features["feature"].tolist()
    ].values

    return scaler.fit_transform(X_regr), scaler.fit_transform(y_regr)


def model_fit(
    X_train: np.ndarray, y_train: np.ndarray
) -> linear_model.LinearRegression:
    """
    fitting linear regression model with training data
    """
    regr = linear_model.LinearRegression()
    regr.fit(X_train, y_train)

    logger.info("\n Intercept: \n%s", str(regr.intercept_))
    logger.info("Coefficients: \n%s", str(regr.coef_))
    return regr


def model_predict(
    regr: linear_model.LinearRegression, X_test: np.ndarray
) -> np.ndarray:
    y_pred = regr.predict(X_test)
    return y_pred


def eval_model(X_train: np.ndarray, y_train: np.ndarray):
    """
    evaluating model training on OLS, cross-validation and accuracy
    """

    training_values = sm.add_constant(X_train)
    est = sm.OLS(y_train, training_values)
    est2 = est.fit()
    logger.info(str(est2.summary()))
    logger.info("\n R^2 value of: \n%s", str(est2.rsquared))

    # Perform 5 fold cross-validation and log the scores
    scores = cross_val_score(regr, X_train, y_train, cv=5)
    logger.info("\n 5 fold cross-validation scores: \n%s", str(scores))

    # Calculate and log accuracy
    logger.info("\n Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    scaler = StandardScaler()

    PCA_path = "challenge_evaluation/berlin_important_features.csv"
    data_path = "challenge_evaluation/Berlin.csv"

    df_features, df_data = import_data(
        PCA_components_path=PCA_path, Berlin_data_path=data_path
    )

    df_imp_features = random_forest_regressor_features(df_PCA_features=df_features)

    # please use this data for your own model
    X, y = data_preparation(df_PCA_features=df_features, df_RF_features=df_imp_features)

    # train-test-split here #
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.1, random_state=42
    )

    regr = model_fit(X_train=X_train, y_train=y_train)

    # predicted y values
    y_pred = model_predict(regr=regr, X_test=X_test)

    eval_model(X_train=X_train, y_train=y_train)
