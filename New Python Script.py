import streamlit as st

st.set_page_config(page_title="Agri Drone Area Calculator", layout="centered")
st.title("🚁 Agricultural Drone Area Coverage Calculator")
st.caption("Nozzle-based spreading model (Turn loss fixed at 2%)")

st.divider()

TURN_LOSS = 0.02
ACRE_M2 = 4046.86

# -----------------------
# Nozzle Selection
# -----------------------
st.subheader("🧪 Select Nozzle Type")

if "selected_nozzle" not in st.session_state:
    st.session_state.selected_nozzle = "Centrifugal"

col1, col2 = st.columns(2)

with col1:
    if st.button("🔘 Centrifugal Nozzle", use_container_width=True):
        st.session_state.selected_nozzle = "Centrifugal"

with col2:
    if st.button("🔘 Flat Fan Nozzle", use_container_width=True):
        st.session_state.selected_nozzle = "Flat Fan"

selected_nozzle = st.session_state.selected_nozzle

st.divider()

# -----------------------
# Inputs
# -----------------------

dispense_per_acre = st.number_input(
    "Dispense weight per acre (kg)",
    min_value=1.0,
    max_value=200.0,
    value=25.0,
    step=1.0
)

acres = st.number_input(
    "Number of acres",
    min_value=0.1,
    max_value=50.0,
    value=1.0,
    step=0.1
)

# Total weight (auto calculated)
total_dispense = dispense_per_acre * acres

st.metric("Total Dispense Weight (kg)", f"{round(total_dispense,1)}")

st.divider()

# -----------------------
# Altitude Selection
# -----------------------
st.subheader("📏 Select Altitude (m)")

altitudes = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
cols = st.columns(len(altitudes))

for alt, col in zip(altitudes, cols):
    with col:
        if st.button(f"{alt}m"):
            st.session_state.selected_altitude = alt

if "selected_altitude" not in st.session_state:
    st.session_state.selected_altitude = 2.0

st.caption(f"Selected Altitude: {st.session_state.selected_altitude} m")

# -----------------------
# Discharge % Selection
# -----------------------
st.subheader("💧 Select Discharge Rate (%)")

rates = [30, 40, 50, 60, 70, 80, 90, 100]
cols = st.columns(len(rates))

for r, col in zip(rates, cols):
    with col:
        if st.button(f"{r}%"):
            st.session_state.selected_rate = r

if "selected_rate" not in st.session_state:
    st.session_state.selected_rate = 50

st.caption(f"Selected Discharge Setting: {st.session_state.selected_rate}%")

st.divider()

# -----------------------
# Nozzle-Based Constants (For Now Fixed)
# -----------------------
if selected_nozzle == "Centrifugal":
    SWATH_WIDTH = 5.5
    FLOW_RATE = 3.0
else:
    SWATH_WIDTH = 4.0
    FLOW_RATE = 2.307

# -----------------------
# Calculations
# -----------------------

# Spray time (seconds)
t_spray = (total_dispense / FLOW_RATE) * 60

# Ideal area
A_ideal = (SWATH_WIDTH * t_spray)  # m² (before speed)

# Real area needed
A_real_m2 = acres * ACRE_M2

# Apply turn efficiency
efficiency_factor = (1 - TURN_LOSS)
# Solve for speed:
# A_real = (v × SWATH × t) × efficiency^N
# v = A_real / (SWATH × t × efficiency^N)

# For simplicity assume 12 turns default
N = 12

v_required = A_real_m2 / (SWATH_WIDTH * t_spray * (efficiency_factor ** N))

v_required = round(v_required, 1)

# -----------------------
# Output
# -----------------------
st.subheader("📊 Results")

st.metric("Required Speed (m/s)", f"{v_required}")
st.metric("Swath Width (m)", f"{SWATH_WIDTH}")

st.caption(
    "Model:\n"
    "Total Weight = kg/acre × acres\n"
    "Speed = Area / (Swath × SprayTime × TurnEfficiency)\n\n"
    "Turn loss fixed at 2% per turn."
)
