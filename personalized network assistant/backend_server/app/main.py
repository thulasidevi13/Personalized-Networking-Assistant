from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import conversation

app = FastAPI(title="Personalized Networking Assistant")

# CORS Middleware Setup (Frontend ko connect karne dene ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "*" ka matlab hai kisi bhi frontend se request aa sakti hai
    allow_credentials=True,
    allow_methods=["*"],  # POST, GET sab methods allow karega
    allow_headers=["*"],
)

app.include_router(conversation.router)

@app.get("/")
def root():
    return {"message": "Welcome!"}
