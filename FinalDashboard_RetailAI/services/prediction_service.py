import os
import pickle
import joblib
import pandas as pd
import streamlit as st

MODELS_DIR = "models"
DATA_DIR = "data"


@st.cache_resource
def load_revenue_model():
    """Loads the revenue prediction model using joblib (correct method)."""
    model_path = os.path.join(MODELS_DIR, "RevenuePredictionModel.pkl")
    try:
        model = joblib.load(model_path)
        return model
    except Exception as e:
        st.error(f"Failed to load RevenuePredictionModel: {str(e)}")
        return None


@st.cache_resource
def load_model_columns():
    """Loads the expected columns for the model using pickle."""
    col_path = os.path.join(MODELS_DIR, "model_columns.pkl")
    try:
        with open(col_path, "rb") as f:
            columns = pickle.load(f)
        return columns
    except Exception as e:
        st.error(f"Failed to load model_columns: {str(e)}")
        return None


@st.cache_data
def load_dataset(filename):
    """Loads CSV datasets and caches them."""
    path = os.path.join(DATA_DIR, filename)
    try:
        return pd.read_csv(path)
    except Exception as e:
        st.error(f"Failed to load {filename}: {str(e)}")
        return pd.DataFrame()


def get_predictions_data():
    return load_dataset("Predictions.csv")


def get_model_comparison_data():
    return load_dataset("ModelComparison.csv")


def get_feature_importance_data():
    return load_dataset("FeatureImportance.csv")


def build_input_dataframe(inputs: dict, model_columns: list) -> pd.DataFrame:
    """
    Build the dataframe exactly as expected by the trained Linear Regression model.
    """

    # Initialize all expected columns to 0
    row = {col: 0 for col in model_columns}

    # =====================================================
    # Numerical Features
    # =====================================================

    row["YearNumber"] = int(inputs["Year"])
    row["MonthNumber"] = int(inputs["Month"])
    row["TotalQuantity"] = int(inputs["TotalQuantity"])

    # Extract discount decimal explicitly for model inference
    if "AverageDiscountDecimal" in inputs:
        row["AvgDiscount"] = float(inputs["AverageDiscountDecimal"])
    elif "AverageDiscountPercentage" in inputs:
        row["AvgDiscount"] = float(inputs["AverageDiscountPercentage"]) / 100.0
    else:
        row["AvgDiscount"] = float(inputs["AverageDiscount"]) / 100.0

    row["NumberOfProducts"] = int(inputs["NumProducts"])
    row["NumberOfCategories"] = int(inputs["NumCategories"])

    # =====================================================
    # Gender
    # Baseline = Female
    # =====================================================

    gender = inputs["Gender"]

    if gender == "Male":
        row["Gender_Male"] = 1

    elif gender == "Unknown":
        row["Gender_Unknown"] = 1

    # Female -> all zeros

    # =====================================================
    # Channel
    # =====================================================

    channel = inputs["Channel"]

    if channel == "Marketplace":
        row["ChannelName_Marketplace"] = 1

    elif channel == "Mobile App":
        row["ChannelName_Mobile App"] = 1

    elif channel == "Store":
        row["ChannelName_Store"] = 1

    elif channel == "Web":
        row["ChannelName_Web"] = 1

    # =====================================================
    # Payment Method
    # =====================================================

    payment = inputs["PaymentMethod"]

    if payment == "COD":
        row["PaymentMethod_COD"] = 1

    elif payment == "Card":
        row["PaymentMethod_Card"] = 1

    elif payment == "Cash":
        row["PaymentMethod_Cash"] = 1

    elif payment == "Wallet":
        row["PaymentMethod_Wallet"] = 1

    # =====================================================
    # Create dataframe
    # =====================================================

    df = pd.DataFrame([row])

    # Keep exactly the same order used during training
    df = df[model_columns]

    return df

def predict_revenue(inputs: dict) -> float:
    """
    Runs the Linear Regression model on user inputs and returns
    the predicted total revenue.
    """
    model = load_revenue_model()
    model_columns = load_model_columns()

    if model is None or model_columns is None:
        return 0.0

    try:
        df = build_input_dataframe(inputs, model_columns)

        print("=" * 50)
        print("MODEL INPUT")
        print(df.T)
        print("=" * 50)

        prediction = model.predict(df)[0]

        print("Prediction:", prediction)

        return float(prediction)
    except Exception as e:
        st.error(f"Prediction failed: {str(e)}")
        return 0.0
