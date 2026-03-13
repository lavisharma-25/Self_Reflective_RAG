from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/health-check")
async def health_check():
    return {"status": "ok"}