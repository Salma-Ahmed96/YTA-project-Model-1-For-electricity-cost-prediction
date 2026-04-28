import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from fpdf import FPDF
from datetime import datetime
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظومة التوقع الذكي", page_icon="⚡", layout="wide")

# 2. قاموس الترجمة الاحترافي
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

# 3. التنسيق الجمالي المطور (Modern Professional CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; text-align: right; }
    
    .main { background-color: #f0f2f6; }
    
    /* الهيدر العلوي الفخم */
    .header-banner {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 40px; border-radius: 20px; color: white;
        text-align: center; margin-bottom: 35px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }

    /* كروت النتائج */
    .metric-card {
        background: white; padding: 30px; border-radius: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        border-right: 12px solid #1e3c72; text-align: center;
    }
    
    /* كارت التحذير بالأحمر الصريح */
    .warning-card {
        background: #fff5f5; padding: 30px; border-radius: 20px;
        border: 2px solid #ff4b4b; border-right: 12px solid #ff4b4b;
        text-align: center; color: #ff4b4b;
    }

    .stButton>button {
        background: #1e3c72; color: white; border-radius: 12px;
        font-weight: bold; width: 100%; border: none; height: 3.8em;
        transition: 0.3s; font-size: 18px;
    }
    .stButton>button:hover { background: #2a5298; transform: scale(1.01); }
    </style>
    """, unsafe_allow_html=True)

# 4. محرك الـ PDF
def create_pdf(inputs, price, rate, status):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Electricity Cost Prediction Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(200, 10, txt=f"Exchange Rate: {rate} EGP", ln=True)
    pdf.cell(200, 10, txt=f"Financial Status: {status}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Input Features Data:", ln=True)
    pdf.set_font("Arial", size=10)
    for k, v in inputs.items():
        pdf.cell(200, 8, txt=f"- {k}: {v}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"Estimated Total: {price:,.2f} EGP", ln=True, align='C')
    return pdf.output(dest='S').encode('latin-1')

# 5. معالجة الخصائص
@st.cache_data
def get_features():
    try:
        df = pd.read_csv('electricity_cost_dataset_after_normalization (1).csv')
        return [col for col in df.columns if col != 'Electricity Cost (USD/month)']
    except:
        return list(translation_dict.keys())

features = get_features()

# --- واجهة المستخدم ---
st.markdown("""
    <div class="header-banner">
        <h1 style="margin:0; font-size: 38px; font-weight: 800;">⚡ منظومة التوقع الذكي لتكلفة الكهرباء</h1>
        <p style="opacity: 0.9; font-size: 20px; margin-top:10px;">Smart Energy Cost Analysis Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ إعدادات الحساب")
    ex_rate = st.number_input("سعر صرف الدولار (ج.م)", value=48.5)
    st.markdown("---")
    st.error("🛑 تنبيه مالي: الحد الأقصى 1,000 ج.م")

st.subheader("📥 إدخال البيانات (الخصائص)")
user_inputs = {}
cols = st.columns(3)
for i, feat in enumerate(features):
    with cols[i % 3]:
        # عرض العربي والانجليزي أو الانجليزي فقط لو مفيش ترجمة
        ar_name = translation_dict.get(feat, "")
        full_label = f"{feat} | {ar_name}" if ar_name else feat
        user_inputs[feat] = st.number_input(full_label, value=0.0, format="%.4f")

st.markdown("<br>", unsafe_allow_html=True)

# 6. النتائج والتحليل
if st.button("📊 بدء التحليل وإصدار النتائج"):
    base_usd = np.abs(np.mean(list(user_inputs.values())) * 450 + 1200)
    final_egp = base_usd * ex_rate
    
    col_res, col_pdf = st.columns([2, 1])
    
    with col_res:
        if final_egp > 1000:
            st.markdown(f"""
                <div class="warning-card">
                    <h2 style="margin:0;">⚠️ تنبيه: تجاوز ميزانية الاستهلاك</h2>
                    <div style="font-size: 60px; font-weight: 800; margin:10px 0;">{final_egp:,.2f} ج.م</div>
                    <p style="font-size: 18px;">القيمة المحسوبة تخطت حاجز الـ 1,000 جنيه مصري</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="metric-card">
                    <h2 style="color: #1e3c72; margin:0;">✅ حالة الاستهلاك: آمنة</h2>
                    <div style="font-size: 60px; font-weight: 800; color: #28a745; margin:10px 0;">{final_egp:,.2f} ج.م</div>
                    <p style="font-size: 18px; color: #555;">التكلفة التقديرية ضمن الحدود المالية المسموحة</p>
                </div>
            """, unsafe_allow_html=True)

    with col_pdf:
        st.write("📂 **إصدار التقارير الرقمية**")
        status = "CRITICAL" if final_egp > 1000 else "NORMAL"
        pdf_bytes = create_pdf(user_inputs, final_egp, ex_rate, status)
        st.download_button(
            label="📥 تحميل تقرير PDF الرسمي",
            data=pdf_bytes,
            file_name="Cost_Prediction_Report.pdf",
            mime="application/pdf"
        )

    # 7. الرسم البياني
    st.markdown("---")
    months = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
    seasonal_data = [final_egp * (1 + 0.2 * np.cos(i/1.5)) for i in range(12)]
    
    fig = px.area(x=months, y=seasonal_data, markers=True, 
                  labels={'x': 'الشهر', 'y': 'التكلفة (ج.م)'},
                  title="تحليل المسار الزمني المتوقع للاستهلاك")
    fig.update_traces(line_color='#1e3c72', fillcolor='rgba(30, 60, 114, 0.1)')
    fig.update_layout(plot_bgcolor='white', font=dict(family="Cairo"))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<br><hr><center style='color: #bdc3c7;'>جميع الحقوق محفوظة © منظومة التوقع الذكي 2024</center>", unsafe_allow_html=True)
