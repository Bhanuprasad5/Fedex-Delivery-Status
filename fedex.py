import streamlit as st
import pandas as pd
import pickle

# Load the pre-trained model
model = pickle.load(open(r"Fedex.pkl", 'rb'))

# Set the title and subtitle
st.title("FedEx Delivery Status Prediction")
st.subheader("Predict the status of your FedEx delivery with ease")

# Add a sidebar for inputs
st.sidebar.header("Input Shipment Details")
st.sidebar.write("Fill in the following details to predict the delivery status")

# Define features
numerical_features = ['Carrier_Num', 'Distance']
categorical_features = {
    'Year': [2008],
    'Month': list(range(1, 13)),  # Updated for all months
    'DayofMonth': list(range(1, 32)),
    'DayOfWeek': list(range(1, 8)),
    'Carrier_Name': ['WN', 'XE', 'YV', 'OH', 'OO', 'UA', 'US', 'DL', 'EV', 'F9', 'FL',
                     'HA', 'MQ', 'NW', '9E', 'AA', 'AQ', 'AS', 'B6', 'CO']
}
categories = ['Source', 'Destination']

# Collect user inputs
input_data = {}
for feature in numerical_features:
    input_data[feature] = st.sidebar.number_input(f'Enter value for {feature}', min_value=0.0)

for feature, options in categorical_features.items():
    input_data[feature] = st.sidebar.selectbox(f'Select {feature}', options)

for feature in categories:
    input_data[feature] = st.sidebar.text_input(f"Enter {feature}")

# Time inputs
st.sidebar.write("Enter Times (in HH:MM format)")

# Function to get time in minutes
def get_time_in_minutes(label):
    hours = st.sidebar.selectbox(f"{label} Hours", list(range(0, 24)), key=label+"h")
    minutes = st.sidebar.selectbox(f"{label} Minutes", list(range(0, 60)), key=label+"m")
    return hours * 60 + minutes

# Input times
input_data['Actual_Shipment_Time'] = get_time_in_minutes("Actual Shipment Time")
input_data['Planned_Shipment_Time'] = get_time_in_minutes("Planned Shipment Time")
input_data['Planned_Delivery_Time'] = get_time_in_minutes("Planned Delivery Time")
input_data['Planned_TimeofTravel'] = get_time_in_minutes("Planned Time of Travel")
input_data['Shipment_Delay'] = get_time_in_minutes("Shipment Delay Time")

# Convert input data to DataFrame
input_df = pd.DataFrame([input_data])

# Display prediction
if st.button('Predict Delivery Status'):
    prediction = model.predict(input_df)
    if int(prediction[0]) == 1:
        st.success("Your delivery is predicted to be ON TIME!")
        #st.image(r"_48d14ee4-11a2-46a8-b205-65fad183fa68.jpeg", width=400)
    else:
        st.warning("Your delivery is predicted to be DELAYED!")
        #st.image(r"_94d74535-a96e-4e10-be4b-f264ecf6c07a.jpeg", width=400)

# Footer section
st.markdown("""
<style>
    footer {visibility: hidden;}
    .reportview-container .main .block-container{padding-top: 2rem;}
</style>
""", unsafe_allow_html=True)
