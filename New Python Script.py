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
# Shape Selection (Improved Visual Radio)
# -----------------------
st.subheader("🗺 Select Field Shape")

shape_data = {
    "Square": {"file": "square.png", "turns": 16},
    "Rectangle": {"file": "rectangle.png", "turns": 12},
    "Skewed": {"file": "skewed.png", "turns": 11},
    "L Shape": {"file": "lshape.png", "turns": 18},
}

shape_names = list(shape_data.keys())

cols = st.columns(len(shape_names))

for shape, col in zip(shape_names, cols):
    with col:

        is_selected = st.session_state.selected_shape == shape

        # Custom radio circle (red when selected)
        circle_html = f"""
        <div style="
            width:18px;
            height:18px;
            border-radius:50%;
            border:2px solid #d32f2f;
            display:inline-block;
            margin-right:6px;
            vertical-align:middle;
            position:relative;
        ">
            {"<div style='width:10px;height:10px;background:#d32f2f;border-radius:50%;position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);'></div>" if is_selected else ""}
        </div>
        """

        if st.button(shape, key=f"shape_btn_{shape}"):
            st.session_state.selected_shape = shape

        st.markdown(
            f"<div style='display:flex;align-items:center;justify-content:center;margin-top:-32px;'>{circle_html}<span style='font-size:14px;'>{shape}</span></div>",
            unsafe_allow_html=True
        )

        st.image(shape_data[shape]["file"], width=130)

# Apply turns based on selected shape
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

