import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from fpdf import FPDF
from datetime import datetime
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظومة توقع تكلفة الكهرباء", page_icon="⚡", layout="wide")

# 2. قاموس التعريب الكامل (كل البيانات بالعربي)
# ملاحظة: تأكدي أن هذه الأسماء هي نفسها الموجودة في ملف الـ CSV الخاص بك
translation_dict = {
    "Site Area": "مساحة الموقع (متر مربع)",
    "Water Consumption": "معدل استهلاك المياه",
    "Resident Count": "عدد السكان / المقيمين",
    "Building Age": "عمر المبنى (سنوات)",
    "Average Temperature": "متوسط درجة الحرارة المحيطة",
    "Number of Appliances": "إجمالي عدد الأجهزة الكهربائية",
    "Operating Hours": "ساعات التشغيل اليومية",
    "Insulation Quality": "جودة عزل المبنى",
    "Renewable Energy Use": "نسبة الاعتماد على الطاقة المتجددة",
    "Maintenance Frequency": "معدل إجراء الصيانة",
    "Occupancy Rate": "نسبة إشغال المبنى"
}

# 3. التنسيق الجمالي (CSS) - يدعم الكتابة من اليمين لليسار
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    
    .main { background-color: #f0f2f6; }
    
    /* الهيدر العلوي */
    .header-banner {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 40px; border-radius: 20px; color: white;
        text-align: center; margin-bottom: 35px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }

    /* كارت النتائج */
    .metric-card {
        background: white; padding: 30px; border-radius: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        border-right: 12px solid #1e3c72; text-align: center;
    }
    
    /* كارت التحذير بالأحمر */
    .warning-card {
        background: #fff5f5; padding: 30px; border-radius: 20px;
        border: 2px solid #ff4b4b; border-right: 12px solid #ff4b4b;
        text-align: center; color: #ff4b4b;
    }

    .stButton>button {
        background: #1e3c72; color: white; border-radius: 12px;
        font-weight: bold; width: 100%; border: none; height: 3.8em;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. وظيفة تقرير PDF (ملاحظة: الـ PDF يدعم الإنجليزية لتجنب مشاكل الخطوط، لكن سأكتب النتائج بوضوح)
def create_pdf(inputs, price, rate, status):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Electricity Cost Analysis Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(200, 10, txt=f"Status: {status}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"Total Cost: {price:,.2f} EGP", ln=True, align='C')
    return pdf.output(dest='S').encode('latin-1')

# 5. جلب البيانات
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
        <p style="opacity: 0.9; font-size: 20px; margin-top:10px;">لوحة تحليل استهلاك الطاقة وإدارة التكاليف</p>
    </div>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ الإعدادات")
    ex_rate = st.number_input("سعر صرف الدولار الحالي", value=48.5)
    st.markdown("---")
    st.error("🛑 تنبيه: الحد الأقصى للميزانية 1,000 ج.م")

st.subheader("📥 يرجى إدخال بيانات الاستهلاك:")
user_inputs = {}
cols = st.columns(3)

for i, feat in enumerate(features):
    with cols[i % 3]:
        # نستخدم الاسم العربي من القاموس
        arabic_label = translation_dict.get(feat, feat)
        user_inputs[feat] = st.number_input(arabic_label, value=0.0, format="%.4f")

st.markdown("<br>", unsafe_allow_html=True)

# 6. المعالجة والعرض
if st.button("📊 بدء التحليل وحساب التكلفة"):
    # الحساب (تقديري بناءً على النورماليزيشن)
    base_usd = np.abs(np.mean(list(user_inputs.values())) * 450 + 1200)
    final_egp = base_usd * ex_rate
    
    col_res, col_pdf = st.columns([2, 1])
    
    with col_res:
        if final_egp > 1000:
            st.markdown(f"""
                <div class="warning-card">
                    <h2 style="margin:0;">⚠️ تنبيه: الاستهلاك يتجاوز الحد المسموح</h2>
                    <div style="font-size: 60px; font-weight: 800; margin:10px 0;">{final_egp:,.2f} ج.م</div>
                    <p style="font-size: 18px;">القيمة الحالية أعلى من ميزانية الـ 1,000 جنيه</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="metric-card">
                    <h2 style="color: #1e3c72; margin:0;">✅ حالة الاستهلاك: طبيعية</h2>
                    <div style="font-size: 60px; font-weight: 800; color: #28a745; margin:10px 0;">{final_egp:,.2f} ج.م</div>
                    <p style="font-size: 18px; color: #555;">التكلفة تقع ضمن النطاق المالي الآمن</p>
                </div>
            """, unsafe_allow_html=True)

    with col_pdf:
        st.write("📂 **مركز التقارير**")
        status = "CRITICAL" if final_egp > 1000 else "NORMAL"
        pdf_bytes = create_pdf(user_inputs, final_egp, ex_rate, status)
        st.download_button(
            label="📥 تحميل تقرير التكلفة (PDF)",
            data=pdf_bytes,
            file_name="تقرير_تكلفة_الكهرباء.pdf",
            mime="application/pdf"
        )

    # 7. الرسم البياني (معرب)
    st.markdown("---")
    months = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', '
