from fastapi import FastAPI

from backend.api.router import router

app = FastAPI(title="Conciliador de Facturas")
app.include_router(router, prefix="/api")
