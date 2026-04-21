import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- 1. SETTING & MODERN STYLING ---
st.set_page_config(page_title="Slab Analysis Pro", page_icon="🏗️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stApp { font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    div[data-testid="stMetricValue"] { font-size: 24px; color: #007bff; }
    .status-box { padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #dee2e6; background: white; }
    .beam-label { font-weight: bold; color: #d32f2f; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR - INPUT DATA ---
with st.sidebar:
    st.title("🏗️ SlabMaster v3.5")
    st.markdown("---")
    st.subheader("📏 Geometry")
    L_in = st.number_input("Long Span (L) [m]", value=6.0, step=0.5)
    B_in = st.number_input("Short Span (B) [m]", value=4.0, step=0.5)
    
    st.subheader("💡 Loads")
    dl = st.number_input("Dead Load [kN/m²]", value=4.0)
    ll = st.number_input("Live Load [kN/m²]", value=2.5)
    sf = st.slider("Safety Factor (Ultimate)", 1.0, 2.0, 1.45)
    
    calc_trigger = st.button("🚀 ANALYZE SYSTEM", use_container_width=True)

# --- 3. COMPUTATION LOGIC ---
L = max(L_in, B_in)
B = min(L_in, B_in)
w_u = (dl + ll) * sf
ratio = L / B
total_load = w_u * L * B
col_load = total_load / 4

# Equivalent Loads on Beams (EUDL)
if ratio <= 2.0:
    # Two-way Slab
    type_text = "Two-way Slab"
    w_beam_short = (w_u * B) / 3
    w_beam_long = (w_u * B / 3) * ((3 - (B/L)**2) / 2)
else:
    # One-way Slab
    type_text = "One-way Slab"
    w_beam_short = 0.0
    w_beam_long = (w_u * B) / 2

# --- 4. MAIN DASHBOARD ---
st.title("Structural Load Analysis Dashboard")
st.markdown(f"**Analysis Mode:** {type_text} | **Design Pressure:** {w_u:.2f} kN/m²")

if calc_trigger:
    # --- Metrics Bar ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Load per Column", f"{col_load:.2f} kN")
    m2.metric("Long Beam Load", f"{w_beam_long:.2f} kN/m")
    m3.metric("Short Beam Load", f"{w_beam_short:.2f} kN/m")
    m4.metric("L/B Ratio", f"{ratio:.2f}")

    # --- Diagram Section ---
    st.subheader("📐 Structural Layout & Load Distribution")
    
    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor('#f8f9fa')

    # 1. วาด Slab (พื้น)
    slab = patches.Rectangle((0, 0), L, B, linewidth=1, edgecolor='#cfd8dc', facecolor='#eceff1', alpha=0.4)
    ax.add_patch(slab)

    # 2. วาด Tributary Areas (พื้นที่รับแรง)
    if ratio <= 2.0:
        # แนวเส้นทะแยงมุมสำหรับพื้น 2 ทาง
        p_mid = B/2
        # พื้นที่สามเหลี่ยม (ด้านสั้น)
        tri_left = patches.Polygon([[0,0], [p_mid, p_mid], [0, B]], facecolor='#ffecb3', alpha=0.5, edgecolor='#ffa000', ls='--')
        tri_right = patches.Polygon([[L,0],
