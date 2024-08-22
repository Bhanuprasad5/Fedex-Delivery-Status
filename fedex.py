import streamlit as st
import pandas as pd
import pickle

# Load the model
model = pickle.load(open(r"Fedex.pkl", 'rb'))

# Set page config
st.set_page_config(page_title="FedEx Delivery Status Prediction", layout="centered")

# Custom CSS to enhance appearance
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        max-width: 800px;
        margin: 0 auto;
        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background-color: #007BFF;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .input-box {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    }
    .st-selectbox label, .st-number-input label, .st-text-input label {
        font-weight: bold;
        color: #333;
    }
    .st-selectbox, .st-number-input, .st-text-input {
        border-radius: 5px;
    }
    .title-box {
        text-align: center;
        margin-bottom: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.markdown("<div class='title-box'><h1>FedEx Delivery Status Prediction 🚚</h1></div>", unsafe_allow_html=True)

# Subtitle
st.subheader("Predict whether your FedEx shipment will be on time or delayed")

# Numerical Features
st.markdown("### Enter Numerical Features")
numerical_features = ['Carrier_Num', 'Distance']
input_data = {}

for feature in numerical_features:
    with st.container():
        st.markdown(f"<div class='input-box'><label>{feature}</label>", unsafe_allow_html=True)
        input_data[feature] = st.number_input(f'{feature}', min_value=0, max_value=10000, value=0)
        st.markdown("</div>", unsafe_allow_html=True)

# Categorical Features
st.markdown("### Select Categorical Features")
categorical_features = {
    'Year': [2008],
    'Month': [1, 2, 3, 4, 5, 6],
    'DayofMonth': list(range(1, 32)),
    'DayOfWeek': list(range(1, 8)),
    'Carrier_Name': ['WN', 'XE', 'YV', 'OH', 'OO', 'UA', 'US', 'DL', 'EV', 'F9', 'FL', 'HA', 'MQ', 'NW', '9E', 'AA', 'AQ', 'AS', 'B6', 'CO']
}
for feature, options in categorical_features.items():
    with st.container():
        st.markdown(f"<div class='input-box'><label>{feature}</label>", unsafe_allow_html=True)
        input_data[feature] = st.selectbox(f'{feature}', options)
        st.markdown("</div>", unsafe_allow_html=True)

# Text Inputs for Source and Destination
st.markdown("### Enter Shipment Details")
categories = ['Source', 'Destination']
for feature in categories:
    with st.container():
        st.markdown(f"<div class='input-box'><label>{feature}</label>", unsafe_allow_html=True)
        input_data[feature] = st.text_input(f"{feature}")
        st.markdown("</div>", unsafe_allow_html=True)

# Time Inputs
st.markdown("### Enter Time Details (in Hours and Minutes)")

def get_time_input(label, key_suffix):
    with st.container():
        st.markdown(f"<div class='input-box'><label>{label}</label>", unsafe_allow_html=True)
        hours = st.selectbox("Hours", list(range(0, 24)), key=f"hours_{key_suffix}")
        minutes = st.selectbox("Minutes", list(range(0, 60)), key=f"minutes_{key_suffix}")
        st.markdown("</div>", unsafe_allow_html=True)
    return hours * 60 + minutes

input_data['Actual_Shipment_Time'] = get_time_input("Actual Shipment Time", "1")
input_data['Planned_Shipment_Time'] = get_time_input("Planned Shipment Time", "2")
input_data['Planned_Delivery_Time'] = get_time_input("Planned Delivery Time", "3")
input_data['Planned_TimeofTravel'] = get_time_input("Planned Time of Travel", "4")
input_data['Shipment_Delay'] = get_time_input("Shipment Delay Time", "5")

# DataFrame to hold input data
input_df = pd.DataFrame([input_data])

# Predict Button
if st.button('Predict Delivery Status'):
    prediction = model.predict(input_df)
    status = "On Time" if int(prediction[0]) == 1 else "Delayed"
    st.markdown(f"## Prediction: **{status}**")

    # Display Image Based on Prediction
    if int(prediction[0]) == 1:
        st.image(r"_48d14ee4-11a2-46a8-b205-65fad183fa68.jpeg", width=400, caption="Your delivery is on time! 🚀")
    else:
        st.image(r"_94d74535-a96e-4e10-be4b-f264ecf6c07a.jpeg", width=400, caption="Your delivery is delayed. 😞")

# Footer
st.markdown("""
    <hr>
    <footer style='text-align: center;'>
        <p style='color: #666;'>FedEx Delivery Status Prediction | Powered by Streamlit</p>
    </footer>
    """, unsafe_allow_html=True)
