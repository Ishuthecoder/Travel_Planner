import streamlit as st
import requests
from datetime import datetime
from groq import Groq

# API Keys
OPENTRIPMAP_API_KEY = "5ae2e3f221c38a28845f05b6d9a4fa487c8eca54e731c783daf94147"
OPENWEATHER_API_KEY = "34178a7533b9f3cda834b7c19348049f"
GROQ_API_KEY = "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"

# Initialize Groq Client
groq_client = Groq(api_key=GROQ_API_KEY)

# Function to generate structured travel plan using Groq LLaMA 3-70B
def generate_travel_plan(destination, budget, refined_interests, duration, attractions, hotels, restaurants, weather):
    prompt = f"""
    Generate a structured {duration}-day travel itinerary for {destination} based on the following details:
    
    *Budget:* {budget}
    *Interests (Refined):* {', '.join(refined_interests)}
    *Duration:* {duration} days
    
    *Top Attractions:*
    {', '.join(attractions) if attractions else 'No attractions found'}
    
    *Top Hotels:*
    {', '.join(hotels) if hotels else 'No hotels found'}
    
    *Top Restaurants:*
    {', '.join(restaurants) if restaurants else 'No restaurants found'}
    
    *Weather Forecast:* {weather}
    
    Provide the itinerary in a structured day-wise format, suggesting activities for each day, including morning, afternoon, and evening plans.
    """
    
    response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "system", "content": "You are an AI travel planner that structures travel details in a readable format."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# Function to get location data
def get_location_data(place):
    url = f"https://api.opentripmap.com/0.1/en/places/geoname?name={place}&apikey={OPENTRIPMAP_API_KEY}"
    response = requests.get(url).json()
    return response if 'lat' in response and 'lon' in response else None

# Function to fetch attractions, hotels, and restaurants
def get_places(lat, lon, kind):
    url = f"https://api.opentripmap.com/0.1/en/places/radius?radius=10000&lon={lon}&lat={lat}&kinds={kind}&apikey={OPENTRIPMAP_API_KEY}"
    response = requests.get(url).json()
    return [place['properties'].get('name') for place in response.get("features", []) if place['properties'].get('name')]

# Function to get weather
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    if 'main' in response:
        temp = response['main']['temp']
        humidity = response['main']['humidity']
        wind_speed = response['wind']['speed']
        description = response['weather'][0]['description'].capitalize()
        
        season_recommendation = ""
        if temp >= 20 and temp <= 30:
            season_recommendation = "The weather is ideal for travel!"
        elif temp < 20:
            season_recommendation = "It might be a bit chilly, pack accordingly."
        else:
            season_recommendation = "It could be quite hot, stay hydrated and wear light clothing."
        
        return f"Temperature: {temp}°C, {description}. Humidity: {humidity}%. Wind Speed: {wind_speed} m/s. {season_recommendation}"
    return "Weather data not available."

# Function to refine user input
def refine_user_preferences(interests):
    refined_interests = []
    for interest in interests:
        if interest == "Adventure":
            choice = st.selectbox("Which type of adventure?", ["Trekking", "Water Sports", "Amusement Parks"])
            refined_interests.append(choice)
        elif interest == "Mix of famous and offbeat places":
            choice = st.radio("Do you want more famous places or hidden gems?", ["More Famous", "More Hidden Gems"])
            refined_interests.append(f"Mix: {choice}")
        else:
            refined_interests.append(interest)
    return refined_interests

# Streamlit UI
st.title("Travel TaskBot")
st.write("Plan your trip with AI-powered insights!")

destination = st.text_input("Enter Destination (City/Country):")
budget = st.radio("Select Your Budget:", ["Low", "Medium", "High"])
interests = st.multiselect("Select Your Interests:", ["Adventure", "Historical", "Food", "Nature", "Relaxation", "Shopping", "Mix of famous and offbeat places"])
duration = st.number_input("Enter Trip Duration (in days):", min_value=1, max_value=30, value=3)

if interests:
    refined_interests = refine_user_preferences(interests)
    st.write("Your refined interests:", refined_interests)

if st.button("Generate Travel Plan") and destination:
    st.subheader(f"Top Attractions, Hotels, and Restaurants in {destination}")
    location_data = get_location_data(destination)
    
    if location_data:
        lat, lon = location_data.get("lat"), location_data.get("lon")
        attractions = get_places(lat, lon, "interesting_places")
        hotels = get_places(lat, lon, "accomodations")
        restaurants = get_places(lat, lon, "restaurants")
        weather = get_weather(destination)  # Fetch weather details
        
        # Display weather at the top
        st.write(f"**Weather Forecast for {destination}:**")
        st.write(weather)
        
        # Generating final itinerary
        travel_plan = generate_travel_plan(destination, budget, refined_interests, duration, attractions, hotels, restaurants, weather)
        st.write(travel_plan)
