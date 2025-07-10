# bike_tracker_app

![GitHub Tag](https://img.shields.io/github/v/tag/3elele/bike_tracker_app)

| :triangular_flag_on_post: DEV VERSION |
| :--------------------------------------- |

This repository contains the scripts for creating a simple Flask app to track my (almost) daily bike usage.

**Context**. The idea for this app is born from the fact that tracking daily bike usage without a (sometimes) very expensive smart device is nerly impossible. I just have my bike's distance-speed tracker and started to note my usage on a piece of paper. One day I washed my jeans with my piece of paper and WoOoOsh my bike progress is gone... So I started to note my progress on my phone's note app but very quickly I realised that as I work in Computer Science I could just have a little app to organise my progress note. That's how bike_tracker_app is born.

The bike tracker app is intended for personal use and in continous development.

An exemple database is present in this repo containing my bike usage from april 2025. 

## USAGE

Download the bike_tracker_app repo using git  then from the downloaded folder launch the app in development mode.

For production execution 

```
git clone 3elele/bike_tracker_app
cd bike_tracker_app-master
# DEV
python app.py
# PROD UNIX
waitress-serve --port=1620 app:app
# PROD WIN
python -m waitress --port=1620 app:app
```

**NB** Ensure port 1620 is available on your machine for the app to work correctly. The execution port can be changed in the uvicorn config file.

## TODO

- Add possibility to change database input
- Add CSV import for more convenient data creation
- Change plotting library to have interactive plots
