import streamlit as st

st.set_page_config(page_title="Agri Drone Area Calculator", layout="centered")
st.title("🚁 Agricultural Drone Area Coverage Calculator (Calibrated Model)")
st.caption("Speed-based turn physics + density correction")

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
    st.session_state.setdefault(f"{k}_slider", v)
    st.session_state.setdefault(f"{k}_input", v)

# -----------------------
# Sync Functions
# -----------------------
def slider_changed(name):
    val = st.session_state[f"{name}_slider"]
    st.session_state[name] = val
    st.session_state[f"{name}_input"] = val

def input_changed(name):
    val = st.session_state[f"{name}_input"]
    st.session_state[name] = val
    st.session_state[f"{name}_slider"] = val

# -----------------------
# Synced Input Widget
# -----------------------
def synced_input(label, name, minv, maxv, step, fmt=None):
    c1, c2 = st.columns([2, 1])
    with c1:
        st.slider(
            label,
            min_value=minv,
            max_value=maxv,
            step=step,
            value=st.session_state[name],
            key=f"{name}_slider",
            on_change=slider_changed,
            args=(name,)
        )
    with c2:
        st.number_input(
            " ",
            min_value=minv,
            max_value=maxv,
            step=step,
            format=fmt,
            value=st.session_state[name],
            key=f"{name}_input",
            on_change=input_changed,
            args=(name,)
        )

# -----------------------
# Inputs
# -----------------------
synced_input("Speed (m/s)", "speed", 0.5, 15.0, 0.1)
synced_input("Swath width (m)", "width", 0.5, 15.0, 0.1)
synced_input("Flow rate (kg/min)", "flow", 0.1, 20.0, 0.001, "%.4f")
synced_input("Total Dispense weight (kg)", "tank", 1.0, 50.0, 0.5)
synced_input("Number of turns (N)", "turns", 0, 200, 1)

st.divider()

# -----------------------
# Core Calculations
# -----------------------
V = st.session_state.speed
W = st.session_state.width
F = st.session_state.flow
T = st.session_state.tank
N = st.session_state.turns

# Ideal Area (acre)
A_ideal = (T * V * W) / (F * 4046.86)

# Application Density
D = F / (V * W)

# Reference Density (from CASE 1 calibration)
D_ref = 3 / (5 * 5.5)

# Calibrated Constants
k1 = 0.0045
k2 = 0.35

# Efficiency Model
efficiency = (
    1
    - k1 * N * (V / 5) ** 2
    + k2 * ((D_ref - D) / D_ref)
)

# Clamp efficiency for stability
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

This accounts for:
• Speed²-based turn radius loss
• Application density correction
• Empirical calibration from real field data
"""
)
