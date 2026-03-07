import streamlit as st
import joblib
import serial
import time
import pandas as pd

st.set_page_config(page_title="AI Downtime Monitoring", layout="wide")

st.title("⚙ AI-Based Machine Downtime Classification System")

model = joblib.load("downtime_model.pkl")

# Initialize session state
if "index" not in st.session_state:
    st.session_state.index = 0

if "history" not in st.session_state:
    st.session_state.history = []

# Simulated realistic pattern
pattern = [25, 28, 30, 32, 35, 38, 42, 45, 50, 60, 75, 90, 95, 85, 70, 55, 40, 35, 30, 28]

sensor_value = pattern[st.session_state.index % len(pattern)]

prediction = model.predict([[sensor_value]])
probability = model.predict_proba([[sensor_value]])[0][1] * 100

st.session_state.history.append(sensor_value)

col1, col2 = st.columns(2)

with col1:
    st.metric("Live Sensor Value", sensor_value)
    st.progress(int(probability))
    st.write(f"Failure Probability: {probability:.2f}%")

with col2:
    if prediction[0] == 1:
        st.error("⚠ FAILURE DETECTED")
        status = '1'
    else:
        st.success("System Normal")
        status = '0'

        # Initialize Arduino once
if "arduino" not in st.session_state:
    try:
        st.session_state.arduino = serial.Serial('COM6', 9600)
        time.sleep(2)
    except:
        st.warning("Arduino not connected")

# Send signal only if status changes
if "last_status" not in st.session_state:
    st.session_state.last_status = None

try:
    if st.session_state.last_status != status:
        st.session_state.arduino.write(status.encode())
        st.session_state.last_status = status
except:
    pass

# Chart
df = pd.DataFrame(st.session_state.history, columns=["Sensor Value"])
st.line_chart(df)

# Arduino Control
if "arduino" not in st.session_state:
    try:
        st.session_state.arduino = serial.Serial('COM5', 9600)  # change if needed
        time.sleep(2)
    except:
        st.warning("Arduino not connected")

# Move to next value
st.session_state.index += 1

# Auto refresh every 2 seconds
time.sleep(2)
st.rerun()