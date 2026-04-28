import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from fpdf import FPDF
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظومة التوقع الذكي", page_icon="⚡", layout="wide")

# 2. القاموس العربي
translation_dict = {
    "Site Area": "مساحة الموقع",
    "Water Consumption": "استهلاك المياه",
    "Resident Count": "عدد السكان",
    "Building Age": "عمر المبنى",
    "Average Temperature": "درجة الحرارة",
    "Number of Appliances": "عدد الأجهزة",
    "Operating Hours": "ساعات التشغيل",
    "Insulation Quality": "جودة العزل",
    "Renewable Energy Use": "الطاقة المتجددة",
    "Maintenance Frequency": "عدد الصيانات",
    "Occupancy Rate": "معدل الإشغال"
}

# 3. التصميم
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .header-banner { background: linear-gradient(135deg, #0f2027, #2c5364); padding: 30px; border-radius: 20px; color: white; text-align: center; margin-bottom: 30px; }
    .warning-card { background: #fff5f5; padding: 25px; border-radius: 15px; border: 2px solid #ff4b4b; text-align: center; color: #ff4b4b; }
    .metric-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); border-right: 10px solid #1e3c72; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 4. تحميل البيانات
try:
    df_temp = pd.read_csv('electricity_cost_dataset_after_normalization (1).csv')
    features = [col for col in df_temp.columns if col != 'Electricity Cost (USD/month)']
except:
    features = list(translation_dict.keys())

st.markdown('<div class="header-banner"><h1>⚡ منظومة التوقع الذكي لتكلفة الكهرباء</h1></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ الإعدادات")
    ex_rate = st.number_input("سعر صرف الدولار", value=48.5)

user_inputs = {}
cols = st.columns(3)
for i, feat in enumerate(features):
    with cols[i % 3]:
        label = translation_dict.get(feat, feat)
        user_inputs[feat] = st.number_input(label, value=0.0, format="%.4f")

if st.button("📊 احسب التكلفة الآن"):
    # حساب مبسط للتجربة
    base_usd = np.abs(np.mean(list(user_inputs.values())) * 500 + 1000)
    final_egp = base_usd * ex_rate
    
    if final_egp > 1000:
        st.markdown(f'<div class="warning-card"><h2>⚠️ تنبيه: {final_egp:,.2f} ج.م</h2><p>تجاوزت الميزانية</p></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="metric-card"><h2>✅ التكلفة: {final_egp:,.2f} ج.م</h2></div>', unsafe_allow_html=True)

    # الرسم البياني (هنا التصحيح اللي كان فيه المشكلة)
    st.markdown("---")
    months_list = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
    trend = [final_egp * (1 + 0.1 * np.sin(j)) for j in range(12)]
    fig = px.line(x=months_list, y=trend, title="توقع الاستهلاك السنوي", markers=True)
    st.plotly_chart(fig, use_container_width=True)
