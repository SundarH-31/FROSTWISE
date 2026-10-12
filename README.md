# FROSTWISE Official Website + Software Prototype

Streamlit website with Home, Our Solution, Who Benefits, Ask FROSTWISE, Contact, and Live Dashboard pages.

## Run on Windows
```powershell
py -3.13 -m pip install -r requirements.txt
py -3.13 -m streamlit run app.py
```
Open http://localhost:8501.

## CSV format
Required columns: `timestamp`, `room_temperature_c`, `setpoint_c`, `ambient_temperature_c`, `compressor_power_kw`.

Demo data is simulated. Energy assumes one row per hour of average compressor power. Alerts are screening signals, not confirmed diagnoses. The chat assistant is a local FAQ, not a live AI model. Contact form drafts are not sent automatically.
