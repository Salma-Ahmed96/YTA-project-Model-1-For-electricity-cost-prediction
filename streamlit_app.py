import streamlit as st
import joblib
import numpy as np

# تحميل الميزان والموديل بالأسماء اللي عندك في الـ GitHub
scaler = joblib.load('scaler.joblib')
model = joblib.load('mlp_doubled_neurons_model.joblib')

st.title("Electricity Cost Prediction ⚡")

# خانة الإدخال
input_val = st.number_input("Enter consumption value:")

if st.button("Predict"):
    # تحويل الرقم لمصفوفة
    input_data = np.array([[input_val]])
    
    # استخدام الميزان ثم التوقع
    input_data_scaled = scaler.transform(input_data)
    prediction = model.predict(input_data_scaled)
    
    st.success(f"The predicted cost is: {prediction[0]}")
