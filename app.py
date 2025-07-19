import streamlit as st

st.set_page_config(page_title="Solar Distribution Box Sizing Tool", layout="centered")

st.title("🔌 Solar Distribution Box Sizing Tool")
st.subheader("For Residential Rooftop Solar Installations")

st.markdown("""
This tool helps you size the DCDB and ACDB for your solar system based on inverter size and string configuration.
""")

st.header("📟 Input Parameters")

# Input Section
inverter_rating = st.number_input("Inverter Capacity (kW)", min_value=0.5, max_value=100.0, value=3.0, step=0.5)
string_count = st.number_input("Number of DC Strings", min_value=1, max_value=10, value=2)
voc_per_string = st.number_input("Open Circuit Voltage per String (V)", min_value=100, max_value=1000, value=450)
isc_per_string = st.number_input("Short Circuit Current per String (A)", min_value=1, max_value=30, value=9)

ac_output_voltage = st.selectbox("AC Output Voltage", options=["230V Single Phase", "415V Three Phase"])

st.header("🛠️ Recommended Ratings")

# DCDB Calculations
st.subheader("DC Distribution Box (DCDB)")

fuse_rating = round(isc_per_string * 1.25, 1)
mcb_dc_rating = round(string_count * isc_per_string * 1.25, 1)

st.markdown(f"""
- **String Fuses (per string):** {fuse_rating} A DC Fuse
- **Main DC MCB:** {mcb_dc_rating} A DC MCB (Total Combined Current)
- **Surge Protection Device:** DC SPD rated for **{voc_per_string} V**
- **Isolator:** Same as MCB rating **{mcb_dc_rating} A**
- **Enclosure:** IP65, UV Protected, Polycarbonate
""")

# ACDB Calculations
st.subheader("AC Distribution Box (ACDB)")

ac_current_output = round((inverter_rating * 1000) / (230 if ac_output_voltage == "230V Single Phase" else 415) * 1.25, 1)

st.markdown(f"""
- **AC MCB:** {ac_current_output} A
- **AC SPD:** Suitable for {ac_output_voltage} system
- **AC Isolator:** Rated for {ac_current_output} A
- **RCCB/ELCB:** 30mA Sensitivity
- **Enclosure:** IP65, UV Protected
""")

st.header("📥 Download Sample Datasheet")
st.markdown("[Download Sample DCDB/ACDB Datasheet (PDF)](https://yourgithubrepo.com/sample_datasheet.pdf)")

st.success("🔋 Use this as a basic sizing guide. Consult a qualified electrician for installation.")

st.markdown("---")
st.markdown("Made with ❤️ by Ganesh Moorthi | [Visit My Medium](https://medium.com/@ganeshitya)")
