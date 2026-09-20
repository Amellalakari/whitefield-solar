# Whitefield rooftop solar estimate

A small Streamlit app for a 5 kW rooftop in Whitefield, Bengaluru.

It pulls Open-Meteo weather and turns solar radiation into estimated kWh and rupees.

## What it shows
- Last 30 days of estimated output
- Last 7 days vs previous 7 days
- Next 7 days forecast
- Approximate bill savings at ₹7.50 per unit

## What it is not
- Not a trained machine-learning model
- Not validated against a real inverter
- Not a replacement for a site survey or shading study

## How to run locally
```bash
pip install -r requirements.txt
streamlit run solar_app.py
