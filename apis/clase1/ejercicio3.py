from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

app = FastAPI(title="FastAPI Intro")


class GreetRequest(BaseModel):
    """Cuerpo de POST /api/greet. 'name' es opcional y por defecto vale 'Guest'."""
    name: str = "Guest"


@app.get("/", response_class=PlainTextResponse)
def index():
    """Devuelve un mensaje de bienvenida."""
    return "Welcome to my first FastAPI application!"


@app.get("/about", response_class=PlainTextResponse)
def about():
    """Devuelve información sobre la app."""
    return "This is a FastAPI introduction exercise to learn basic routing and JSON handling."


@app.get("/api/hello")
def hello_api():
    """Devuelve un mensaje en JSON."""
    return {"message": "Hello, World!"}


@app.get("/api/user/{username}")
def get_user(username: str):
    """Recibe un username por la URL y devuelve un JSON con él."""
    return {"username": username, "message": f"Welcome, {username}!"}


@app.post("/api/greet")
def greet(body: GreetRequest):
    """
    Recibe un JSON con un nombre y devuelve un saludo.

    Cuerpo esperado: {"name": "Alice"}
    """
    # FastAPI ya ha leído el JSON y lo ha validado contra GreetRequest
    return {"greeting": f"Hello, {body.name}!"}
