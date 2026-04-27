import streamlit as st
import joblib
import numpy as np

# تحميل الموديل
model = joblib.load('mlp_doubled_neurons_model.joblib')

st.title("Electricity Cost Prediction ⚡")
st.success("Model loaded successfully!")

input_val = st.number_input("Enter your consumption value:", value=0.0)

if st.button("Predict"):
    try:
        # الموديل محتاج 11 قيمة، هنبعت له الرقم بتاعك ومعاه 10 أصفار كمثال
        # عشان يقبل الـ Shape بتاع الداتا
        input_data = np.zeros((1, 11)) 
        input_data[0, 0] = input_val # بنحط الرقم بتاعك في أول خانة
        
        prediction = model.predict(input_data)
        
        # عرض النتيجة
        st.write(f"### Predicted Electricity Cost: {prediction[0]:.2f}")
    except Exception as e:
        st.error(f"Error: {e}")
