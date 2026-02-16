# -*- coding: utf-8 -*-
#
##
###
####
#####

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
    if speed <= 6:
        met = 1
    elif speed <= 8:
        met = 2
    elif speed <= 10:
        met = 3
    elif speed <= 12:
        met = 4
    elif speed <= 14:
        met = 5
    elif speed <= 16:
        met = 6
    elif speed <= 18:
        met = 7
    elif speed <= 20:
        met = 8
    elif speed <= 22:
        met = 9
    elif speed <= 24:
        met = 10
    elif speed <= 26:
        met = 11
    elif speed <= 28:
        met = 12
    elif speed <= 30:
        met = 13
    elif speed <= 32:
        met = 14
    else:
        met = 0

    return met

def calculate_calories(speed: int, time_in_minutes: int, weight: int = 77) -> int:
    met = set_met_value(int(speed))
    calories = met * weight * (time_in_minutes // 60)
#    print(met, weight, (time_in_minutes // 60), calories)

    return calories

def send_data_to_json() -> None:
    if date.value in bike_data_dict["date"]:
        date_id = bike_data_dict["date".index(date.value)]
        bike_data_dict["km"][date_id] = km.value
        bike_data_dict["speed"][date_id] = speed.value
        bike_data_dict["minutes"][date_id] = int(minutes.value)
        bike_data_dict["kgcal"][date_id] = calculate_calories(speed.value,
                                                              minutes.value)
    else:
        bike_data_dict["date"].append(date.value)
        bike_data_dict["km"].append(km.value)
        bike_data_dict["speed"].append(speed.value)
        bike_data_dict["minutes"].append(int(minutes.value))
        bike_data_dict["kgcal"].append(calculate_calories(speed.value,
                                                      minutes.value))
    with open("bike_data.json", "w") as j:
        json.dump(bike_data_dict, j)
    ui.notify(f"Data for {date.value} added to the database")

# UI Elements --------------------
with ui.row(wrap=False):
    with ui.card():
        date = ui.date_input("Day",
                             value="2025-15-04")

        with ui.row():
            speed = ui.number(label="avg km/h", 
                              value=mean(bike_data_dict["speed"]), 
                              precision=2,
                              step=0.1)
            km = ui.number(label="km", 
                                 value=mean(bike_data_dict["km"]), 
                                 precision=2,
                                 step=0.1)
            minutes = ui.number(label="minutes", 
                             value=mean(bike_data_dict["minutes"]))

        ui.button("Add data", 
                  on_click=send_data_to_json, 
                  icon="directions_bike")

    with ui.tabs().props("vertical") as tabs:
        ui.tab("km", label="Distance", icon="add_road")
        ui.tab("speed", label="Speed", icon="speed")
        ui.tab("min", label="Time", icon="timer")
        ui.tab("cal", label="Calories", icon="whatshot")
    with ui.tab_panels(tabs, value="km").props("vertical").classes("w-full h-full"):
        with ui.tab_panel("km"):
            fig = go.Figure(go.Scatter(x=bike_data_dict["date"],
                                       y=bike_data_dict["km"]))
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
            ui.plotly(fig).classes("w-full h-80")
        with ui.tab_panel("speed"):
            fig = go.Figure(go.Scatter(x=bike_data_dict["date"],
                                       y=bike_data_dict["speed"]))
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
            ui.plotly(fig).classes("w-full h-80")
        with ui.tab_panel("min"):
            fig = go.Figure(go.Scatter(x=bike_data_dict["date"],
                                       y=bike_data_dict["minutes"]))
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
            ui.plotly(fig).classes("w-full h-80")
        with ui.tab_panel("cal"):
            fig = go.Figure(go.Scatter(x=bike_data_dict["date"],
                                       y=bike_data_dict["kgcal"]))
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
            ui.plotly(fig).classes("w-full h-80")

# App run --------------------
ui.run(port=1620, 
       title="Bike tracker app", 
       favicon="icon.png")