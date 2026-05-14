from pathlib import Path

import uvicorn
from fastapi import APIRouter, FastAPI, Request 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from src.api.dependencies import exception_handler
from src.api.routers import student_router
from src.core.common.exceptions import GenericError

app = FastAPI(title="QLSV API", version="0.1.0")


@app.exception_handler(GenericError)
async def generic_exception_handler(
    request: Request, exc: GenericError
) -> JSONResponse:
    return await exception_handler(request, exc)


api_router = APIRouter(prefix="/api")
api_router.include_router(student_router.router)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "QLSV API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
