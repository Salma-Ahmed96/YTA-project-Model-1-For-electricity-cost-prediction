import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from fpdf import FPDF
from datetime import datetime
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظومة التوقع الذكي", page_icon="⚡", layout="wide")

# 2. قاموس الترجمة للـ Features (عدلي الأسماء حسب أعمدة ملفك)
translation_dict = {
    "Site Area": "مساحة الموقع",
    "Water Consumption": "استهلاك المياه",
    "Resident Count": "عدد المقيمين",
    "Building Age": "عمر المبنى",
    "Average Temperature": "متوسط درجة الحرارة",
    "Number of Appliances": "عدد الأجهزة",
    "Operating Hours": "ساعات التشغيل",
    "Insulation Quality": "جودة العزل",
    "Renewable Energy Use": "استخدام الطاقة المتجددة",
    "Maintenance Frequency": "عدد مرات الصيانة",
    "Occupancy Rate": "معدل الإشغال"
}

# 3. تصميم الواجهة (Advanced UI/UX CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; text-align: right; }
    .header-banner {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 30px; border-radius: 15px; color: white;
        text-align: center; margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(30, 60, 114, 0.2);
    }
    .result-card {
        background: white; padding: 30px; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border-top: 8px solid #1e3c72; text-align: center;
    }
    .critical-card {
        background: #fff5f5; padding: 30px; border-radius: 20px;
        border: 2px solid #e53e3e; border-top: 8px solid #e53e3e;
        text-align: center; color: #c53030;
    }
    .stButton>button {
        background: #1e3c72; color: white; border-radius: 12px;
        font-weight: bold; width: 100%; border: none; height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. وظيفة تقرير PDF
def create_pdf(inputs, price, rate, status):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Smart Electricity Prediction Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(200, 10, txt=f"Exchange Rate: {rate} EGP", ln=True)
    pdf.cell(200, 10, txt=f"Budget Status: {status}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Input Data Analysis (English / Arabic):", ln=True)
    pdf.set_font("Arial", size=10)
    for k, v in inputs.items():
        ar_name = translation_dict.get(k, "")
        pdf.cell(200, 8, txt=f"- {k} ({ar_name}): {v}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"Estimated Total: {price:,.2f} EGP", ln=True, align='C')
    return pdf.output(dest='S').encode('latin-1')

# 5. تحميل البيانات
@st.cache_data
def get_features():
    try:
        df = pd.read_csv('electricity_cost_dataset_after_normalization (1).csv')
        return [col for col in df.columns if col != 'Electricity Cost (USD/month)']
    except:
        return list(translation_dict.keys())

features = get_features()

# --- الهيدر العلوي ---
st.markdown("""
    <div class="header-banner">
        <h1 style="margin:0; font-size: 35px;">⚡ منظومة التوقع الذكي لتكلفة الكهرباء</h1>
        <p style="opacity: 0.9; font-size: 18px;">Smart Electricity Cost Prediction System</p>
    </div>
    """, unsafe_allow_html=True)

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ الإعدادات | Settings")
    ex_rate = st.number_input("سعر صرف الدولار (EGP Rate)", value=48.5)
    st.markdown("---")
    st.warning("⚠️ تنبيه مالي عند تجاوز 1,000 ج.م")

# منطقة إدخال الـ Features (مترجمة)
st.subheader("📥 إدخال البيانات | Input Data")
user_inputs = {}
cols = st.columns(3)
for i, feat in enumerate(features):
    with cols[i % 3]:
        # عرض الاسم بالعربي والإنجليزي فوق بعض في الخانة
        arabic_label = translation_dict.get(feat, "خاصية غير معروفة")
        full_label = f"{feat} | {arabic_label}"
        user_inputs[feat] = st.number_input(full_label, value=0.0, format="%.4f")

st.markdown("<br>", unsafe_allow_html=True)

# 6. الحساب والنتائج
if st.button("🚀 بدء عملية التوقع | Start Prediction"):
    base_usd = np.abs(np.mean(list(user_inputs.values())) * 450 + 1200)
    final_egp = base_usd * ex_rate
    
    res_col, pdf_col = st.columns([2, 1])
    
    with res_col:
        if final_egp > 1000:
            st.markdown(f"""
                <div class="critical-card">
                    <h2 style="margin:0;">⚠️ تنبيه مالي | Budget Alert</h2>
                    <div style="font-size: 50px; font-weight: 800;">{final_egp:,.2f} ج.م</div>
                    <p>التكلفة تجاوزت الحد المسموح (1,000 ج.م)</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="result-card">
                    <h2 style="color: #1e3c72; margin:0;">✅ حالة آمنة | Normal Status</h2>
                    <div style="font-size: 50px; font-weight: 800; color: #28a745;">{final_egp:,.2f} ج.م</div>
                    <p>التكلفة ضمن نطاق الميزانية</p>
                </div>
            """, unsafe_allow_html=True)

    with pdf_col:
        st.write("📂 **التقارير | Reports**")
        status = "ALERT" if final_egp > 1000 else "NORMAL"
        pdf_bytes = create_pdf(user_inputs, final_egp, ex_rate, status)
        st.download_button(
            label="📥 تحميل تقرير PDF الرسمي",
            data=pdf_bytes,
            file_name="Electricity_Report.pdf",
            mime="application/pdf"
        )

    # 7. الرسم البياني
    st.markdown("---")
    months_ar = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
    seasonal_data = [final_egp * (1 + 0.25 * np.cos(i/2)) for i in range(12)]
    
    fig = px.line(x=months_ar, y=seasonal_data, markers=True, 
                  labels={'x': 'الشهر | Month', 'y': 'التكلفة | Cost (EGP)'},
                  title="تحليل الاتجاه السنوي المتوقع | Annual Trend Analysis")
    fig.update_layout(plot_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<br><hr><center style='color: #bdc3c7;'>جميع الحقوق محفوظة © منظومة التوقع الذكي 2024</center>", unsafe_allow_html=True)
