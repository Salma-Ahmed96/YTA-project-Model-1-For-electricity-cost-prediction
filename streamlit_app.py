import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from fpdf import FPDF
from datetime import datetime
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظومة التوقع الذكي", page_icon="⚡", layout="wide")

# 2. القاموس العربي للبيانات
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

# 3. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .header-banner { 
        background: linear-gradient(135deg, #0f2027, #2c5364); 
        padding: 40px; border-radius: 20px; color: white; 
        text-align: center; margin-bottom: 30px; 
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .warning-card { 
        background: #fff5f5; padding: 30px; border-radius: 20px; 
        border: 2px solid #ff4b4b; text-align: center; color: #ff4b4b; 
    }
    .metric-card { 
        background: white; padding: 30px; border-radius: 20px; 
        box-shadow: 0 8px 20px rgba(0,0,0,0.08); 
        border-right: 12px solid #1e3c72; text-align: center; 
    }
    .stButton>button {
        background: #1e3c72; color: white; border-radius: 12px;
        font-weight: bold; width: 100%; border: none; height: 3.5em; font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. وظيفة إنشاء ملف PDF
def create_pdf(inputs, price, rate, status):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Electricity Cost Prediction Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(200, 10, txt=f"Financial Status: {status}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Input Data Summary:", ln=True)
    pdf.set_font("Arial", size=10)
    for k, v in inputs.items():
        pdf.cell(200, 8, txt=f"- {k}: {v}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"Total Estimated Cost: {price:,.2f} EGP", ln=True, align='C')
    return pdf.output(dest='S').encode('latin-1')

# 5. محاولة جلب البيانات
try:
    df_temp = pd.read_csv('electricity_cost_dataset_after_normalization (1).csv')
    features = [col for col in df_temp.columns if col != 'Electricity Cost (USD/month)']
except:
    features = list(translation_dict.keys())

# --- الهيدر العلوي ---
st.markdown('<div class="header-banner"><h1>⚡ منظومة التوقع الذكي لتكلفة الكهرباء</h1><p>لوحة تحكم تحليل وإدارة الطاقة</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ الإعدادات")
    ex_rate = st.number_input("سعر صرف الدولار (ج.م)", value=48.5)
    st.markdown("---")
    st.error("🛑 تنبيه مالي: الحد 1,000 ج.م")

# منطقة الإدخال
st.subheader("📥 يرجى إدخال بيانات الاستهلاك:")
user_inputs = {}
cols = st.columns(3)
for i, feat in enumerate(features):
    with cols[i % 3]:
        label = translation_dict.get(feat, feat)
        user_inputs[feat] = st.number_input(label, value=0.0, format="%.4f")

st.markdown("<br>", unsafe_allow_html=True)

# 6. الحساب والعرض (التحليل)
if st.button("📊 بدء التحليل وحساب التكلفة"):
    # حساب تقديري
    base_usd = np.abs(np.mean(list(user_inputs.values())) * 450 + 1200)
    final_egp = base_usd * ex_rate
    
    col_res, col_pdf = st.columns([2, 1])
    
    with col_res:
        if final_egp > 1000:
            st.markdown(f"""
                <div class="warning-card">
                    <h2>⚠️ تنبيه: تجاوز ميزانية الاستهلاك</h2>
                    <div style="font-size: 50px; font-weight: 800;">{final_egp:,.2f} ج.م</div>
                    <p>هذه القيمة أعلى من الحد المسموح به</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="metric-card">
                    <h2 style="color: #1e3c72;">✅ حالة الاستهلاك: آمنة</h2>
                    <div style="font-size: 50px; font-weight: 800; color: #28a745;">{final_egp:,.2f} ج.م</div>
                </div>
            """, unsafe_allow_html=True)

    with col_pdf:
        st.write("📂 **تحميل التقرير**")
        status_txt = "OVER BUDGET" if final_egp > 1000 else "NORMAL"
        pdf_data = create_pdf(user_inputs, final_egp, ex_rate, status_txt)
        st.download_button(
            label="📥 تحميل تقرير PDF",
            data=pdf_data,
            file_name="تقرير_تكلفة_الكهرباء.pdf",
            mime="application/pdf"
        )

    # 7. الرسم البياني للاستهلاك الشهري (تم تصحيح الشهور)
    st.markdown("---")
    st.subheader("🗓️ المسار الزمني المتوقع للاستهلاك (12 شهر)")
    
    # قائمة الشهور المصححة بدون أخطاء Syntax
    months_ar = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
    
    # محاكاة بيانات شهرية
    monthly_trend = [final_egp * (1 + 0.2 * np.cos(i/1.5)) for i in range(12)]
    
    fig = px.area(x=months_ar, y=monthly_trend, markers=True, 
                  labels={'x': 'الشهر', 'y': 'التكلفة التقديرية (ج.م)'},
                  title="توقع تغير التكلفة على مدار العام")
    fig.update_traces(line_color='#1e3c72', fillcolor='rgba(30, 60, 114, 0.1)')
    fig.update_layout(plot_bgcolor='white', font=dict(family="Cairo"))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<br><hr><center style='color: #bdc3c7;'>جميع الحقوق محفوظة © منظومة التوقع الذكي 2024</center>", unsafe_allow_html=True)
