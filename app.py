import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. ตั้งค่าหน้าเบราว์เซอร์ (ต้องอยู่บรรทัดแรกสุดเสมอ)
st.set_page_config(
    page_title="Slab Load Design Pro", # ชื่อบนแถบ Browser
    page_icon="🏗️",                  # ไอคอนบนแถบ Browser
    layout="centered"
)

# 2. ส่วนหัวของแอป
st.title("🏗️ Slab Load Distribution App")
st.caption("เครื่องมือช่วยคำนวณการถ่ายแรงจากพื้นลงสู่คาน | พัฒนาโดย AI Assistant")
st.markdown("---")

# 3. ส่วนรับข้อมูล (Input Section)
st.subheader("📥 ข้อมูลออกแบบ (Input Parameters)")
col_in1, col_in2 = st.columns(2)

with col_in1:
    dead_load = st.number_input("Dead Load (kN/m²)", value=3.00, step=0.10, format="%.2f")
    live_load = st.number_input("Live Load (kN/m²)", value=2.00, step=0.10, format="%.2f")

with col_in2:
    length_l = st.number_input("ความยาวด้านยาว L (m)", value=4.00, step=0.10, format="%.2f")
    width_b = st.number_input("ความกว้างด้านสั้น B (m)", value=2.00, step=0.10, format="%.2f")

column_pos = st.selectbox("Column Position", ["corner", "edge", "interior"])

st.markdown("---")

# 4. ส่วนการคำนวณและแสดงผล (Calculation & Output)
# ใช้ปุ่มเดียวเพื่อป้องกัน Error Duplicate ID
if st.button("🚀 Calculate Results", use_container_width=True):
    
    # สูตรคำนวณ
    total_load = dead_load + live_load
    if width_b > 0:
        ratio = length_l / width_b
    else:
        ratio = 0
    
    # ส่วนแสดงค่า Metric (ตัวเลขใหญ่ๆ)
    st.subheader("📊 ผลการวิเคราะห์ (Results)")
    res_col1, res_col2, res_col3 = st.columns(3)
    
    res_col1.metric("Total Load", f"{total_load:.2f} kN/m²")
    res_col2.metric("L/B Ratio", f"{ratio:.2f}")
    
    # วิเคราะห์ประเภทพื้น
    if ratio > 2.0:
        res_col3.warning("One-way Slab")
        slab_type = "พื้นทางเดียว (One-way Slab)"
        dist_desc = "ถ่ายแรงลงคานด้านยาว 2 ด้าน (Uniform Load)"
    else:
        res_col3.success("Two-way Slab")
        slab_type = "พื้นสองทาง (Two-way Slab)"
        dist_desc = "ถ่ายแรงลงคาน 4 ด้าน (รูปสามเหลี่ยม และ คางหมู)"

    # ตารางสรุปรายการคำนวณ
    st.write("### 📝 สรุปรายการคำนวณ")
    summary_data = {
        "รายการ": ["ประเภทพื้น", "ทิศทางการถ่ายแรง", "ตำแหน่งเสา", "น้ำหนักบรรทุกรวม"],
        "ข้อมูล": [slab_type, dist_desc, column_pos, f"{total_load:.2f} kN/m²"]
    }
    st.table(pd.DataFrame(summary_data))

    # วาดรูป Diagram พื้นแบบง่าย
    st.write("### 🖼️ แผนผังการกระจายแรง (Diagram)")
    fig, ax = plt.subplots(figsize=(6, 3))
    # วาดรูปพื้น
    rect = plt.Rectangle((0, 0), length_l, width_b, color='#E1F5FE', ec='#01579B', lw=2)
    ax.add_patch(rect)
    
    # ปรับแต่งกราฟ
    ax.set_xlim(-0.5, length_l + 0.5)
    ax.set_ylim(-0.5, width_b + 0.5)
    ax.set_aspect('equal')
    ax.axis('off') # ปิดแกนตัวเลขเพื่อให้ดูเหมือนรูปวาด
    
    # ใส่ข้อความกำกับขนาด
    ax.text(length_l/2, -0.2, f"L = {length_l} m", ha='center')
    ax.text(-0.2, width_b/2, f"B = {width_b} m", va='center', rotation=90)
    
    st.pyplot(fig)
    st.balloons() # ใส่ Effect แสดงความยินดี

else:
    st.info("กรอกข้อมูลให้ครบถ้วนแล้วกดปุ่ม Calculate เพื่อเริ่มการคำนวณ")

# ส่วนท้ายแอป
st.markdown("---")
st.caption("Slab Load Design Pro - Engineering Tools for Students")



  
