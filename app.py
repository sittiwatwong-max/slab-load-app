import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าจอ
st.set_page_config(page_title="Slab Load App", layout="centered")

st.title("Slab Load Distribution App")
st.caption("Preliminary Design Tool")

# 2. ส่วนรับข้อมูล (Inputs) - ปรับเป็นระเบียบ
with st.container():
    dead_load = st.number_input("Dead Load (kN/m²)", value=3.00, step=0.10, format="%.2f")
    live_load = st.number_input("Live Load (kN/m²)", value=2.00, step=0.10, format="%.2f")
    length_l = st.number_input("Length L (m)", value=4.00, step=0.10, format="%.2f")
    width_b = st.number_input("Width B (m)", value=2.00, step=0.10, format="%.2f")
    
    column_pos = st.selectbox("Column Position", ["corner", "edge", "interior"])

st.markdown("---")

# 3. ส่วนคำนวณ (ใช้เพียงปุ่มเดียวเท่านั้นเพื่อไม่ให้ซ้ำ)
if st.button("Calculate"):
    # คำนวณเบื้องต้น
    total_load = dead_load + live_load
    ratio = length_l / width_b if width_b != 0 else 0
    
    # แสดงผลลัพธ์
    st.subheader("Results")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Load", f"{total_load:.2f} kN/m²")
    with col2:
        st.metric("L/B Ratio", f"{ratio:.2f}")

    # วิเคราะห์ประเภทพื้น
    if ratio > 2.0:
        st.success("Analysis: One-way Slab (พื้นทางเดียว)")
    else:
        st.success("Analysis: Two-way Slab (พื้นสองทาง)")
        
    # สรุปข้อมูลใส่ตารางให้ดูโปร
    df_res = pd.DataFrame({
        "Parameter": ["Dead Load", "Live Load", "Total Load", "Slab Geometry"],
        "Value": [f"{dead_load} kN/m²", f"{live_load} kN/m²", f"{total_load} kN/m²", f"{length_l}x{width_b} m"]
    })
    st.table(df_res)



  
