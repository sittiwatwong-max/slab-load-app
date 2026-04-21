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
    .status-box { padding: 20px; border-radius: 15px; background: white; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR - INPUT DATA ---
with st.sidebar:
    st.title("🏗️ SlabMaster v4.1")
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

# Equivalent Loads (EUDL)
if ratio <= 2.0:
    type_text = "Two-way Slab"
    w_beam_short = (w_u * B) / 3
    w_beam_long = (w_u * B / 3) * ((3 - (B/L)**2) / 2)
else:
    type_text = "One-way Slab"
    w_beam_short = 0.0
    w_beam_long = (w_u * B) / 2

# --- 4. MAIN INTERFACE ---
st.title("Structural Load Analysis Dashboard")

if calc_trigger:
    # --- Metrics ---
    st.markdown(f"#### Analysis Result: <span style='color:#1a73e8'>{type_text}</span>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Load / Column", f"{col_load:.2f} kN")
    m2.metric("Long Beam", f"{w_beam_long:.2f} kN/m")
    m3.metric("Short Beam", f"{w_beam_short:.2f} kN/m")
    m4.metric("L/B Ratio", f"{ratio:.2f}")

    # --- Diagram ---
    st.write("### 📐 Load Distribution Diagram")
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#f8f9fa')

    # Slab Area
    ax.add_patch(patches.Rectangle((0, 0), L, B, fc='#f5f5f5', ec='#cfd8dc', alpha=0.5))

    # Tributary Areas
    if ratio <= 2.0:
        p_mid = B / 2
        t1 = patches.Polygon([[0,0], [p_mid, p_mid], [0, B]], fc='#ffe082', alpha=0.4, ec='#ffb300', ls='--')
        t2 = patches.Polygon([[L,0], [L-p_mid, p_mid], [L, B]], fc='#ffe082', alpha=0.4, ec='#ffb300', ls='--')
        t3 = patches.Polygon([[0,0], [L,0], [L-p_mid, p_mid], [p_mid, p_mid]], fc='#a5d6a7', alpha=0.4, ec='#43a047', ls='--')
        t4 = patches.Polygon([[0,B], [L,B], [L-p_mid, p_mid], [p_mid, p_mid]], fc='#a5d6a7', alpha=0.4, ec='#43a047', ls='--')
        ax.add_patch(t1); ax.add_patch(t2); ax.add_patch(t3); ax.add_patch(t4)
    else:
        ax.add_patch(patches.Rectangle((0, 0), L, B/2, fc='#a5d6a7', alpha=0.4, ec='#43a047', ls='--'))
        ax.plot([0, L], [B/2, B/2], color='#43a047', ls='--', lw=2)

    # Beams & Columns
    ax.plot([0, L, L, 0, 0], [0, 0, B, B, 0], color='#263238', lw=5) # Beam frame
    c_size = 0.2
    for x, y in [(0,0), [L,0], [L,B], [0,B]]:
        ax.add_patch(patches.Rectangle((x-c_size/2, y-c_size/2), c_size, c_size, color='#c62828', zorder=10))
        ax.text(x, y+0.3, f"{col_load:.1f}kN", ha='center', fontweight='bold', color='#c62828')

    # Load Labels
    ax.text(L/2, -0.4, f"Long Beam: {w_beam_long:.2f} kN/m", ha='center', color='#2e7d32', fontweight='bold')
    ax.text(L/2, B+0.2, f"Long Beam: {w_beam_long:.2f} kN/m", ha='center', color='#2e7d32', fontweight='bold')
    if w_beam_short > 0:
        ax.text(-0.3, B/2, f"Short Beam: {w_beam_short:.2f} kN/m", va='center', rotation=90, color='#ef6c00', fontweight='bold')
        ax.text(L+0.3, B/2, f"Short Beam: {w_beam_short:.2f} kN/m", va='center', rotation=90, color='#ef6c00', fontweight='bold')

    ax.set_xlim(-1, L+1); ax.set_ylim(-1, B+1); ax.set_aspect('equal'); ax.axis('off')
    st.pyplot(fig)

    # --- Report ---
    st.markdown("### 📋 Analysis Report")
    c_left, c_right = st.columns(2)
    with c_left:
        st.info(f"**Total Ultimate Load:** {total_load:.2f} kN\n\n**Pressure:** {w_u:.2f} kN/m²")
    with c_right:
        df = pd.DataFrame({
            "Element": ["Long Beam", "Short Beam"],
            "Load (kN/m)": [f"{w_beam_long:.2f}", f"{w_beam_short:.2f}"]
        })
        st.table(df)
else:
    st.info("กรุณากรอกข้อมูลและกดปุ่ม 'ANALYZE SYSTEM'")

st.markdown("---")
st.caption("SlabMaster Pro v4.1 | Fix: Unterminated string literal")
