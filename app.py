import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- 1. SETTING & THEME ---
st.set_page_config(page_title="SlabMaster Pro", page_icon="🏗️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .main { background-color: #f4f7f9; }
    .stMetric { 
        background: white; padding: 20px; border-radius: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #eee;
    }
    .calc-card {
        background: #ffffff; padding: 25px; border-radius: 20px;
        border-left: 8px solid #007bff; box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR INPUTS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4342/4342728.png", width=80)
    st.title("SlabMaster Pro")
    st.subheader("⚙️ Configuration")
    
    with st.expander("Dimensions (m)", expanded=True):
        L_long = st.number_input("Long Span (L)", value=5.0, min_value=0.1)
        L_short = st.number_input("Short Span (B)", value=3.0, min_value=0.1)
    
    with st.expander("Loading (kN/m²)", expanded=True):
        dead_load = st.number_input("Dead Load", value=3.5)
        live_load = st.number_input("Live Load", value=2.0)
    
    safety_factor = st.slider("Safety Factor (Ultimate)", 1.0, 2.0, 1.4)
    run_calc = st.button("🚀 ANALYZE STRUCTURE", use_container_width=True)

# --- 3. LOGIC & CALCULATIONS ---
# ปรับด้านให้ถูกต้องเสมอ
L = max(L_long, L_short)
B = min(L_long, L_short)
total_w = (dead_load + live_load) * safety_factor
area = L * B
total_load_on_slab = total_w * area
ratio = L / B

# คำนวณ Load ลงเสา (4 ต้น) - แบบง่ายคือหาร 4 แต่เชิงลึกจะกระจายตามพื้นที่รับผิดชอบ
# ในที่นี้คือ 1 slab panel เสาแต่ละต้นรับ 1/4 ของ Slab
load_per_column = total_load_on_slab / 4

# --- 4. MAIN INTERFACE ---
st.markdown(f'<div class="calc-card"><h1>Analysis Dashboard</h1><p>Project: Slab-to-Column Distribution Study</p></div>', unsafe_allow_html=True)
st.write("##")

if run_calc:
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "📐 Structural Diagram", "📑 Report"])
    
    with tab1:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Ultimate Load", f"{total_w:.2f} kN/m²")
        c2.metric("Total Weight", f"{total_load_on_slab:.2f} kN")
        c3.metric("Ratio L/B", f"{ratio:.2f}", delta="Two-way" if ratio <= 2 else "One-way")
        c4.metric("Load per Column", f"{load_per_column:.2f} kN", delta_color="inverse")

        st.write("### 🪜 Beam Distribution (EUDL)")
        if ratio <= 2:
            w_short = (total_w * B) / 3
            w_long = (total_w * B / 3) * ((3 - (B/L)**2) / 2)
        else:
            w_short = 0
            w_long = (total_w * B) / 2
        
        bc1, bc2 = st.columns(2)
        bc1.info(f"**Long Beam Load:** {w_long:.2f} kN/m")
        bc2.warning(f"**Short Beam Load:** {w_short:.2f} kN/m")

    with tab2:
        st.write("### 🏗️ Tributary Area & Column Positions")
        fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
        fig.patch.set_facecolor('#f4f7f9')
        
        # Draw Slab
        rect = plt.Rectangle((0, 0), L, B, fc='#e3f2fd', ec='#0d47a1', lw=2, alpha=0.6)
        ax.add_patch(rect)

        # Draw Columns (เสา 4 ต้น)
        cols_x = [0, L, L, 0]
        cols_y = [0, 0, B, B]
        ax.scatter(cols_x, cols_y, s=400, c='#263238', marker='s', zorder=5, label='Columns')

        # Draw Tributary Lines (เส้นแบ่งแรงลงเสา)
        ax.axhline(B/2, color='#546e7a', ls='--', lw=1, alpha=0.5)
        ax.axvline(L/2, color='#546e7a', ls='--', lw=1, alpha=0.5)

        # Annotate Columns with Load
        for i, (x, y) in enumerate(zip(cols_x, cols_y)):
            ax.annotate(f"C{i+1}\n{load_per_column:.1f} kN", (x, y), 
                        xytext=(15, 15) if x==0 else (-45, 15), 
                        textcoords='offset points', fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.8))

        # Styling
        ax.set_aspect('equal')
        ax.set_xlim(-1, L+1)
        ax.set_ylim(-1, B+1)
        plt.title(f"Load Distribution Path (Type: {'Two-way' if ratio <=2 else 'One-way'})", pad=20)
        plt.axis('off')
        st.pyplot(fig)

    with tab3:
        st.subheader("📋 Calculation Summary")
        report_df = pd.DataFrame({
            "Parameter": ["Slab Area", "Total Ultimate Load", "Slab Classification", "Column Load (C1-C4)"],
            "Value": [f"{area:.2f} m²", f"{total_load_on_slab:.2f} kN", "Two-way System" if ratio <=2 else "One-way System", f"{load_per_column:.2f} kN per column"],
            "Unit": ["m²", "kN", "Type", "kN"]
        })
        st.table(report_df)
        
        st.download_button("📥 Export CSV", report_df.to_csv().encode('utf-8'), "slab_analysis.csv", "text/csv")

else:
    # Landing State
    st.markdown("""
        <div style="text-align: center; padding: 50px; border: 2px dashed #ccc; border-radius: 20px;">
            <h2 style="color: #666;">Ready for Engineering Analysis</h2>
            <p>กรอกข้อมูลที่แถบด้านข้างแล้วกดปุ่ม <b>Analyze Structure</b> เพื่อเริ่มต้น</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #999;'>SlabMaster Pro v3.0 | Modern Structural UI</p>", unsafe_allow_html=True)
