import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# Configure page
st.set_page_config(page_title="Pakistan Air Quality Dashboard", page_icon="🌤️", layout="wide")
st.title("🌤️ Pakistan Air Quality Dashboard")

# Cities data
CITIES = {
    "Lahore": {"lat": "31.5204", "lon": "74.3587"},
    "Karachi": {"lat": "24.8607", "lon": "67.0011"},
    "Islamabad": {"lat": "33.6844", "lon": "73.0479"},
    "Peshawar": {"lat": "34.0151", "lon": "71.5249"},
    "Quetta": {"lat": "30.1798", "lon": "66.9750"},
    "Multan": {"lat": "30.1575", "lon": "71.5249"},
    "Faisalabad": {"lat": "31.4504", "lon": "73.1350"},
    "Murree": {"lat": "33.9070", "lon": "73.3943"},
    "Toba Tek Singh": {"lat": "30.9667", "lon": "72.4833"}
}

# API settings
API_KEY = "7ffc2320232fa01f434ea3a84805ba37"

def get_air_quality_data(lat, lon):
    AIR_QUALITY_URL = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    try:
        response = requests.get(AIR_QUALITY_URL)
        response.raise_for_status()
        data = response.json()
        
        if 'list' not in data:
            st.error(f"Unexpected API response format: {data}")
            return None
            
        air_quality_data = []
        for item in data['list']:
            air_quality_data.append({
                'date': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M'),
                'aqi': item['main']['aqi'],
                'co': round(item['components']['co'], 2),
                'no': round(item['components']['no'], 2),
                'no2': round(item['components']['no2'], 2),
                'o3': round(item['components']['o3'], 2),
                'so2': round(item['components']['so2'], 2),
                'nh3': round(item['components']['nh3'], 2),
                'pm2_5': round(item['components']['pm2_5'], 1),
                'pm10': round(item['components']['pm10'], 1)
            })
        return pd.DataFrame(air_quality_data)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

def get_current_temperature(lat, lon, api_key):
    WEATHER_URL = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        response = requests.get(WEATHER_URL)
        data = response.json()
        return round(data['main']['temp'], 1)
    except Exception as e:
        st.error(f"Error fetching temperature data: {e}")
        return None

# Add city selector in sidebar
selected_city = st.sidebar.selectbox("Select City", list(CITIES.keys()))

# Get data for selected city
city_data = CITIES[selected_city]
air_quality_df = get_air_quality_data(city_data["lat"], city_data["lon"])

if air_quality_df is not None:
    # Display city name and temperature
    current_temp = get_current_temperature(city_data["lat"], city_data["lon"], API_KEY)
    if current_temp is not None:
        st.markdown(f"""
            <h2 style='text-align: center; margin-bottom: 1rem;'>
                {selected_city}<br>
                <span style='font-size: 1.5rem; color: #666;'>
                    Current Temperature: {current_temp}°C
                </span>
            </h2>
        """, unsafe_allow_html=True)

    # Display AQI Level and recommendations
    current_aqi = air_quality_df['aqi'].iloc[0]
    aqi_labels = {
        1: "Good 😊",
        2: "Fair 🙂",
        3: "Moderate 😐",
        4: "Poor 😷",
        5: "Very Poor 🤢"
    }
    aqi_colors = {
        1: "green",
        2: "yellow",
        3: "orange",
        4: "red",
        5: "purple"
    }
    aqi_recommendations = {
        1: {
            "message": "✅ It's safe to go outside!",
            "details": "Air quality is good. Perfect for outdoor activities."
        },
        2: {
            "message": "✅ Generally safe for outdoor activities",
            "details": "Sensitive individuals should consider reducing prolonged outdoor exertion."
        },
        3: {
            "message": "⚠️ Take Precautions",
            "details": "Wear a mask if going outside. Consider limiting outdoor activities."
        },
        4: {
            "message": "❌ Stay Indoors Recommended",
            "details": "Avoid outdoor activities. If you must go out, wear a proper mask."
        },
        5: {
            "message": "🚫 Avoid Outdoor Activities",
            "details": "Hazardous air quality. Stay indoors and keep windows closed. Use air purifiers if available."
        }
    }

    # Display AQI Level
    st.markdown("""
        <h2 style='text-align: center; margin-bottom: 2rem;'>
            Current AQI Level:<br>
            <span style='font-size: 2.5rem; font-weight: 700; color: {}'>
                {}
            </span>
        </h2>
    """.format(aqi_colors[current_aqi], aqi_labels[current_aqi]), unsafe_allow_html=True)
    
    # Display Alert Box
    alert_color = aqi_colors[current_aqi]
    st.markdown(f"""
        <div style='
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
            background-color: {alert_color}20;
            border: 2px solid {alert_color};
        '>
            <h3 style='
                color: {alert_color};
                margin: 0;
                font-size: 1.5rem;
                font-weight: bold;
            '>
                {aqi_recommendations[current_aqi]['message']}
            </h3>
            <p style='
                margin: 0.5rem 0 0 0;
                color: {alert_color};
                font-size: 1.1rem;
            '>
                {aqi_recommendations[current_aqi]['details']}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Display PM2.5 and PM10 current values
    st.subheader("Particulate Matter")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Current PM2.5",
            f"{air_quality_df['pm2_5'].iloc[0]:.1f} μg/m³"
        )
    with col2:
        st.metric(
            "Current PM10",
            f"{air_quality_df['pm10'].iloc[0]:.1f} μg/m³"
        )

# Display last update time
st.sidebar.markdown("---")
st.sidebar.write("Last updated:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# Update the sidebar information
st.sidebar.markdown("""
### Dashboard Information
- Shows air quality data for major cities in Pakistan
- Pollutant levels are in μg/m³
- AQI Scale:
  - 1 = Good (Safe for outdoor activities)
  - 2 = Fair (Generally safe)
  - 3 = Moderate (Take precautions)
  - 4 = Poor (Stay indoors recommended)
  - 5 = Very Poor (Avoid outdoor activities)
""")

