import os
from dotenv import load_dotenv
from duckduckgo_search import DDGS
import google.generativeai as genai
import time
import random




#print("Current working directory:", os.getcwd())
#print("GEMINI_API_KEY:", os.getenv("GEMINI_API_KEY"))





# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

# Function to perform web search for weather
ddgs = DDGS()

def get_weather_from_web(city):
    query = f"current weather in {city}"
    try:
        time.sleep(random.uniform(10, 15))
        results = ddgs.text(query, max_results=3)
        weather_info = ""
        for result in results:
            weather_info += f"{result['title']}: {result['body']}\n"
        return weather_info if weather_info else "No weather information found."
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"

# Function to query Gemini for weather summary
def get_weather_summary(city, web_data):
    prompt = f"""
You are a weather assistant. I have fetched the following web data about the current weather in {city}:
{web_data}

Please summarize the weather information in a concise, user-friendly format. Include key details like temperature, conditions, and any notable weather events. If the data is insufficient or unclear, state that and suggest checking a reliable source.
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error processing weather data with Gemini: {str(e)}"

# Main function to run the weather agent
def main():
    city = input("Enter the city to check the weather for: ")
    print(f"Fetching weather for {city}...")
    
    # Get raw web data
    web_data = get_weather_from_web(city)
    print("Raw web data:", web_data)
    
    # Get summarized weather from Gemini
    summary = get_weather_summary(city, web_data)
    print("\nWeather Summary:")
    print(summary)

if __name__ == "__main__":
    main()
