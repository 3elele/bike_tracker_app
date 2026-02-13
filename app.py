# -*- coding: utf-8 -*-
#
##
###
####
#####

"""
TODO

create tabs for plotly elements to switch between date distance speed time
add calories computation for the json
add calories to the plotly tabs
"""

from nicegui import ui
from statistics import mean
import json
import plotly.graph_objects as go

## GLOBALS
with open("bike_data.json") as j:
    bike_data_dict = json.load(j)

# Functions --------------------
def send_data_to_json() -> None:
    bike_data_dict["date"].append(date.value)
    bike_data_dict["distance"].append(distance.value)
    bike_data_dict["speed"].append(speed.value)
    bike_data_dict["time"].append(time.value)
    with open("bike_data.json", 'w') as j:
        json.dump(bike_data_dict, j)
    ui.notify(f"Data for {date.value} added to the database")

# UI Elements --------------------
with ui.row(wrap=False):
    with ui.card():
        date = ui.date_input("Day")

        with ui.row():
            distance = ui.number(label="km", 
                                 value=mean(bike_data_dict['distance']), 
                                 precision=2)
            speed = ui.number(label="avg km/h", 
                              value=mean(bike_data_dict['speed']), 
                              precision=2)
            time = ui.number(label="minutes", 
                             value=mean(bike_data_dict['time']))

        ui.button("Add data", 
                  on_click=send_data_to_json, 
                  icon='directions_bike')
    fig = go.Figure(go.Scatter(x=bike_data_dict['date'], y=bike_data_dict['distance']))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    ui.plotly(fig).classes('w-full h-80')


# App run --------------------
ui.run(port=1620, 
       title="Bike tracker app", 
       favicon="icon.png",
       reload=False)