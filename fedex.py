import streamlit as st
import pandas as pd
import pickle
from PIL import Image

# Load the pre-trained model
model = pickle.load(open("Fedex.pkl", 'rb'))

# Custom CSS to enhance visual appeal
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #ECE9E6, #FFFFFF);
        font-family: 'Arial', sans-serif;
        color: #333;
    }
    .title {
        
        font-size: 2.5rem;
        text-align: center;
        font-weight: bold;
    }
    .subheader {
        color: #555;
        font-size: 1.5rem;
        margin-bottom: 30px;
    }
    .stButton button {
        background-color: #FF5733;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 20px;
        font-size: 1rem;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #C70039;
    }
    .stSidebar {
        background-color: #F5F5F5;
        padding: 20px;
    }
    .stSidebar h3 {
        color: #333;
        margin-top: 0;
    }
    </style>
""", unsafe_allow_html=True)

# Set the title and subtitle with enhanced styles
st.markdown("<div class='title'>FedEx Delivery Status Prediction</div>", unsafe_allow_html=True)

# Display FedEx logo/image with optimized sizing
st.image("573326-innomatics_research_labs_logo.png", width=150)

# Display a background image with reduced width to fit the design
image = Image.open("fedex.png")
st.image(image, use_column_width=True)

st.markdown("<div class='subheader'>Predict the status of your FedEx delivery with ease</div>", unsafe_allow_html=True)

# Add a sidebar for inputs with custom styled header
st.sidebar.markdown("<h3>Input Shipment Details</h3>", unsafe_allow_html=True)
st.sidebar.write("Fill in the following details to predict the delivery status")

# Define features with improved descriptions
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

# Function to get time in minutes with enhanced UI
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

# Debug: Display the input DataFrame with improved UI
st.markdown("### Input DataFrame for Debugging")
st.dataframe(input_df.style.set_properties(**{'background-color': '#f0f0f0', 'color': 'black'}))

# Display prediction with styled buttons and feedback
if st.button('Predict Delivery Status'):
    try:
        prediction = model.predict(input_df)
        if int(prediction[0]) == 1:
            st.success("Your delivery is predicted to be ON TIME!")
            st.image("delivered.jpeg", width=400, caption="Your delivery is on time! 🚀")
        else:
            st.warning("Your delivery is predicted to be DELAYED!")
            st.image("not.jpeg", width=400, caption="Your delivery is delayed. 😞")
    except ValueError as e:
        st.error(f"Prediction failed: {str(e)}")
