import streamlit as st
import math
Lapserate=0.0065
def single_iteration(V_knots, Tt_measured_k, Ts, Kr=1.0):
    """
    Perform one iteration to calculate Mach number using ATPL speed of sound formula.
    
    Args:
        V_knots (float): True airspeed in knots
        Tt_measured_k (float): Measured total temperature in Kelvin
        Ts (float): Current static temperature in Kelvin
        Kr (float): Recovery factor (default 1.0)
    
    Returns:
        tuple: (Mach number, calculated total temperature, new static temperature, temperature difference)
    """
    # Calculate speed of sound using ATPL formula: a = 38.95 * sqrt(Ts) (in knots)
    a = 38.95 * math.sqrt(Ts)
    
    # Calculate Mach number: M = V_knots / a
    M = V_knots / a
    
    Tt_calc = Ts * (1 + (0.2 * Kr * M**2))
    
    # Calculate temperature difference
    diff = abs(Tt_measured_k - Tt_calc)
    
    # Update static temperature: Ts_new = Ts + (Tt_measured_k - Tt_calc) * 0.5
    Ts_new = Ts + (Tt_measured_k - Tt_calc) * 0.5
    
    return M, Tt_calc, Ts_new, diff

# Streamlit GUI
st.title("✈️ Mach Number - Step by Step Iteration. ")
st.title(" Developed By:  -- Amr Ashraf --")
st.write("Calculate Mach number iteratively using the ISA model and ATPL speed of sound formula.")

# Input fields
velocity_knots = st.number_input("TAS (knots)", min_value=0.0, value=500.0, step=1.0)
altitude_ft = st.number_input("Altitude (ft)", min_value=0.0, value=15000.0, step=1000.0)
Tt_measured_c = st.number_input("Measured Total Temp (°C)", value=25.0, step=1.0)
Kr = st.number_input("Recovery Factor (Kr)", min_value=0.0, max_value=1.0, value=0.9, step=0.05)

# Convert inputs
altitude_m = altitude_ft * 0.3048  # ft to meters
Tt_measured_k = Tt_measured_c + 273  # °C to Kelvin

# Input validation
if velocity_knots < 0 or Tt_measured_k < 0 or Kr < 0 or Kr > 1:
    st.error("Invalid inputs: Velocity and temperature must be non-negative, and Kr must be between 0 and 1.")
    st.stop()

if 'Ts' not in st.session_state or 'last_inputs' not in st.session_state or st.session_state.last_inputs != (velocity_knots, altitude_ft, Tt_measured_c, Kr):
    
    st.session_state.Ts = 288.15 - Lapserate * altitude_m if altitude_m <= 11000 else 216.65
    st.session_state.iteration = 0
    st.session_state.last_inputs = (velocity_knots, altitude_ft, Tt_measured_c, Kr)

if st.button("🔁 Perform One Iteration"):
    M, Tt_calc, new_Ts, diff = single_iteration(
        velocity_knots, Tt_measured_k, st.session_state.Ts, Kr
    )
    st.session_state.iteration += 1
    st.session_state.Ts = new_Ts
    
    st.subheader("🔍 Current Iteration Result")
    st.write(f"**Iteration:** {st.session_state.iteration}")
    st.write(f"**Mach Number:** {M:.4f}")
    st.write(f"**Calculated Tt (K):** {Tt_calc:.2f}")
    st.write(f"**Static Temp (Ts) (K):** {new_Ts:.2f}")
    st.write(f"**Temp Difference (K):** {diff:.3f}")
    
    if diff < 0.1:
        st.success("Convergence achieved!")

# Reset button
if st.button("♻️ Reset"):
    st.session_state.Ts = 288.15 - Lapserate * altitude_m if altitude_m <= 11000 else 216.65
    st.session_state.iteration = 0
    st.session_state.last_inputs = (velocity_knots, altitude_ft, Tt_measured_c, Kr)
    st.success("State reset successfully.")