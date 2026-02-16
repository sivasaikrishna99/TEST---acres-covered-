import streamlit as st
import numpy as np

st.title("Drone Spray Coverage Calculator")

# -----------------------------
# INPUTS (UNCHANGED UI)
# -----------------------------

speed = st.slider("Speed (m/s)", 1.0, 8.0, 5.0, 0.1)

flowrate = st.number_input("Flowrate (L/min)", value=2.0)

swath = st.number_input("Swath Width (m)", value=5.5)

turns = st.number_input("Number of Turns", value=12)

tank_capacity = st.number_input("Tank Capacity (L)", value=15.0)

# -----------------------------
# Visual Shape Selection
# -----------------------------

shape = st.radio(
    "Select Field Shape",
    ["Square", "Rectangle", "Long Rectangle",
     "Trapezium", "Rhombus", "Skewed Rectangle"],
    horizontal=True
)

# -----------------------------
# Ideal Area Calculation (UNCHANGED LOGIC STYLE)
# -----------------------------

# Spray rate per second
flow_per_sec = flowrate / 60

# Area sprayed per second
area_per_sec = speed * swath

# Volume per square meter
vol_per_m2 = flow_per_sec / area_per_sec

# Total sprayable area in m2
ideal_area_m2 = tank_capacity / vol_per_m2

# Convert to acre
ideal_area = ideal_area_m2 / 4046.86

# -----------------------------
# Shape Factors (Geometry Model)
# -----------------------------

shape_factors = {
    "Square": 1.0,
    "Rectangle": 1.4,
    "Long Rectangle": 1.8,
    "Trapezium": 1.6,
    "Rhombus": 1.3,
    "Skewed Rectangle": 1.7
}

Sf_base = shape_factors[shape]

# Slight adjustment using turns
Sf = Sf_base * (1 + 0.015 * (turns - 10))

# Effective straight length
L_eff = np.sqrt(ideal_area_m2 * Sf)

# -----------------------------
# Turn Physics Model
# -----------------------------

R = 5        # realistic drone turn radius (m)
V_turn = 3   # slower turning speed (m/s)

K = np.pi * R * (speed / V_turn)

eta = L_eff / (L_eff + K)

# -----------------------------
# Actual Area
# -----------------------------

actual_area = ideal_area * eta

# -----------------------------
# RESULTS
# -----------------------------

st.subheader("Results")

st.write(f"Ideal Area (acre)")
st.write(f"{ideal_area:.3f}")

st.write(f"Actual Field Area (acre)")
st.write(f"{actual_area:.3f}")

st.write(f"Field Efficiency")
st.write(f"{eta:.3f}")
