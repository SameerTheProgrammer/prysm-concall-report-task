from fastapi import FastAPI
from routes.concall import concall_router
from config.db import get_db_status, initialize_table

app = FastAPI(title="Concall.ai", description="An AI for concalls for any companies", version="1.0.0")

db_info = get_db_status()
print(f"Database is connected successfully. NOW: {db_info["now"]}, STATUS: {db_info["status"]}")

initialize_table()

@app.get("/")
async def health_check():
    return {"status": "healthy"}

app.include_router(concall_router, prefix="/concall", tags=["Concall"])