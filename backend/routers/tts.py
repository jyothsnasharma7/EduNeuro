from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from pathlib import Path

from schemas.tts import TTSRequest, TTSResponse
from services.tts_service import generate_speech, delete_audio_file
from core.dependencies import get_current_user
from schemas.user import UserResponse

router = APIRouter(prefix="/tts", tags=["text-to-speech"])

# Directory for audio files
AUDIO_DIR = Path("static/audio")


@router.post("/generate", response_model=TTSResponse, status_code=200)
async def create_speech(request: TTSRequest):
    """
    Convert text to speech.
    
    AUTHENTICATION REMOVED FOR HACKATHON DEMO.
    """
    result = await generate_speech(
        text=request.text,
        language=request.language,
        slow=request.slow,
        voice_type=request.voice_type
    )
    return TTSResponse(**result)


@router.get("/audio/{filename}")
async def get_audio_file(filename: str):
    """
    Serve audio files.
    """
    filepath = AUDIO_DIR / filename
    
    # Security: Ensure the file exists and is in the audio directory
    if not filepath.exists() or not str(filepath).startswith(str(AUDIO_DIR.resolve())):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio file not found"
        )
    
    return FileResponse(
        path=filepath,
        media_type="audio/mpeg",
        filename=filename
    )


@router.delete("/audio/{filename}")
async def delete_audio(
    filename: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Delete an audio file.

    STILL REQUIRES AUTHENTICATION.
    """
    deleted = await delete_audio_file(filename)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio file not found"
        )
    return {"message": "Audio file deleted successfully"}
