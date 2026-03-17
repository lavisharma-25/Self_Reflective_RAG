import os
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(tags=["Index"])

@router.get("/")
def read_index():
    return FileResponse(os.path.join("frontend", "index.html"))