import streamlit as st
import pandas as pd
import io

# إعداد الصفحة لتكون واسعة
st.set_page_config(page_title="Data Properties Explorer", layout="wide")

st.title("🔍 خصائص وتحليل بيانات الكهرباء")

# 1. تحميل الملف
try:
    df = pd.read_csv('electricity_cost_dataset_after_normalization (1).csv')
    
    # صفوف لعرض المعلومات بشكل منظم
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("عدد الأعمدة (Features)", df.shape[1])
    with col2:
        st.metric("عدد السجلات (Rows)", df.shape[0])
    with col3:
        st.metric("القيم المفقودة", df.isnull().sum().sum())

    st.markdown("---")

    # 2. عرض أسماء الأعمدة وأنواعها (Data Types)
    st.subheader("1️⃣ أسماء الأعمدة ونوع البيانات")
    # لتحويل مخرجات df.info() لنص يمكن عرضه في Streamlit
    buffer = io.StringIO()
    df.info(buf=buffer)
    st.text(buffer.getvalue())

    st.markdown("---")

    # 3. الإحصاءات الوصفية (Statistical Summary)
    st.subheader("2️⃣ الملخص الإحصائي (الوصف)")
    st.write("هذا الجدول يوضح (المتوسط الحسابي، الانحراف المعياري، أقل وأكبر قيمة) لكل Feature:")
    st.dataframe(df.describe())

    st.markdown("---")

    # 4. فحص القيم الفريدة (Unique Values)
    st.subheader("3️⃣ فحص التكرار والقيم الفريدة")
    selected_col = st.selectbox("اختار عمود لعرض عدد القيم الفريدة فيه:", df.columns)
    st.write(f"عدد القيم الفريدة في {selected_col} هو: {df[selected_col].nunique()}")
    
    st.markdown("---")

    # 5. عرض عينة من الداتا الحقيقية
    st.subheader("4️⃣ عرض عينة من البيانات (أول 10 صفوف)")
    st.table(df.head(10))

except FileNotFoundError:
    st.error("❌ لم يتم العثور على ملف CSV. تأكدي من تسميته بشكل صحيح ووضعه بجانب ملف الكود.")
