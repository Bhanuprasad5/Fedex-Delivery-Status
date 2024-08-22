import streamlit as st
import pandas as pd
import pickle

# Load the prediction model
model = pickle.load(open("Fedex.pkl", 'rb'))

# Page configuration
st.set_page_config(page_title="FedEx Delivery Status Prediction", page_icon="🚚", layout="centered")

# Title and description
st.title("🚚 FedEx Delivery Status Prediction")
st.markdown("""
Welcome to the FedEx Delivery Status Prediction app. 
Please fill in the details below to predict the delivery status of your shipment.
""")

# Custom styling
st.markdown("""
<style>
    .main { 
        background-color: #f7f7f7; 
        color: #333;
    }
    .stTextInput > div > div > input {
        background-color: #e3f2fd;
    }
    .stNumberInput > div > div > input {
        background-color: #e3f2fd;
    }
    .stSelectbox > div > div {
        background-color: #e3f2fd;
    }
    .stButton > button {
        background-color: #1976d2;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Input sections with titles
st.header("Shipment Details")

numerical_features = ['Carrier Number', 'Distance']
categorical_features = {
    'Year': [2008], 
    'Month': [1, 2, 3, 4, 5, 6],  
    'Day of Month': list(range(1, 32)),
    'Day of Week': list(range(1, 8)),  
    'Carrier Name': ['WN', 'XE', 'YV', 'OH', 'OO', 'UA', 'US', 'DL', 'EV', 'F9', 'FL', 'HA', 'MQ', 'NW', '9E', 'AA', 'AQ', 'AS', 'B6', 'CO']
}
categories = ['Source', 'Destination']

input_data = {}
for feature in numerical_features:
    input_data[feature] = st.number_input(f'Enter value for {feature}', min_value=0)

for feature, options in categorical_features.items():
    input_data[feature] = st.selectbox(f'Select {feature}', options)

for feature in categories:
    input_data[feature] = st.text_input(f"Enter {feature}")

# Time inputs
st.header("Time Details")

st.subheader("Actual Shipment Time")
hours1 = st.selectbox("Hours", list(range(0, 24)), key="hours1")
minutes1 = st.selectbox("Minutes", list(range(0, 60)), key="minutes1")
total_minutes1 = hours1 * 60 + minutes1

st.subheader("Planned Shipment Time")
hours2 = st.selectbox("Hours", list(range(0, 24)), key="hours2")
minutes2 = st.selectbox("Minutes", list(range(0, 60)), key="minutes2")
total_minutes2 = hours2 * 60 + minutes2

st.subheader("Planned Delivery Time")
hours3 = st.selectbox("Hours", list(range(0, 24)), key="hours3")
minutes3 = st.selectbox("Minutes", list(range(0, 60)), key="minutes3")
total_minutes3 = hours3 * 60 + minutes3

st.subheader("Planned Time of Travel")
hours4 = st.selectbox("Hours", list(range(0, 12)), key="hours4")
minutes4 = st.selectbox("Minutes", list(range(0, 60)), key="minutes4")
total_minutes4 = hours4 * 60 + minutes4

st.subheader("Shipment Delay Time")
hours5 = st.selectbox("Hours", list(range(0, 43)), key="hours5")
minutes5 = st.selectbox("Minutes", list(range(0, 60)), key="minutes5")
total_minutes5 = hours5 * 60 + minutes5

# Store time inputs in input_data dictionary
input_data['Actual_Shipment_Time'] = total_minutes1
input_data['Planned_Shipment_Time'] = total_minutes2
input_data['Planned_Delivery_Time'] = total_minutes3
input_data['Planned_TimeofTravel'] = total_minutes4
input_data['Shipment_Delay'] = total_minutes5

# Convert input_data to DataFrame
input_df = pd.DataFrame([input_data])

# Prediction
if st.button('Predict Delivery Status'):
    prediction = model.predict(input_df)
    st.write(f'**Prediction:** {"On-Time" if int(prediction[0]) == 1 else "Delayed"}')
    
    if int(prediction[0]) == 1:
        st.image("path/to/your/on-time-image.jpeg", width=400)
    else:
        st.image("path/to/your/delayed-image.jpeg", width=400)
