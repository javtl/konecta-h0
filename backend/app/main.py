from fastapi import FastAPI

app = FastAPI(title="Konecta API")

@app.get("/")
def read_root():
    return {"message": "¡Hola Javier! FastAPI está funcionando correctamente en Pop!_OS"}
