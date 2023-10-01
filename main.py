from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
from googletrans import Translator
import requests
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


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
async def translate_url(input_data: InputData):  # Accept the URL from the request body
    lis = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
    }

    url = input_data.url

    res = requests.get(url, headers=headers, timeout=100)

    content = res.content

    soup = BeautifulSoup(content, "html.parser")
    # Remove all script tags from the soup
    for script in soup.find_all("script"):
        script.extract()
    text = soup.get_text()
    lis = [x for x in text.split("\n") if x != ""]

    dict = {}

    for i in lis:
        i = i.strip()
        if i != "":
            print(i)
            translated_text = translator.translate(i, src="en", dest="hi")
            dict.update({i: translated_text.text})

    print(dict)
    return dict


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
