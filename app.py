import streamlit as st
import pandas as pd
from fpdf import FPDF

st.set_page_config(page_title="Solar Distribution Box Sizing Tool", layout="centered")

st.title("🔌 Solar Distribution Box Sizing Tool")
st.subheader("Professional Sizing Guide for Rooftop Solar Installations")

st.markdown("""
This tool helps you size the **DC Distribution Box (DCDB)** and **AC Distribution Box (ACDB)** based on your inverter and panel configurations.
""")

st.header("📟 Input Parameters")

inverter_rating = st.number_input("Inverter Capacity (kW)", min_value=0.5, max_value=100.0, value=3.0, step=0.5)
string_count = st.number_input("Number of DC Strings", min_value=1, max_value=10, value=2)
voc_per_string = st.number_input("Open Circuit Voltage per String (V)", min_value=100, max_value=1000, value=450)
isc_per_string = st.number_input("Short Circuit Current per String (A)", min_value=1, max_value=30, value=9)
ac_output_voltage = st.selectbox("AC Output Voltage", options=["230V Single Phase", "415V Three Phase"])

st.header("🛠️ Recommended Ratings")

# DCDB Calculations
fuse_rating = round(isc_per_string * 1.25, 1)
mcb_dc_rating = round(string_count * isc_per_string * 1.25, 1)

dcdb_data = {
    "Component": ["String Fuses (per string)", "Main DC MCB", "DC SPD", "DC Isolator", "Enclosure"],
    "Recommended Rating": [
        f"{fuse_rating} A DC Fuse",
        f"{mcb_dc_rating} A DC MCB",
        f"Rated for {voc_per_string} V (Type 2 SPD)",
        f"{mcb_dc_rating} A DC Isolator",
        "IP65, UV-Proof, Polycarbonate"
    ]
}

# ACDB Calculations
ac_current_output = round((inverter_rating * 1000) / (230 if ac_output_voltage == "230V Single Phase" else 415) * 1.25, 1)

acdb_data = {
    "Component": ["AC MCB", "AC SPD", "AC Isolator", "RCCB/ELCB", "Enclosure"],
    "Recommended Rating": [
        f"{ac_current_output} A AC MCB",
        f"Suitable for {ac_output_voltage} (Type 2 SPD)",
        f"{ac_current_output} A AC Isolator",
        "30mA Sensitivity",
        "IP65, UV-Proof, Polycarbonate"
    ]
}

st.subheader("📋 DC Distribution Box (DCDB)")
st.dataframe(pd.DataFrame(dcdb_data), use_container_width=True)

st.subheader("📋 AC Distribution Box (ACDB)")
st.dataframe(pd.DataFrame(acdb_data), use_container_width=True)

# PDF Generation
st.header("📝 Download Sizing Report as PDF")

if st.button("📥 Generate PDF Report"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Solar Distribution Box Sizing Report", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Inverter Capacity: {inverter_rating} kW", ln=True)
    pdf.cell(0, 10, f"Number of DC Strings: {string_count}", ln=True)
    pdf.cell(0, 10, f"VOC per String: {voc_per_string} V", ln=True)
    pdf.cell(0, 10, f"ISC per String: {isc_per_string} A", ln=True)
    pdf.cell(0, 10, f"AC Output Voltage: {ac_output_voltage}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "DC Distribution Box (DCDB):", ln=True)

    pdf.set_font("Arial", "", 12)
    for comp, rating in zip(dcdb_data["Component"], dcdb_data["Recommended Rating"]):
        pdf.cell(0, 8, f"- {comp}: {rating}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "AC Distribution Box (ACDB):", ln=True)

    pdf.set_font("Arial", "", 12)
    for comp, rating in zip(acdb_data["Component"], acdb_data["Recommended Rating"]):
        pdf.cell(0, 8, f"- {comp}: {rating}", ln=True)

    st.download_button(
        label="📄 Download PDF",
        data=pdf.output(dest="S").encode("latin-1"),
        file_name="Solar_Distribution_Box_Sizing_Report.pdf",
        mime="application/pdf"
    )

st.markdown("---")
st.markdown("Made with ❤️ by Ganesh Moorthi | [Visit My Medium](https://medium.com/@ganeshitya)")
