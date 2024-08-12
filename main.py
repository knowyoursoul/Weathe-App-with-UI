import tkinter as tk
from tkinter import messagebox
import requests

# Загрузка API ключа
try:
    with open('API_KEY', 'r') as file:
        api_key = file.read().strip()
except FileNotFoundError:
    messagebox.showerror("Error", "API_KEY file not found!")
    raise

def get_weather():
    location = city_entry.get().strip()
    
    if not location:
        messagebox.showwarning("Input Error", "Please enter a location!")
        return
    
    try:
        result = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={api_key}')
        result.raise_for_status()  # Это вызовет исключение при HTTP ошибке (например, 404 или 500)
        data = result.json()

        if data['cod'] == '404':
            messagebox.showerror("Error", "Invalid location!")
            return

        description = data['weather'][0]['description']
        temperature = round(data['main']['temp'])
        feels_like = round(data['main']['feels_like'])
        high = round(data['main']['temp_max'])
        low = round(data['main']['temp_min'])

        result_text = (f"The weather in {location.capitalize()} is {temperature}°C with {description}.\n"
                       f"It feels like {feels_like}°C.\n"
                       f"Today's high is {high}°C and today's low is {low}°C.")
        
        weather_result_label.config(text=result_text)

    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("HTTP Error", f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error retrieving data: {e}")

# Создание основного окна
root = tk.Tk()
root.title("Weather App")
root.geometry("400x300")

# Виджеты интерфейса
city_label = tk.Label(root, text="Enter Location:", font=("Helvetica", 14))
city_label.pack(pady=10)

city_entry = tk.Entry(root, font=("Helvetica", 14))
city_entry.pack(pady=10)

get_weather_button = tk.Button(root, text="Get Weather", command=get_weather, font=("Helvetica", 14))
get_weather_button.pack(pady=10)

weather_result_label = tk.Label(root, text="", font=("Helvetica", 14), justify="left", wraplength=350)
weather_result_label.pack(pady=20)

# Запуск приложения
root.mainloop()
