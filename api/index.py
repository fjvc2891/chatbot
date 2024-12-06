from fastapi import FastAPI
from mangum import Mangum  # Para compatibilidad con Serverless

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "¡Hola desde FJVC!"}

# Adaptador ASGI para Vercel
handler = Mangum(app)
