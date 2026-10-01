
# Central Park Squirrel Census Dashboard

An interactive web application built with Python to analyze and visualize data from the **2018 Central Park Squirrel Census**. This project processes raw observational data, structures it into a clean data model, and presents insights about squirrel behavior, color distribution, and locations through an intuitive dashboard.

## 📊 Project Overview

This project was developed as part of the **VALI IT!** intensive training programme. The main goal was to transform raw data into a structured format and build a functional data application.

The project consists of:
* **Data Processing & Modeling:** Cleaning raw data and creating dimensional tables (`dim_location`, `dim_squirrel`, `dim_time`, and `fact_observations`) using pandas in  Jupyter Notebook.
* **Interactive Dashboard:** A web application (`squirrel_app.py`) featuring key metrics, activity bar charts, an interactive location map of Central Park, and dynamically filtered data previews.

## 🛠️ Tech Stack

* **Language:** Python
* **Data Analysis:** Pandas, Jupyter Notebook
* **Dashboard Framework:** Streamlit (or Plotly/Dash, depending on your exact library)
* **Data Source:** 2018 Central Park Squirrel Census

## 📁 Repository Structure

* `Squirrel app.ipynb` - Jupyter Notebook used for initial data exploration and cleaning.
* `squirrel_app.py` - Main application script for running the interactive dashboard.
* `Squirrel_Data_Raw.csv` - The original dataset before processing.
* `dim_*.csv` & `fact_*.csv` - Cleaned dimensional and fact tables resulting from the data model.
* `requirements.txt` - Project dependencies and required packages.

## 🚀 Getting Started

https://portfolio-kruyb2ddsgyafty4tdau3b.streamlit.app/
