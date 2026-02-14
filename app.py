# -*- coding: utf-8 -*-
#
##
###
####
#####

"""
TODO

create tabs for plotly elements to switch between date distance speed time
add calories to the plotly tabs
"""

from nicegui import ui
from statistics import mean
import json
import plotly.graph_objects as go

## GLOBALS
try:
    with open("bike_data.json") as j:
        bike_data_dict = json.load(j)
except FileNotFoundError:
    bike_data_dict = {
        "date":["2025-14-04"],
        "km":[18.5],
        "speed":[9.66], 
        "minutes":[60],
        "kgcal":[539],
    }

# Functions --------------------
def set_met_value(speed: int) -> int:
    match speed:
        case _ if speed <= 6:
            met = 1
        case 8:
            met = 2
        case 10:
            met = 3
        case 12:
            met = 4
        case 14:
            met = 5
        case 16:
            met = 6
        case 18:
            met = 7
        case 20:
            met = 8
        case 22:
            met = 9
        case 24:
            met = 10
        case _:
            met = None  # or any default value

    return met

def calculate_calories(speed: int, time_in_minutes: int, weight: int = 77) -> int:
    met = set_met_value(speed)
    calories = met * weight * (time_in_minutes // 60)

    return calories

def send_data_to_json() -> None:
    bike_data_dict["date"].append(date.value)
    bike_data_dict["km"].append(km.value)
    bike_data_dict["speed"].append(speed.value)
    bike_data_dict["minutes"].append(minutes.value)
    bike_data_dict["kgcal"].append(calculate_calories())
    with open("bike_data.json", "w") as j:
        json.dump(bike_data_dict, j)
    ui.notify(f"Data for {date.value} added to the database")

# UI Elements --------------------
with ui.row(wrap=False):
    with ui.card():
        date = ui.date_input("Day")

        with ui.row():
            km = ui.number(label="km", 
                                 value=mean(bike_data_dict["km"]), 
                                 precision=2)
            speed = ui.number(label="avg km/h", 
                              value=mean(bike_data_dict["speed"]), 
                              precision=2)
            minutes = ui.number(label="minutes", 
                             value=mean(bike_data_dict["minutes"]))

        ui.button("Add data", 
                  on_click=send_data_to_json, 
                  icon="directions_bike")
    fig = go.Figure(go.Scatter(x=bike_data_dict["date"], y=bike_data_dict["km"]))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    ui.plotly(fig).classes("w-full h-80")


# App run --------------------
ui.run(port=1620, 
       title="Bike tracker app", 
       favicon="icon.png")