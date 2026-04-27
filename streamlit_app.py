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
        # الموديل طلع محتاج 10 مدخلات بالظبط
        input_data = np.zeros((1, 10)) 
        input_data[0, 0] = input_val
        
        prediction = model.predict(input_data)
        
        # عرض النتيجة
        st.write(f"### Predicted Electricity Cost: {prediction[0][0]:.2f}")
    except Exception as e:
        # لو لسه فيه مشكلة في العدد، الكود ده هيقولنا العدد الصح كام
        st.error(f"Try once more, it's almost there!")
        st.info(f"Technical detail: {e}")
