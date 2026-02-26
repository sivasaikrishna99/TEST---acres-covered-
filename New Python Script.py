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

import streamlit as st
import streamlit.components.v1 as components
import base64
import json

# -----------------------
# Helper: Convert image to base64
# -----------------------
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# -----------------------
# Shape Data
# -----------------------
shape_data = {
    "Square": {"file": "square.png", "turns": 16},
    "Rectangle": {"file": "rectangle.png", "turns": 12},
    "Skewed": {"file": "skewed.png", "turns": 11},
    "L Shape": {"file": "lshape.png", "turns": 18},
}

if "selected_shape" not in st.session_state:
    st.session_state.selected_shape = "Square"

# Encode images
images = {
    name: get_base64_image(data["file"])
    for name, data in shape_data.items()
}

# -----------------------
# HTML Component
# -----------------------
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
.container {{
    display: flex;
    gap: 20px;
}}

.shape {{
    text-align: center;
    cursor: pointer;
}}

.shape img {{
    width: 140px;
    border-radius: 10px;
    border: 4px solid transparent;
}}

.shape.selected img {{
    border: 4px solid #d32f2f;
}}

.label {{
    margin-top: 6px;
    font-weight: 500;
}}
</style>
</head>
<body>

<div class="container">
"""

for name, img in images.items():
    selected_class = "selected" if st.session_state.selected_shape == name else ""
    html_code += f"""
    <div class="shape {selected_class}" onclick="selectShape('{name}')">
        <img src="data:image/png;base64,{img}">
        <div class="label">{name}</div>
    </div>
    """

html_code += f"""
</div>

<script>
const streamlit = window.parent;

function selectShape(shape) {{
    streamlit.postMessage({{
        type: "streamlit:setComponentValue",
        value: shape
    }}, "*");
}}
</script>

</body>
</html>
"""

selected = components.html(html_code, height=260)

# -----------------------
# Update session state
# -----------------------
if selected:
    st.session_state.selected_shape = selected

selected_shape = st.session_state.selected_shape
N = shape_data[selected_shape]["turns"]

st.write("Selected Shape:", selected_shape)
st.write("Turns Applied:", N)
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













