# -*- coding: utf-8 -*-
#
##
###
####
#####

from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
import pandas as pd
from plotnine import ggplot, aes, geom_col, labs, theme_xkcd, coord_flip, guides
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg' to avoid GUI-related issues

from utils import init_db, __bike__

# Globals
app = Flask(__name__)

#-------------------------
@app.route('/')
def index():
    init_db()
    return render_template('index.html')

@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.json
    conn = sqlite3.connect(__bike__)
    c = conn.cursor()
    c.execute("INSERT INTO bike_data (day, speed, distance, time) VALUES (?, ?, ?, ?)",
              (data['day'], data['speed'], data['distance'], data['time']))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/get_data')
def get_data():
    conn = sqlite3.connect(__bike__)
    c = conn.cursor()
    c.execute("SELECT * FROM bike_data")
    data = c.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/plot')
def plot():
    time_range = request.args.get('time_range', 'day')

    conn = sqlite3.connect(__bike__)
    df = pd.read_sql_query("SELECT * FROM bike_data", conn)
    conn.close()

    df['day'] = pd.to_datetime(df['day'])

    if time_range == 'month':
        df['month'] = df['day'].dt.to_period('M')
        plot_data = df.groupby('month')['distance', 'time'].sum().reset_index()
        plot_data['month'] = plot_data['month'].astype(str)
        x_label = 'month'
    elif time_range == 'year':
        df['year'] = df['day'].dt.to_period('Y')
        plot_data = df.groupby('year')['distance', 'time'].sum().reset_index()
        plot_data['year'] = plot_data['year'].astype(str)
        x_label = 'year'
    else:
        plot_data = df
        x_label = 'day'

    plot = (
        ggplot(plot_data, aes(x=x_label, y='distance', fill='time')) +
        geom_col(alpha=.2, color='black') +
        labs(title='Bike Usage', x=x_label.title(), y='Distance (km)') +
        guides(fill="none") +
        theme_xkcd() + coord_flip()
    )

    stream = BytesIO()
    plot.save(stream, format='png', dpi=300)
    stream.seek(0)

    return send_file(stream, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True, port=1620)
