# app/main.py

from fastapi import FastAPI

app = FastAPI(title="Api rest en contenedor")


@app.get("/")
def read_root():
    return {"hello": "world"}


