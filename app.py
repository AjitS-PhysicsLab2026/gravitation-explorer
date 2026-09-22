import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# Page setup for a modern web look with your name on the browser tab
st.set_page_config(page_title="Ajit's Gravitation Studio", layout="centered")
st.title("🪐 Ajit's  Gravitation Studio")
st.write("A customized dashboard for calculating gravitation metrics and orbital mechanics.")

# --- SIDEBAR INPUTS ---
st.sidebar.header("📝 1. Parameters")

planet_mode = st.sidebar.radio(
    "Select Planet Environment:",
    ["Earth (JEE Constants: R=6400km, M=6e24kg)", "Custom Planet Specs"]
)

if planet_mode == "Custom Planet Specs":
    M = float(st.sidebar.text_input("Custom Mass (M in kg):", "7.342e22"))
    R_km = float(st.sidebar.text_input("Custom Radius (R in km):", "1737"))
    R = R_km * 1000
else:
    M = 6.0e24
    R = 6400000.0  # 6400 km in meters

m = st.sidebar.slider("Mass of Object (m in kg):", min_value=10, max_value=5000, value=500, step=50)

# Toggle between Slider or Manual Entry for Height
height_input_type = st.sidebar.radio("Height Input Method:", ["Slider Control", "Type Manually (Text Box)"])

if height_input_type == "Slider Control":
    h_km = st.sidebar.slider("Height Above Surface (h in km):", min_value=0, max_value=40000, value=1600, step=100)
else:
    h_km_input = st.sidebar.text_input("Type Height Above Surface (h in km):", "36000")
    try:
        h_km = float(h_km_input)
    except ValueError:
        st.sidebar.error("Please enter a valid number for height.")
        h_km = 0.0

case_choice = st.sidebar.radio(
    "Select Object State:",
    ["Case 1: Standard Object", "Case 2: Revolving Satellite"]
)

# Checkbox to show/hide the graph
show_graph = st.checkbox("📈 Show Theoretical Curve Graph", value=False)

if show_graph:
    graph_to_view = st.selectbox(
        "📊 Select Physics Graph to View:",
        ["Value of 'g'", "Potential Energy", "Critical Velocity"]
    )

# --- CORE PHYSICS ENGINE ---
G = 6.6743e-11
h_meters = h_km * 1000
r_current = R + h_meters

# Calculations for numerical metrics
g_at_h = (G * M) / (r_current ** 2)
p_e = - (G * M * m) / r_current

# Total theoretical escape velocity from distance r (in m/s)
v_e_total = math.sqrt((2 * G * M) / r_current)

if case_choice == "Case 2: Revolving Satellite":
    v_c = math.sqrt((G * M) / r_current)
    needed_v_e = v_e_total - v_c  # Satellite formula: v_e - v_c
    vc_text = f"{v_c / 1000:.3f} km/s"  # 👈 DEVELOPER FIX: Converted to km/s
    escape_label = "Additional velocity required to break free from orbit"
else:
    v_c = 0.0
    needed_v_e = v_e_total  # 👈 DEVELOPER FIX: Standard object requires full v_e to escape from rest
    vc_text = "N/A (Not Orbiting)"
    escape_label = "Total escape velocity required to escape from rest at this height"

# Convert escape velocity to km/s for end-user display
needed_v_e_km_s = needed_v_e / 1000  # 👈 DEVELOPER FIX: Converted to km/s

# Displaying Numerical Outputs in crisp dashboard blocks
st.subheader("📊 Live Numerical Outputs")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Value of 'g' at height 'h'", value=f"{g_at_h:.4f} m/s²")
    st.metric(label="Potential Energy (P.E.)", value=f"{p_e:.2e} J")
with col2:
    st.metric(label="Critical Velocity (v_c)", value=vc_text)
    st.metric(label="Additional Escape Velocity Needed", value=f"{needed_v_e_km_s:.3f} km/s", help=escape_label)

# --- CONDITIONAL GRAPHING ENGINE ---
if show_graph:
    st.write("---")
    r_vals = np.linspace(0.01, R * 8, 500)
    y_vals = []
    
    for r in r_vals:
        if graph_to_view == "Value of 'g'":
            y = (G * M / R**3) * r if r <= R else (G * M) / r**2
            title, ylabel, unit = "Acceleration due to Gravity ('g')", "g", "m/s²"
            current_y = (G * M / R**3) * r_current if r_current <= R else (G * M) / r_current**2
        elif graph_to_view == "Potential Energy":
            y = - (G * M * m / (2 * R**3)) * (3 * R**2 - r**2) if r <= R else - (G * M * m) / r
            title, ylabel, unit = "Gravitational Potential Energy (P.E.)", "P.E.", "Joules"
            current_y = - (G * M * m / (2 * R**3)) * (3 * R**2 - r_current**2) if r_current <= R else - (G * M * m) / r_current
        else:
            y = math.sqrt(G * M / R**3) * r if r <= R else math.sqrt(G * M / r)
            # Convert graph values to km/s for consistency if plotting velocity
            y = y / 1000
            title, ylabel, unit = "Critical Velocity (v_c)", "v_c", "km/s"
            current_y = (math.sqrt(G * M / R**3) * r_current if r_current <= R else math.sqrt(G * M / r_current)) / 1000
        y_vals.append(y)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(r_vals / 1000, y_vals, color="#1A73E8", linewidth=2.5, label="Physics Curve")
    ax.axvline(x=R / 1000, color="red", linestyle="--", label="Planet Surface (R)")
    ax.plot(r_current / 1000, current_y, "go", markersize=8, label="Your Object Position")
    
    ax.set_title(f"{title} vs Distance from Center", fontsize=12, fontweight='bold')
    ax.set_xlabel("Distance from Center (r in km)", fontsize=10)
    ax.set_ylabel(f"{ylabel} ({unit})", fontsize=10)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend()
    
    st.pyplot(fig)
