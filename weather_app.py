import streamlit as stm
import requests
import pandas as pd
import os

file_path = "/Users/anmolkumarsrivastava/PycharmProjects/beginner_projects/cities.txt"


def get_direction(degree):
    directions = ["NORTH", "NORTH-EAST", "EAST", "SOUTH-EAST", "SOUTH", "SOUTH-WEST", "WEST", "NORTH-WEST"]
    idx = round(degree / 45) % 8
    return directions[idx]


def get_data():
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        stm.write("File not found. Please ensure the file exists.")
    except Exception as e:
        stm.write(f"An error occurred: {e}")
    df = []
    for i in lines:
        line = list(i.split("|"))
        df.append(line)
    data_frame = pd.DataFrame(df, columns=["City", "Description"])
    return data_frame


def frontend():
    stm.title("WEATHER APPLICATION...")
    data_frame = get_data()
    cities = data_frame["City"]
    city = stm.selectbox("Select city :", cities, index=None)
    if city is not None:
        stm.write("Selected City : ", city)
        stm.divider()
        index = 0
        for i in data_frame["City"].values:
            if city == i:
                break
            else:
                index += 1
        description = data_frame["Description"].at[index]
        get_weather(city, description)


def process_data(response, description):
    data = response.json()
    if data['cod'] == 200:
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        weather_description = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]
        degree = data["wind"]["deg"]
        wind_direction = get_direction(degree)
        col1, col2 = stm.columns(2)
        with col1:
            stm.write("Temperature is : ", str(int(temperature)), "°C")
            stm.write("Humidity is : ", str(int(humidity)), "%")
            stm.write("Wind speed is : ", str(wind_speed), "KMPH")
        with col2:
            stm.write("Feels Like : ", str(int(feels_like)), "°C")
            stm.write("Description : ", weather_description.upper())
            stm.write("Direction : ", wind_direction)
        stm.divider()
        stm.write(description)
    else:
        stm.write(f"Error fetching data: {response.status_code}")


def get_weather(city, description):
    api_key = "4cc73ace2556246080ce1af33ad35e79"
    url = "http://api.openweathermap.org/data/2.5/weather"
    complete_url = f'{url}?q={city}&appid={api_key}&units=metric'
    response = requests.get(complete_url)
    process_data(response, description)


frontend()
