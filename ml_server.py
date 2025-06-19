# ml_server.py

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import requests

from scripts.predict_locator_dynamic import process_html
import logging
logging.basicConfig(level=logging.DEBUG)

print("✅ ml_server.py is loaded")
app = FastAPI()

class LocatorRequest(BaseModel):
    query: str
    url: str

@app.get("/health")
def health():
    logging.debug("Health endpoint called")
    return {"status": "ok"}

@app.post("/predict-locator")
async def predict_locator(request: LocatorRequest):
    print(f"[DEBUG] Received query: {request.query}")
    print(f"[DEBUG] Received URL: {request.url}")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/114.0.0.0 Safari/537.36"
        }
        response = requests.get(request.url, headers=headers, timeout=70)
        response.raise_for_status()
        html_content = response.text
        print("[DEBUG] HTML content successfully fetched.")
    except Exception as e:
        print(f"[ERROR] Failed to fetch URL: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")

    result = process_html(request.query, html_content)
    return result
