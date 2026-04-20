import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. ตั้งค่าหน้าตาเบราว์เซอร์และไอคอน (ส่วนที่คุณต้องการเปลี่ยน)
# ผมใส่ลิงก์รูปไอคอนวิศวกรรม (ตึก/เครน) เพื่อให้เวลาติดตั้งบน Desktop จะได้รูปที่สวยขึ้น
st.set_page_config(
    page_title="Slab Load Design Pro", 
    page_icon="https://cdn-icons-png.flaticon.com/512/4342/4342728.png", 
    layout="centered"
)

# 2. ปรับแต่ง CSS เพื่อความสวยงาม (ทำให้หน้าตาดูเหมือนแอปจริงๆ)
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ส่วนหัวของแอป
st.title("🏗️ Slab Load Distribution Pro")
st.write("โปรแกรมคำนวณการถ่ายแรงพื้นลงสู่คานเบื้องต้น")
st.markdown("---")

# 4. ส่วนรับข้อมูล (Input)
st.subheader("📥 ข้อมูลการออกแบบ (Input Data)")
col1, col2 = st.columns(2)

with col1:
    st.info("💡 น้ำหนักบรรทุก")
    dl = st.number_input("Dead Load (kN/m²)", value=3.0, step=0.1, format="%.2f")
    ll = st.number_input("Live Load (kN/m²)", value=2.0, step=0.1, format="%.2f")

with col2:
    st.info("📏 ขนาดแผ่นพื้น")
    L = st.number_input("ความยาวด้านยาว L (m)", value=4.0, step=0.1, format="%.2f")
    B = st.number_input("ความกว้างด้านสั้น B (m)", value=2.0, step=0.1, format="%.2f")

column_pos = st.selectbox("ตำแหน่งเสา (Column Position)", ["Corner", "Edge", "Interior"])

# 5. ส่วนการคำนวณ (Calculation)
st.markdown("---")
if st.button("🚀 คำนวณและวิเคราะห์ผล"):
    
    # คำนวณค่าพื้นฐาน
    total_w = dl + ll
    ratio = L / B if B > 0 else 0
    
    # วิเคราะห์ประเภทพื้น
    if ratio > 2.0:
        slab_type = "One-way Slab (พื้นทางเดียว)"
        result_color = "orange"
        load_dist = "ถ่ายแรงลงคานด้านยาว 2 ด้าน"
    else:
        slab_type = "Two-way Slab (พื้นสองทาง)"
        result_color = "green"
        load_dist = "ถ่ายแรงลงคาน 4 ด้าน (สามเหลี่ยม/คางหมู)"

    # แสดงผลลัพธ์แบบ Metrics
    st.subheader("📊 ผลการวิเคราะห์ (Results)")
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Total Load", f"{total_w:.2f} kN/m²")
    m_col2.metric("L/B Ratio", f"{ratio:.2f}")
    m_col3.metric("Type", "One-way" if ratio > 2 else "Two-way")

    st.markdown(f"🔔 วิเคราะห์พบว่าเป็น: **:{result_color}[{slab_type}]**")
    
    # แสดงตารางสรุป
    st.write("### 📝 สรุปรายละเอียด")
    summary = {
        "หัวข้อ": ["น้ำหนักรวม (w)", "อัตราส่วนด้าน", "รูปแบบการถ่ายแรง", "ตำแหน่งเสา"],
        "รายละเอียด": [f"{total_w:.2f} kN/m²", f"{ratio:.2f}", load_dist, column_pos]
    }
    st.table(pd.DataFrame(summary))

    # 6. วาดรูปการกระจายแรง (Diagram)
    st.write("### 📐 Load Distribution Diagram")
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # วาดรูปพื้น
    rect = plt.Rectangle((0, 0), L, B, linewidth=2, edgecolor='#333', facecolor='#e1f5fe')
    ax.add_patch(rect)
    
    # วาดเส้นแบ่งแรง (Tributary Area)
    if ratio <= 2.0:
        # เส้นทแยงมุมสำหรับ Two-way
        ax.plot([0, B/2], [0, B/2], 'r--', lw=1)
        ax.plot([L, L-B/2], [0, B/2], 'r--', lw=1)
        ax.plot([0, B/2], [B, B-B/2], 'r--', lw=1)
        ax.plot([L, L-B/2], [B, B-B/2], 'r--', lw=1)
        ax.plot([B/2, L-B/2], [B/2, B/2], 'r--', lw=1)
        ax.plot([B/2, L-B/2], [B-B/2, B-B/2], 'r--', lw=1)
    else:
        # เส้นขนานสำหรับ One-way
        ax.axhline(B/2, color='r', linestyle='--', lw=1)

    ax.set_xlim(-0.5, L + 0.5)
    ax.set_ylim(-0.5, B + 0.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # ใส่ข้อความบอกขนาด
    ax.text(L/2, -0.2, f"Length {L}m", ha='center', fontsize=10)
    ax.text(-0.2, B/2, f"Width {B}m", va='center', rotation=90, fontsize=10)
    
    st.pyplot(fig)
    st.balloons() # เอฟเฟกต์แสดงความยินดี

else:
    st.info("กรอกข้อมูลด้านบนแล้วกดปุ่ม 'คำนวณและวิเคราะห์ผล'")

# ส่วนท้าย
st.markdown("---")
st.caption("Developed for Engineering Purposes | Version 2.0")


  
