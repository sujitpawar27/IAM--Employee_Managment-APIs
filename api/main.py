from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .Routes.employee_routes import router
from .Database.db import Base, engine
from .Routes.department_route import router as department_router

Base.metadata.create_all(bind=engine)
print("Database created")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/users", tags=["Users"])
app.include_router(department_router, prefix="/departments", tags=["Departments"])

@app.get("/")
def home():
    return {"message": "API is working...."}


