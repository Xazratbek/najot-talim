from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.routers import products

app = FastAPI(title="Products mashinalar magazini")
add_pagination(app)
app.include_router(products.router)

@app.get("/",tags=["Bosh sahifa"])
def root():
    return {"message":"Xush kelibsiz! Loyiha muvaffaqiyatli ishlamoqda."}