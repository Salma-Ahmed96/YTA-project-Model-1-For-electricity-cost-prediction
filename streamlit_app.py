import streamlit as st
import pandas as pd
import numpy as np

# 1. إعداد الصفحة
st.set_page_config(page_title="Electricity Cost Predictor", layout="wide")

# 2. تحميل البيانات لمعرفة أسماء الأعمدة ونطاق القيم
@st.cache_data
def load_data():
    return pd.read_csv('electricity_cost_dataset_after_normalization (1).csv')

df = load_data()

# استخراج أسماء الـ Features (كل الأعمدة ما عدا عمود التكلفة)
target_column = 'Electricity Cost (USD/month)'
features = [col for col in df.columns if col != target_column]

st.title("⚡ نظام توقع تكلفة الكهرباء")
st.write("قم بتعديل قيم الخصائص في القائمة الجانبية للحصول على التكلفة المتوقعة.")

# 3. إنشاء خانات الإدخال (Inputs) في القائمة الجانبية
st.sidebar.header("📥 أدخل بيانات الـ Features")

user_inputs = {}
for col in features:
    # إنشاء Slider لكل عمود بناءً على القيم المتاحة في الداتا
    user_inputs[col] = st.sidebar.slider(
        label=f"{col}",
        min_value=float(df[col].min()),
        max_value=float(df[col].max()),
        value=float(df[col].mean()), # القيمة الافتراضية هي المتوسط
        help=f"حدد قيمة {col}"
    )

# 4. تحويل المدخلات إلى مصفوفة للحساب
input_df = pd.DataFrame([user_inputs])

# 5. قسم عرض النتائج
st.markdown("---")
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 القيم التي قمت بإدخالها:")
    st.table(input_df)

with col2:
    st.subheader("💰 التكلفة المتوقعة")
    
    # ملاحظة: هنا يجب وضع موديل الذكاء الاصطناعي الخاص بك (مثلاً ملف .pkl)
    # كحل مؤقت للحساب سأستخدم معادلة افتراضية تعتمد على المدخلات:
    # في مشروعك الحقيقي استبدلي السطر القادم بـ model.predict(input_df)
    
    # مثال لحسبة بسيطة (Linear Combination):
    prediction = np.sum(list(user_inputs.values())) * 100 + 2000 
    
    st.success(f"### ${prediction:,.2f}")
    st.write("هذه القيمة بناءً على المدخلات الـ Normalized.")

# 6. قسم إحصائي بسيط
with st.expander("إظهار تفاصيل الـ Features في قاعدة البيانات"):
    st.write(df[features].describe())
