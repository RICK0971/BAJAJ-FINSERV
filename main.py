from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import uvicorn
from parser import extract_lab_tests
from models import LabTestResponse, LabTestResult

app = FastAPI()

@app.post("/get-lab-tests", response_model=LabTestResponse)
async def get_lab_tests(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        results = extract_lab_tests(contents)
        return LabTestResponse(
            is_success=True,
            data=[LabTestResult(**result) for result in results]
        )
    except Exception as e:
        return LabTestResponse(
            is_success=False,
            error=str(e)
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)