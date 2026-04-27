import streamlit as st
import joblib
import numpy as np

# إعدادات الصفحة (بتخلي شكل الموقع أحلى)
st.set_page_config(page_title="توقع فاتورة الكهرباء", page_icon="⚡")

# تحميل الموديل
try:
    model = joblib.load('mlp_doubled_neurons_model.joblib')
    model_loaded = True
except:
    model_loaded = False

# العنوان الرئيسي
st.title("⚡ برنامج توقع فاتورة الكهرباء")
st.markdown("---")

if model_loaded:
    st.success("✅ النظام جاهز للعمل")
    
    # وصف بسيط
    st.write("أدخل كمية الاستهلاك الشهرية بالكيلو وات لمعرفة التكلفة التقديرية للفاتورة.")

    # خانة إدخال الاستهلاك
    consumption = st.number_input("كمية الاستهلاك (kWh):", min_value=0.0, step=1.0, value=100.0)

    # زرار التوقع
    if st.button("احسب التكلفة"):
        try:
            # تجهيز البيانات للموديل (10 مدخلات)
            input_data = np.zeros((1, 10))
            input_data[0, 0] = consumption
            
            # التوقع
            prediction = model.predict(input_data)
            
            # عرض النتيجة بشكل مميز
            st.markdown("### النتيجة المتوقعة:")
            st.info(f"تكلفة الفاتورة التقديرية هي: **{prediction[0][0]:.2f}** جنيه")
            
            st.warning("⚠️ ملاحظة: هذه القيمة تقريبية بناءً على البيانات المتوفرة للموديل.")
            
        except Exception as e:
            st.error("حدث خطأ أثناء الحساب، يرجى المحاولة مرة أخرى.")
else:
    st.error("❌ فشل في تحميل ملف الموديل. تأكد من وجود الملف على GitHub.")

# تذييل الصفحة
st.markdown("---")
st.caption("تم التطوير بواسطة سلمى - مشروع تعلم الآلة 2026")
