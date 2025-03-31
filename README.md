# Travel_Planner

This is a Streamlit-based travel planning application powered by AI. It helps users generate a structured travel itinerary by gathering travel-related information like attractions, hotels, restaurants, and weather conditions for a given destination. The application uses OpenTripMap API for location-based data, OpenWeather API for weather details, and Groq’s LLaMA model for generating structured travel plans.

## Features

- **Destination Input:** Users can enter the destination (city or country).
- **Budget Selection:** Users can select their budget (Low, Medium, High).
- **Interest Selection:** Users can select multiple interests such as Adventure, Historical, Food, Nature, Relaxation, Shopping, etc.
- **Duration Input:** Users can input the trip duration in days.
- **Weather Forecast:** Weather details are fetched for the destination and included in the travel plan.
- **Attractions, Hotels, and Restaurants:** Top places to visit, stay, and dine are listed.
- **AI-Powered Itinerary:** A personalized day-wise itinerary is generated based on user input.

## Requirements

- Python 3.x
- Streamlit
- Requests
- Groq Python SDK

### Install required libraries:


pip install streamlit requests groq

API Keys
The following API keys are required for accessing external APIs:

OpenTripMap API Key: For location and place data.

OpenWeather API Key: For weather details.

Groq API Key: For generating travel plans using Groq’s LLaMA model.

Replace the placeholders in the code with your respective API keys.

python
Copy

```bash

OPENTRIPMAP_API_KEY = "your_opentripmap_api_key"
OPENWEATHER_API_KEY = "your_openweather_api_key"
GROQ_API_KEY = "your_groq_api_key"


```

How to Run
Clone this repository or download the script.

Install required dependencies using the command above.

Run the Streamlit app using the command:

```bash
streamlit run app.py

```
Access the app in your web browser at http://localhost:8501.


How It Works
User Inputs: Users enter a destination, budget, interests, and trip duration.

API Calls:

get_location_data: Fetches latitude and longitude for the destination using OpenTripMap API.

get_places: Fetches nearby attractions, hotels, and restaurants based on latitude and longitude.

get_weather: Fetches current weather details for the destination using OpenWeather API.

Travel Plan Generation: The user inputs and fetched data are passed to Groq’s LLaMA model to generate a structured travel plan.

Display: The weather forecast, places of interest, and the generated itinerary are displayed to the user.

Customizing
You can refine the categories under which interests are collected. The refine_user_preferences function can be modified to adjust how the user’s interests are captured.

You can adjust the radius of places searched by modifying the radius parameter in the get_places function.

License
This project is open-source and available under the MIT License. See the LICENSE file for more information.

Acknowledgments
OpenTripMap API for location data.

OpenWeather API for weather details.

Groq for providing the LLaMA model to generate personalized travel itineraries.

```bash
This README file gives a clear understanding of the project, setup instructions, and how the code works.

```
