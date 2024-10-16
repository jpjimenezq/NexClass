import requests
import urllib.parse
from bs4 import BeautifulSoup
from datetime import datetime

userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
base_url = "https://co.computrabajo.com"
headers = {"user-agent" : userAgent}

category = ["desing", "development", "marketing", "it-and-software", "personal-development", "business", "photography-and-video", "music"]

url_base = f'https://www.udemy.com/es/courses/{category}/?p=1&price=price-free&sort=popularity'

def extraer_cursos():
    url = url_base
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        print(f"Error: La solicitud no pudo ser completada. Código de estado: {res.status_code}")
        return None

    soup = BeautifulSoup(res.text, "html.parser")

    imagen = soup.find