import requests
import streamlit as st

LAT = 12.9696
LON = 77.7497
SYSTEM_KW = 5.0
DERATE = 0.80
RUPEES_PER_KWH = 7.50

def rad_to_kwh(rad):
    return (float(rad or 0) / 1000.0) * SYSTEM_KW * DERATE

st.title("Whitefield rooftop solar estimate")
st.caption("5 kW system · last 30 days + next 7 days")

try:
    hist = requests.get(
        "https://archive-api.open-meteo.com/v1/archive",
        params={
            "latitude": LAT,
            "longitude": LON,
            "past_days": 30,
            "hourly": "shortwave_radiation",
            "timezone": "Asia/Kolkata",
        },
        timeout=60,
    ).json()
    times = hist["hourly"]["time"]
    rads = hist["hourly"]["shortwave_radiation"]
    rows = [(t, rad_to_kwh(r)) for t, r in zip(times, rads)]
except Exception as e:
    st.write("Could not load history.")
    st.write(str(e))
    st.stop()

total = sum(k for _, k in rows)
last = sum(k for _, k in rows[-168:]) if len(rows) >= 168 else total
prev = sum(k for _, k in rows[-336:-168]) if len(rows) >= 336 else 0
peak_t, peak_k = max(rows, key=lambda x: x[1])

st.metric("Estimated 30-day output", f"{total:.0f} kWh", f"₹{total * RUPEES_PER_KWH:,.0f}")
st.metric("Last 7 days", f"{last:.0f} kWh", f"₹{last * RUPEES_PER_KWH:,.0f}")
st.metric("Previous 7 days", f"{prev:.0f} kWh", f"{last - prev:+.0f} kWh vs prior week")
st.write("Peak hour:", peak_t, "→", round(peak_k, 3), "kWh")

st.subheader("Next 7 days (forecast)")
try:
    fut = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": LAT,
            "longitude": LON,
            "hourly": "shortwave_radiation",
            "forecast_days": 7,
            "timezone": "Asia/Kolkata",
        },
        timeout=60,
    ).json()
    f_rows = [
        (t, r, rad_to_kwh(r))
        for t, r in zip(fut["hourly"]["time"], fut["hourly"]["shortwave_radiation"])
    ]
    next_kwh = sum(x[2] for x in f_rows)
    st.metric("Forecast 7-day output", f"{next_kwh:.0f} kWh", f"₹{next_kwh * RUPEES_PER_KWH:,.0f}")
    st.caption(f"Compared with last week: {next_kwh - last:+.0f} kWh")
except Exception as e:
    st.write("Forecast failed.")
    st.write(str(e))

st.caption("Rupees use ₹7.50 per unit as an approximate avoided grid cost.")