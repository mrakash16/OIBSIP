import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime, timezone

def get_weather(api_key, location):
    base_url = "http://api.openweathermap.org/data/2.5/onecall"
    params = {
        "lat": "", 
        "lon": "", 
        "exclude": "minutely", 
        "appid": api_key,
        "units": "metric" 
    }

    try:
        coordinates_url = "http://api.openweathermap.org/data/2.5/weather"
        coordinates_params = {
            "q": location,
            "appid": api_key
        }
        coordinates_response = requests.get(coordinates_url, params=coordinates_params)
        coordinates_response.raise_for_status()
        coordinates_data = coordinates_response.json()
        params["lat"] = coordinates_data["coord"]["lat"]
        params["lon"] = coordinates_data["coord"]["lon"]

        # Now fetch detailed weather data using One Call API
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        weather_data = response.json()

        current_temperature = weather_data["current"]["temp"]
        current_humidity = weather_data["current"]["humidity"]
        current_description = weather_data["current"]["weather"][0]["description"]
        hourly_forecast = weather_data["hourly"][:5]  
        daily_forecast = weather_data["daily"][:3]  
        wind_speed = weather_data["current"]["wind_speed"]

        return {
            "current_temperature": current_temperature,
            "current_humidity": current_humidity,
            "current_description": current_description,
            "hourly_forecast": hourly_forecast,
            "daily_forecast": daily_forecast,
            "wind_speed": wind_speed
        }
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"

def get_weather_and_display(api_key, location_entry, result_label):
    location = location_entry.get()
    weather_data = get_weather(api_key, location)

    if isinstance(weather_data, dict):
        result_str = (
            f"Weather in {location}:\n"
            f"Temperature: {weather_data['current_temperature']}°C\n"
            f"Humidity: {weather_data['current_humidity']}%\n"
            f"Description: {weather_data['current_description']}\n"
            f"Wind Speed: {weather_data['wind_speed']} m/s\n\n"
            "Hourly Forecast:\n"
        )

        for hour_data in weather_data["hourly_forecast"]:
            result_str += (
                f"{datetime.fromtimestamp(hour_data['dt'], timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}: "
                f"{hour_data['temp']}°C, {hour_data['weather'][0]['description']}\n"
            )

        result_str += "\nDaily Forecast:\n"

        for day_data in weather_data["daily_forecast"]:
            result_str += (
                f"{datetime.fromtimestamp(day_data['dt'], timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}: "
                f"{day_data['temp']['day']}°C, {day_data['weather'][0]['description']}\n"
            )

        result_label.config(text=result_str)
    else:
        result_label.config(text=weather_data)

def clear_entry(location_entry):
    location_entry.delete(0, tk.END)

def main():
    # GUI setup
    root = tk.Tk()
    root.title("Advanced Weather App")

    root.configure(bg="#e6f7ff")

    title_label = tk.Label(root, text="Advanced Weather App", font=("Helvetica", 16, "bold"), bg="#e6f7ff")
    title_label.pack(pady=10)

    location_label = tk.Label(root, text="Enter city or ZIP code:", bg="#e6f7ff")
    location_label.pack(pady=5)

    location_entry = tk.Entry(root)
    location_entry.pack(pady=5)

    get_weather_button = tk.Button(
        root,
        text="Get Weather",
        command=lambda: get_weather_and_display(api_key, location_entry, result_label),
        bg="#4CAF50",  # Green color
        fg="white"    
    )
    get_weather_button.pack(pady=10)

    clear_button = tk.Button(
        root,
        text="Clear Entry",
        command=lambda: clear_entry(location_entry),
        bg="#f44336",  # Red color
        fg="white"     
    )
    clear_button.pack(pady=5)

    result_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#e6f7ff")
    result_label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    api_key = "bd5e378503939ddaee76f12ad7a97608"
    main()
