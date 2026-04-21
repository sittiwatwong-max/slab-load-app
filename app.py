import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- 1. SETTING & MODERN STYLING ---
st.set_page_config(page_title="Slab Analysis Pro", page_icon="🏗️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stApp { font-family: 'Segoe UI', Roboto, sans-serif; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #1a73e8; font-weight: bold; }
    .status-box { padding: 20px; border-radius: 15px; background: white; border: 1px solid #e0e0e0; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR - INPUT DATA ---
with st.sidebar:
    st.title("🏗️ SlabMaster v4.0")
    st.markdown("---")
    st.subheader("📏 Slab Dimensions")
    L_in = st.number_input("Long Span (L) [m]", value=6.0, min_value=0.1, step=0.5)
    B_in = st.number_input("Short Span (B) [m]", value=4.0, min_value=0.1, step=0.5)
    
    st.subheader("💡 Load Factors")
    dl = st.number_input("Dead Load [kN/m²]", value=4.0, step=0.1)
    ll = st.number_input("Live Load [kN/m²]", value=2.5, step=0.1)
    sf = st.slider("Safety Factor (Ultimate)", 1.0, 2.0, 1.45)
    
    calc_trigger = st.button("🚀 ANALYZE SYSTEM", use_container_width=True)

# --- 3. COMPUTATION LOGIC ---
L = max(L_in, B_in)
B = min(L_in, B_in)
w_u = (dl + ll) * sf
ratio = L / B
total_load = w_u * L * B
col_load = total_load / 4

# Equivalent Uniformly Distributed Loads (EUDL)
if ratio <= 2.0:
    type_text = "Two-way Slab"
    w_beam_short = (w_u * B) / 3
    w_beam_long = (w_u * B / 3) * ((3 - (B/L)**2) / 2)
else:
    type_text = "One-way Slab
