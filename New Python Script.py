import streamlit as st
import numpy as np

st.title("Drone Spray Coverage Calculator (Shape Based)")

# -----------------------------
# Inputs
# -----------------------------

speed = st.slider("Speed (m/s)", 1.0, 8.0, 5.0, 0.1)
flowrate = st.number_input("Flowrate (L/min)", value=2.0)
weight = st.number_input("Chemical per Acre (L/acre)", value=2.0)
swath = st.number_input("Swath Width (m)", value=5.5)
turns = st.number_input("Number of Turns", value=12)

shape = st.selectbox(
    "Field Shape",
    ["Square", "Rectangle", "Long Rectangle",
     "Trapezium", "Rhombus", "Skewed Rectangle"]
)

# -----------------------------
# Tank Capacity
# -----------------------------
tank_capacity = 15  # liters

# -----------------------------
# Ideal Area
# -----------------------------
ideal_area = tank_capacity / weight  # acre
ideal_area_m2 = ideal_area * 4046.86

# -----------------------------
# Shape Factors
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

# Turn influence adjustment
Sf = Sf_base * (1 + 0.02 * (turns - 10))

# Effective Straight Length
L_eff = np.sqrt(ideal_area_m2 * Sf)

# -----------------------------
# Turn Physics
# -----------------------------
R = 5        # meters
V_turn = 3   # m/s

K = np.pi * R * (speed / V_turn)

# Efficiency
eta = L_eff / (L_eff + K)

# -----------------------------
# Actual Area
# -----------------------------
actual_area = ideal_area * eta

# -----------------------------
# Output
# -----------------------------
st.subheader("Results")

st.write(f"Ideal Area (acre): {ideal_area:.2f}")
st.write(f"Actual Field Area (acre): {actual_area:.2f}")
st.write(f"Field Efficiency: {eta:.3f}")
