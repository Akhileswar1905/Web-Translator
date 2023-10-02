from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
from googletrans import Translator
import requests
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
from firebase_config import upload_audio_and_get_url
import re


class InputData(BaseModel):
    url: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize a Translator object
translator = Translator()


# Function to convert text to speech and get the URL
def speak_and_get_url(text):
    tts = gTTS(text, lang="hi")
    file_name = "audio/output.mp3"
    tts.save(file_name)
    url = upload_audio_and_get_url(file_name)
    return url


# Replace function
def replace_symbols_with_space(text):
    # Define a regular expression pattern to match symbols and newlines
    pattern = r"[^\w\s]+|\n"

    # Use re.sub() to replace matching symbols and newlines with whitespace
    cleaned_text = re.sub(pattern, " ", text)

    return cleaned_text


# Endpoint for home
@app.get("/")
async def welcome():
    return "Welcome to Web Translator"


# Get Endpoint for /translate
@app.get("/translate")
async def translate_welcome():
    return "Welcome to /translate endpoint"


# FastAPI endpoint to scrape and translate a webpage
@app.post("/translate")
async def translate_url(input_data: InputData):
    url = input_data.url
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
    }

    try:
        res = requests.get(url, headers=headers, timeout=100)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")
        # Remove all script tags from the soup
        for script in soup.find_all("script"):
            script.extract()
        text = soup.get_text()
        lis = [x.strip() for x in text.split("\n") if x.strip() != ""]
        translations = {}

        for i in lis:
            print(i)
            translated_text = translator.translate(i, src="en", dest="hi")
            translations[i] = translated_text.text
        text = replace_symbols_with_space(text)
        print(text)
        audio_url = speak_and_get_url(text)
        return {"text": translations, "audio_url": audio_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
