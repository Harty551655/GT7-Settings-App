# GT7 AI Settings Assistant (MVP)

This project is a starter app for generating **Gran Turismo 7 setup recommendations** based on:

- Car
- Track
- Weather
- Time of day
- Installed custom parts
- Driver struggles (e.g., understeer, traction loss, braking instability)

## What this MVP includes

- A FastAPI backend with:
  - `/api/recommend` for setup recommendations.
  - `/api/health` for a quick service check.
  - A prompt builder so you can plug in a real LLM later.
- A simple web UI to submit inputs and view recommendations.
- Unit + API tests for recommendation behavior.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Then open <http://127.0.0.1:8000>.

## Quick check

```bash
curl http://127.0.0.1:8000/api/health
```

Expected response:

```json
{"status":"ok"}
```

## API

### `POST /api/recommend`

Request body:

```json
{
  "car": "Porsche 911 GT3 RS",
  "track": "Spa-Francorchamps",
  "weather": "rain",
  "time_of_day": "night",
  "custom_parts": ["racing suspension", "high-rpm turbo"],
  "struggles": ["mid-corner understeer", "traction on corner exit"]
}
```

Returns:

- Setup recommendations grouped by area (suspension, differential, aero, transmission, brakes, tires)
- A generated AI prompt (`llm_prompt`) you can send to your preferred LLM provider.

## Next steps

- Add real GT7 baseline setup datasets by car class + track category.
- Plug in an LLM provider for free-text rationale and iterative coaching.
- Save driver profiles and setup history to a database.
