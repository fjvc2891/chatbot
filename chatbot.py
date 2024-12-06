from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from transformers import pipeline

class ChatApp:
    def __init__(self):
        # Inicializar la aplicación FastAPI
        self.app = FastAPI()
        # Cargar los datos del catálogo
        self.productos = pd.read_csv('productos_fake.csv')
        # Configurar el modelo de lenguaje
        self.chat_model = pipeline("text-generation", model="distilgpt2")
        # Configurar las rutas de la API
        self.configure_routes()

    def buscar_producto(self, query):
        """Función para buscar productos en el catálogo."""
        # Dividir la consulta en palabras clave
        palabras_clave = query.split()

        # Buscar productos que coincidan con alguna palabra clave en el nombre
        resultados = self.productos[
            self.productos['name'].str.contains('|'.join(palabras_clave), case=False, na=False)
        ]
        
        if not resultados.empty:
            return resultados[['name', 'price', 'category', 'description']].to_dict(orient='records')
        
        return [{"error": "No se encontraron productos relacionados."}]

    def configure_routes(self):
        """Configurar las rutas de la aplicación."""
        @self.app.get("/")
        async def root():
            return {"message": "¡Bienvenido a FJVC! Estamos aquí para ayudarte con la mejor selección de ropa y zapatos. ¿En qué podemos asistirte hoy?"}

        @self.app.get("/formas-de-pago")
        async def formas_de_pago():
            return {
                "message": "Estas son nuestras formas de pago:",
                "formas_de_pago": [
                    {
                        "metodo": "Tarjeta de crédito/débito",
                        "enlace": "https://www.fjvc.com/pago-tarjeta"
                    },
                    {
                        "metodo": "PayPal",
                        "enlace": "https://www.fjvc.com/pago-paypal"
                    },
                    {
                        "metodo": "Transferencia bancaria",
                        "instrucciones": "Número de cuenta: 1234567890. Banco: FJVC Bank."
                    }
                ]
            }

        @self.app.post("/chat")
        async def chat(query: UserQuery):
            user_message = query.message.lower()

            # Respuesta personalizada para formas de pago
            if "formas de pago" in user_message or "cómo puedo pagar" in user_message:
                return {
                    "response": "Estas son nuestras formas de pago:\n"
                                "- Tarjeta de crédito/débito: [Enlace](https://www.fjvc.com/pago-tarjeta)\n"
                                "- PayPal: [Enlace](https://www.fjvc.com/pago-paypal)\n"
                                "- Transferencia bancaria: Número de cuenta: 1234567890, Banco: FJVC Bank."
                }

            # Intentar buscar productos relacionados
            productos_encontrados = self.buscar_producto(user_message)
            if productos_encontrados and "error" not in productos_encontrados[0]:
                return {"response": productos_encontrados}

            # Respuesta predeterminada
            return {"response": f"Lo siento, no encontré productos relacionados con '{query.message}'. ¿Puedes intentar con otro término o marca?"}

# Clase para recibir mensajes del usuario
class UserQuery(BaseModel):
    message: str

# Crear instancia de la aplicación
chat_app = ChatApp()
app = chat_app.app
