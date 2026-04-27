import streamlit as st
import joblib
import numpy as np

# تحميل الموديل فقط
try:
    model = joblib.load('mlp_doubled_neurons_model.joblib')
    st.success("Model loaded successfully!")
except:
    st.error("Model file not found.")

st.title("Electricity Cost Prediction ⚡")

input_val = st.number_input("Enter your input value:", value=0.0)

if st.button("Predict"):
    try:
        # هندخل الرقم للموديل مباشرة ونشوف هيقول إيه
        # لو الموديل محتاج أكتر من رقم، الكود ده هيجرب يدخله كـ array
        input_data = np.array([[input_val]])
        
        # التوقع
        prediction = model.predict(input_data)
        
        st.write(f"### Prediction Result: {prediction[0]}")
    except Exception as e:
        st.error(f"Prediction error: {e}")
        st.info("نصيحة: الموديل ده غالباً محتاج أكتر من معلومة عشان يتوقع صح.")
