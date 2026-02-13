import streamlit as st

st.set_page_config(page_title="Agri Drone Area Calculator", layout="centered")
st.title("🚁 Agricultural Drone Area Coverage Calculator (Calibrated Model)")
st.caption("Physics + Calibrated Efficiency Model")

st.divider()

# -----------------------
# Default Values
# -----------------------
defaults = {
    "speed": 5.0,      # m/s
    "width": 5.5,      # m
    "flow": 3.0,       # kg/min
    "tank": 10.0,      # kg
    "turns": 10,
}

for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# -----------------------
# Inputs
# -----------------------
speed = st.slider("Speed (m/s)", 0.5, 15.0, st.session_state.speed, 0.1)
width = st.slider("Swath width (m)", 0.5, 15.0, st.session_state.width, 0.1)
flow = st.slider("Flow rate (kg/min)", 0.1, 20.0, st.session_state.flow, 0.001)
tank = st.slider("Total Dispense weight (kg)", 1.0, 50.0, st.session_state.tank, 0.5)
turns = st.slider("Number of turns (N)", 0, 200, st.session_state.turns, 1)

st.divider()

# -----------------------
# Core Calculations
# -----------------------

# Ideal Area
A_ideal = (tank * speed * width) / (flow * 4046.86)

# Application Density
D = flow / (speed * width)

# Reference Density (calibrated from CASE 1)
D_ref = 3 / (5 * 5.5)

# Calibrated Constants
k1 = 0.0045
k2 = 0.35

# Efficiency Model
efficiency = (
    1
    - k1 * turns * (speed / 5) ** 2
    + k2 * ((D_ref - D) / D_ref)
)

# Safety clamp (avoid unrealistic >1.2 or negative values)
efficiency = max(0, min(efficiency, 1.2))

# Real Area
A_real = A_ideal * efficiency

# -----------------------
# Output
# -----------------------

st.subheader("📊 Results")

c1, c2 = st.columns(2)

with c1:
    st.metric("Ideal Area (acre)", f"{A_ideal:.3f}")

with c2:
    st.metric("Actual Field Area (acre)", f"{A_real:.3f}")

st.caption(
    """
Model Used:

A_real = A_ideal × Efficiency

Efficiency =
1 − k1·N·(V/5)^2 + k2·((D_ref − D)/D_ref)

Where:
D = Flow / (Speed × Width)

This model accounts for:
• Turn radius scaling with speed²
• Application density correction
"""
)
