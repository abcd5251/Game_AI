from fastapi import FastAPI, File, UploadFile
from tempfile import NamedTemporaryFile
from model import speech_to_text
import os
import uvicorn

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        
        with NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
            temp_audio.write(await file.read())
            temp_audio.seek(0)
            temp_audio_path = temp_audio.name

        print("Temp audio path:", temp_audio_path)

        text_result = speech_to_text(temp_audio_path)

        return text_result
    finally:
        os.remove(temp_audio_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
