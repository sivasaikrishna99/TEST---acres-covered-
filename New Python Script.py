import streamlit as st

st.set_page_config(page_title="Agri Drone Area Calculator", layout="centered")
st.title("🚁 Agricultural Drone Area Coverage Calculator")
st.caption("Nozzle-based model (Turn loss fixed at 2%)")

st.divider()

# -----------------------
# Defaults
# -----------------------
defaults = {
    "dispense_per_acre": 25.0,
    "acres": 1.0,
}

for k, v in defaults.items():
    st.session_state.setdefault(k, v)
    st.session_state.setdefault(f"{k}_slider", v)
    st.session_state.setdefault(f"{k}_input", v)

if "selected_shape" not in st.session_state:
    st.session_state.selected_shape = "Square"

if "selected_nozzle" not in st.session_state:
    st.session_state.selected_nozzle = "Centrifugal"

# -----------------------
# Sync functions
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
# Synced input widget
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
# Nozzle Selection (with indicator)
# -----------------------
st.subheader("🧪 Select Nozzle Type")

nozzle_types = ["Centrifugal", "Flat Fan"]

cols = st.columns(len(nozzle_types))

for nozzle, col in zip(nozzle_types, cols):
    with col:
        is_selected = st.session_state.selected_nozzle == nozzle
        circle = "🔴" if is_selected else "⚪"

        if st.button(f"{circle} {nozzle}", key=f"btn_{nozzle}", use_container_width=True):
            st.session_state.selected_nozzle = nozzle

selected_nozzle = st.session_state.selected_nozzle

st.divider()

# -----------------------
# Inputs
# -----------------------
synced_input("Dispense weight per acre (kg)", "dispense_per_acre", 1.0, 200.0, 1.0)
synced_input("Number of acres", "acres", 0.1, 50.0, 0.1)

# Total dispense (auto calculated display)
total_dispense = st.session_state.dispense_per_acre * st.session_state.acres
st.metric("Total Dispense Weight (kg)", f"{round(total_dispense,1)}")

st.divider()

# -----------------------
# Altitude & Discharge Selection (with indicator)
# -----------------------
st.subheader("📏 Select Altitude (m)")

altitudes = [1.5, 2, 2.5, 3, 3.5, 4]

st.radio(
    "",
    altitudes,
    key="selected_altitude",
    horizontal=True
)
st.subheader("💧 Select Discharge Rate (%)")

rates = [30, 40, 50, 60, 70, 80, 90, 100]

st.radio(
    "",
    rates,
    key="selected_rate",
    horizontal=True
)
# -----------------------
# Shape Selection (UNCHANGED)
# -----------------------
st.subheader("🗺 Select Field Shape")

shape_data = {
    "Square": {"file": "square.png", "turns": 16},
    "Rectangle": {"file": "rectangle.png", "turns": 13},
    "Skewed": {"file": "skewed.png", "turns": 10},
    "L Shape": {"file": "lshape.png", "turns": 18},
}

shape_names = list(shape_data.keys())

for shape in shape_names:
    if st.session_state.get(f"clicked_{shape}", False):
        st.session_state.selected_shape = shape
        st.session_state[f"clicked_{shape}"] = False

cols = st.columns(len(shape_names))

for shape, col in zip(shape_names, cols):
    with col:
        is_selected = st.session_state.selected_shape == shape
        circle = "🔴" if is_selected else "⚪"

        if st.button(
            f"{circle}  {shape}",
            key=f"btn_{shape}",
            use_container_width=True
        ):
            st.session_state[f"clicked_{shape}"] = True

        st.image(shape_data[shape]["file"], width=130)

selected_shape = st.session_state.selected_shape
N = shape_data[selected_shape]["turns"]

st.caption(f"Turns Applied: {N}")

st.divider()

# -----------------------
# Nozzle Constants (TEMPORARY FIXED AS REQUESTED)
# -----------------------
if selected_nozzle == "Centrifugal":
    SWATH_WIDTH = 5.5
    FLOW_RATE = 3.0
else:
    SWATH_WIDTH = 4.0
    FLOW_RATE = 2.307

TURN_LOSS = 0.00
ACRE_M2 = 4046.86

# -----------------------
# Calculations
# -----------------------
t_spray = ((total_dispense / FLOW_RATE) * 60) - (N * 4)

A_ideal = (SWATH_WIDTH * t_spray) / ACRE_M2

A_real = A_ideal * ((1 - TURN_LOSS) ** N)

v_required = (st.session_state.acres * ACRE_M2) / (
    SWATH_WIDTH * t_spray * ((1 - TURN_LOSS) ** N)
)

v_required = round(v_required, 1)

# -----------------------
# Output
# -----------------------
st.subheader("📊 Results")

c1, c2 = st.columns(2)

with c2:
    st.metric("Required Speed (m/s)", f"{v_required}")
    st.metric("Swath Width (m)", f"{SWATH_WIDTH}")

st.caption(
    "Model:\n"
    "Total Weight = kg/acre × acres\n"
    "Speed = Area / (Swath × SprayTime × TurnEfficiency)\n\n"
    "Turn loss fixed at 2% per turn."
)










