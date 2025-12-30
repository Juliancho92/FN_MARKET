from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, productos, tickets

app = FastAPI(
    title="FN MARKET API",
    description="API backend para FN MARKET e-commerce",
    version="1.0.0"
)

# CORS Middleware
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173", # Vite default
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(productos.router)
app.include_router(tickets.router)

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de FN MARKET"}
