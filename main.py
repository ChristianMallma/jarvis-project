import os
import openai

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Establece tu API key de OpenAI
openai.api_key = os.getenv('API_KEY')


# Función para generar una respuesta a partir de un prompt
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()


# Ruta principal del sitio web
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Ruta para procesar la entrada del usuario y generar una respuesta
@app.post("/chat")
async def chat(request: Request, message: str = Form(...)):
    prompt = f"Usuario: {message}\nJarvis:"
    response = generate_response(prompt)
    return templates.TemplateResponse("index.html", {"request": request, "message": message, "response": response})
