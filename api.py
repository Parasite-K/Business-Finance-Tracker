from fastapi import FastAPI

from routers import(
    transactions,
    projects,
    clients,
    reports
)



app = FastAPI()
app.include_router(transactions.router)
app.include_router(projects.router)
app.include_router(clients.router)
app.include_router(reports.router)

@app.get("/")
def home():
    return {"message": "Business Finance Tracker API"}


