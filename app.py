import streamlit as st

st.set_page_config(page_title="Slab Load App", layout="centered")

st.title("Slab Load Distribution App")
st.caption("Preliminary Design Tool")

# INPUT
DL = st.number_input("Dead Load (kN/m²)", value=3.0)
LL = st.number_input("Live Load (kN/m²)", value=2.0)
L = st.number_input("Length L (m)", value=4.0)
B = st.number_input("Width B (m)", value=2.0)

column_type = st.selectbox("Column Position", ["corner", "edge", "center"])

if st.button("Calculate"):
    q = DL + LL

    st.subheader("Results")
    st.write(f"q = {q:.2f} kN/m²")

    if L / B > 2:
        st.success("One-way slab")
        w = q * B
        P = (w * L) / 2

        st.write(f"Beam load w = {w:.2f} kN/m")
        st.write(f"Column load P = {P:.2f} kN")

    else:
        st.success("Two-way slab")
        wx = q * (B / 2)
        wy = q * (L / 2)

        if column_type == "corner":
            P = q * (L/2) * (B/2)
        elif column_type == "edge":
            P = q * L * (B/2)
        else:
            P = q * (L * B / 4)

        st.write(f"wx = {wx:.2f} kN/m")
        st.write(f"wy = {wy:.2f} kN/m")
        st.write(f"Column load P = {P:.2f} kN")
