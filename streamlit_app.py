import streamlit as st
import pandas as pd
import numpy as np

# 1. إعدادات واجهة المستخدم
st.set_page_config(page_title="حاسبة تكلفة الكهرباء - مصر", page_icon="🇪🇬", layout="wide")

# تصميم مخصص (CSS) لجعل النتيجة بالجنيه المصري واضحة جداً
st.markdown("""
    <style>
    .stNumberInput label { font-weight: bold; color: #1e3c72; }
    .main-result {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        padding: 40px;
        border-radius: 25px;
        color: white;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin-top: 30px;
    }
    .currency-label { font-size: 24px; font-weight: normal; }
    .price-value { font-size: 60px; font-weight: 800; display: block; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# 2. تحميل أسماء الـ Features فقط
@st.cache_data
def get_features_list():
    df = pd.read_csv('electricity_cost_dataset_after_normalization (1).csv')
    return [col for col in df.columns if col != 'Electricity Cost (USD/month)']

features = get_features_list()

# 3. العنوان الرئيسي
st.title("🇪🇬 حاسبة تكلفة الكهرباء التقديرية")
st.write("أدخلي البيانات أدناه واحصلي على التكلفة فوراً بالجنيه المصري.")

# 4. منطقة إدخال البيانات (التحكم الكامل لكِ)
st.markdown("### 🛠️ خطوة 1: إدخال بيانات الموقع (Features)")
user_data = {}

# توزيع الـ 10 أعمدة على صفين بشكل منظم
col_group1 = st.columns(5)
col_group2 = st.columns(5)

for i, feature in enumerate(features):
    target_col = col_group1[i] if i < 5 else col_group2[i-5]
    with target_col:
        user_data[feature] = st.number_input(f"{feature}", value=0.0, format="%.4f")

st.markdown("---")

# 5. منطقة سعر الصرف (ديناميكي)
st.markdown("### 💰 خطوة 2: تحديد سعر الصرف")
rate_col, _ = st.columns([1, 3])
with rate_col:
    exchange_rate = st.number_input("سعر الدولار مقابل الجنيه:", value=48.50, step=0.10)

# 6. زر الحساب والنتيجة النهائية
st.markdown("<br>", unsafe_allow_html=True)
if st.button("✨ احسب التكلفة النهائية بالجنيه المصري"):
    
    # عملية الحساب (استبدلي هذه المعادلة بـ model.predict لو عندك موديل جاهز)
    # الحسبة هنا تعتمد على القيم الـ Normalized التي تدخلينها
    raw_prediction_usd = np.abs(sum(user_data.values()) * 100 + 2000) 
    
    # التحويل للجنيه المصري
    final_price_egp = raw_prediction_usd * exchange_rate

    # عرض النتيجة بشكل ضخم ومبهر
    st.markdown(f"""
        <div class="main-result">
            <span class="currency-label">التكلفة المتوقعة هي</span>
            <span class="price-value">{final_price_egp:,.2f} ج.م</span>
            <p>تم الحساب بناءً على سعر صرف {exchange_rate} جنيه للدولار</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.balloons()

# تذييل الصفحة
st.markdown("<center style='color: #999;'><br>نظام التوقع يعتمد على القيم المعيارية (Normalized Values)</center>", unsafe_allow_html=True)
