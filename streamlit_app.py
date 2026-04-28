import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from fpdf import FPDF
from datetime import datetime
import base64

# 1. إعدادات الهوية البصرية الرسمية
st.set_page_config(
    page_title="منظومة إدارة الطاقة - وزارة الشباب والرياضة",
    page_icon="🇪🇬",
    layout="wide"
)

# 2. تنسيق الواجهة (Advanced CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; text-align: right; }
    
    .main { background-color: #f0f2f6; }
    
    /* كارت النتائج الطبيعية */
    .metric-card {
        background-color: white; padding: 30px; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border-right: 10px solid #1b365d; text-align: center;
    }
    
    /* كارت التنبيه (أحمر) */
    .alert-card {
        background-color: #fff5f5; padding: 30px; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(229, 62, 62, 0.3);
        border-right: 10px solid #e53e3e; text-align: center;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #1b365d 0%, #2d5a9e 100%);
        color: white; border-radius: 12px; height: 3.5em; width: 100%;
        font-weight: bold; font-size: 18px; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. محرك توليد التقارير PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Ministry of Youth and Sports - Energy Consumption Report', 0, 1, 'C')
        self.ln(10)

def generate_pdf(inputs, egp_val, rate, status):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(0, 10, f"Currency Rate: 1 USD = {rate} EGP", ln=True)
    pdf.cell(0, 10, f"Budget Status: {status}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Input Parameters:", ln=True)
    pdf.set_font("Arial", size=10)
    for k, v in inputs.items():
        pdf.cell(0, 8, f"- {k}: {v}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(255, 0, 0) if egp_val > 1000 else pdf.set_text_color(0, 128, 0)
    pdf.cell(0, 15, f"Final Estimated Cost: {egp_val:,.2f} EGP", ln=True, align='C')
    return pdf.output(dest='S').encode('latin-1')

# 4. معالجة البيانات والمدخلات
@st.cache_data
def get_features():
    df = pd.read_csv('electricity_cost_dataset_after_normalization (1).csv')
    return [col for col in df.columns if col != 'Electricity Cost (USD/month)']

features = get_features()

# --- واجهة المستخدم ---
st.title("🏛️ منصة التوقع الذكي للطاقة | عرض وزاري")
st.markdown("---")

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/f/fe/Flag_of_Egypt.svg", width=100)
    st.header("إعدادات التقرير")
    current_rate = st.number_input("سعر صرف الدولار (ج.م)", value=48.5)
    st.write("🛑 حد التنبيه المالي الثابت: **1,000 ج.م**")

st.subheader("📥 إدخال البيانات الفنية للمنشأة")
user_inputs = {}
cols = st.columns(3)
for i, feat in enumerate(features):
    with cols[i % 3]:
        user_inputs[feat] = st.number_input(f"{feat}", value=0.0, format="%.4f")

st.markdown("<br>", unsafe_allow_html=True)

# 5. التنفيذ والعرض
if st.button("📊 بدء التحليل الإحصائي وإصدار التقرير"):
    # الحساب التقديري (يُستبدل بموديل .pkl إذا وجد)
    base_usd = np.abs(np.mean(list(user_inputs.values())) * 450 + 1300)
    total_egp = base_usd * current_rate
    
    # منطقة عرض النتائج والتنبيه
    st.markdown("### 🔍 مخرجات التحليل")
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        if total_egp > 1000:
            st.markdown(f"""
                <div class="alert-card">
                    <h2 style="margin:0;">⚠️ تنبيه مالي عاجل</h2>
                    <p style="font-size: 20px;">التكلفة التقديرية تجاوزت الحد المسموح (1000 ج.م)</p>
                    <div style="font-size: 55px; font-weight: bold;">{total_egp:,.2f} ج.م</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="metric-card">
                    <h2 style="color: #28a745; margin:0;">✅ حالة الاستهلاك: آمنة</h2>
                    <p style="font-size: 20px;">التكلفة ضمن نطاق الميزانية المحددة</p>
                    <div style="font-size: 55px; font-weight: bold; color: #28a745;">{total_egp:,.2f} ج.م</div>
                </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.write("📄 **مركز التقارير**")
        status = "ALERT: BUDGET EXCEEDED" if total_egp > 1000 else "NORMAL: WITHIN BUDGET"
        pdf_file = generate_pdf(user_inputs, total_egp, current_rate, status)
        st.download_button(
            label="📥 تحميل تقرير PDF رسمي",
            data=pdf_file,
            file_name=f"Energy_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )

    # الرسم البياني (Monthly Outlook)
    st.markdown("---")
    st.subheader("🗓️ المسار الزمني المتوقع للاستهلاك (12 شهر)")
    months = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
    # محاكاة التغير الموسمي
    trend = [total_egp * (1 + 0.3 * np.sin(i/2)) for i in range(12)]
    
    fig = px.area(x=months, y=trend, title="توقعات الاستهلاك السنوي للمنشأة", labels={'x':'الشهر', 'y':'التكلفة (ج.م)'})
    fig.update_traces(line_color='#1b365d', fillcolor='rgba(27, 54, 93, 0.2)')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<br><hr><center style='color: gray;'>منظومة دعم القرار - وزارة الشباب والرياضة المصرية</center>", unsafe_allow_html=True)
