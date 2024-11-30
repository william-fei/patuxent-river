# Sora Migration Visualizer

## Exploring Tools for Geospatial Visualization and Analysis

## Background

This project visualizes the migration patterns of the Sora Rail.

Every fall, Sora gather by the hundreds at Patuxent River Park. By attaching transmitters that weigh only 1.5 grams, researchers are gaining valuable data into the migration routes of these marsh birds.

https://github.com/user-attachments/assets/746e287a-4e23-4181-9330-ae0ed9370557

## Data Cleaning

The repository contains my script for the data cleaning: `cleaning.ipnyb`.

I used Python to process the original 2 GB dataset, which contained all recorded interactions between tagged birds and receiver stations from 2017 to 2022. I filtered the data to retain only the first recorded instance of each bird at a specific receiver location, excluding birds that traveled identical paths. After processing, I reduced the dataset to 12 KB to ensure it was concise yet representative of unique migration paths.