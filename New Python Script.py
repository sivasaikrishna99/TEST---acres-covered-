import streamlit as st

st.set_page_config(page_title="Agri Drone Area Calculator", layout="centered")
st.title("🚁 Agricultural Drone Area Coverage Calculator")
st.caption("Single-turn efficiency model (Turn loss fixed at 2%)")

st.divider()

# -----------------------
# Defaults
# -----------------------
defaults = {
    "speed": 5.0,
    "width": 5.5,
    "flow": 3.0,
    "tank": 10.0,
}

for k, v in defaults.items():
    st.session_state.setdefault(k, v)
    st.session_state.setdefault(f"{k}_slider", v)
    st.session_state.setdefault(f"{k}_input", v)

if "selected_shape" not in st.session_state:
    st.session_state.selected_shape = "Square"

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
# Inputs
# -----------------------
synced_input("Speed (m/s)", "speed", 0.5, 15.0, 0.1)
synced_input("Swath width (m)", "width", 0.5, 15.0, 0.1)
synced_input("Flow rate (kg/min)", "flow", 0.1, 20.0, 0.001, "%.4f")
synced_input("Total Dispense weight (kg)", "tank", 1.0, 50.0, 0.5)

st.divider()

# -----------------------
# Shape Selection (Professional Clickable Cards)
# -----------------------
st.subheader("🗺 Select Field Shape")

shape_data = {
    "Square": {"file": "square.png", "turns": 16},
    "Rectangle": {"file": "rectangle.png", "turns": 12},
    "Skewed": {"file": "skewed.png", "turns": 11},
    "L Shape": {"file": "lshape.png", "turns": 18},
}

shape_names = list(shape_data.keys())

# Ensure default selection
if "selected_shape" not in st.session_state:
    st.session_state.selected_shape = shape_names[0]

cols = st.columns(len(shape_names))

for shape, col in zip(shape_names, cols):
    with col:

        is_selected = st.session_state.selected_shape == shape

        border_color = "#d32f2f" if is_selected else "#cccccc"
        background = "#fff5f5" if is_selected else "white"

        # Card container
        st.markdown(
            f"""
            <div style="
                border: 3px solid {border_color};
                border-radius: 10px;
                padding: 10px;
                background-color: {background};
                text-align: center;
            ">
            """,
            unsafe_allow_html=True
        )

        if st.button("Select", key=f"card_{shape}", use_container_width=True):
            st.session_state.selected_shape = shape
            st.rerun()

        st.image(shape_data[shape]["file"], width=130)

        st.markdown(
            f"<div style='margin-top:5px; font-weight:500;'>{shape}</div>",
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

# Apply turns
selected_shape = st.session_state.selected_shape
N = shape_data[selected_shape]["turns"]

st.caption(f"Turns Applied: {N}")
# -----------------------
# Calculations (UNCHANGED)
# -----------------------
v = st.session_state.speed
w = st.session_state.width
flow = st.session_state.flow
tank = st.session_state.tank

turn_loss_percent = 2.0
efficiency_per_turn = 1 - (turn_loss_percent / 100)

t_spray = (tank / flow) * 60
A_ideal = (v * w * t_spray) / 4046.86
A_real = A_ideal * (efficiency_per_turn ** N)

# -----------------------
# Output
# -----------------------
st.subheader("📊 Results")

c1, c2 = st.columns(2)

with c2:
    st.metric("Actual Area (acre)", f"{A_real:.4f}")

st.caption(
    "Model:\n"
    "A_real = A_ideal × (1 - 0.02) ^ N\n\n"
    "Turn loss fixed at 2% per turn."
)










