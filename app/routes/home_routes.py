from fastapi import HTTPException, APIRouter
from fastapi.responses import FileResponse
import os


router = APIRouter()

@router.get('/') 
async def read_index():
    html_file_path = os.path.join(os.getcwd(), 'templates', 'index.html')
    if os.path.exists(html_file_path):
        return FileResponse(html_file_path)
    raise HTTPException(status_code=404, detail="Index HTML not found")