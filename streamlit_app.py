
import tensorflow as tf
import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization

def load_and_predict(input_data):
    # Load the scaler
    scaler = joblib.load('scaler.joblib')

    # Define the model architecture (must match the trained model)
    model = Sequential([
        Dense(256, activation='relu', input_shape=(10,)),
        BatchNormalization(),
        Dense(128, activation='relu'),
        BatchNormalization(),
        Dense(64, activation='relu'),
        BatchNormalization(),
        Dense(1)
    ])

    # Load the model weights
    # Use custom_objects if you have custom layers/activations, not needed here
    model.load_weights('mlp_doubled_neurons_model.keras')

    # Preprocess the input data using the loaded scaler
    # Ensure input_data is a DataFrame with the correct column order
    input_df = pd.DataFrame([input_data], columns=['Site Area (square meters)', 'Water Consumption (liters/day)', 'Recycling Rate (%)', 'Utilisation Rate (%)', 'Air Quality Index (AQI)', 'Issue Resolution Time (hours)', 'Resident Count (number of people)', 'Structure Type_Industrial', 'Structure Type_Mixed-use', 'Structure Type_Residential'])
    scaled_input_data = scaler.transform(input_df)

    # Make prediction
    prediction = model.predict(scaled_input_data)
    return prediction[0][0]

if __name__ == '__main__':
    # Example usage (replace with actual input from Streamlit)
    # The order of features must match the training data
    sample_input = np.array([
        1360,  # 'Site Area (square meters)'
        2519.0, # 'Water Consumption (liters/day)'
        68,     # 'Recycling Rate (%)'
        59,     # 'Utilisation Rate (%)'
        51,     # 'Air Quality Index (AQI)'
        34,     # 'Issue Resolution Time (hours)'
        6,      # 'Resident Count (number of people)'
        False,  # 'Structure Type_Industrial'
        True,   # 'Structure Type_Mixed-use'
        False   # 'Structure Type_Residential'
    ])

    predicted_cost = load_and_predict(sample_input)
    print(f"Predicted Electricity Cost: {predicted_cost:.2f} USD/month")

