from pydantic import BaseModel, Field, validator
from typing import List, Optional, Union
from datetime import datetime

class LabTestResult(BaseModel):
    test_name: str = Field(..., description="Name of the lab test")
    test_value: Union[float, str] = Field(..., description="Actual value of the test")
    bio_reference_range: str = Field(..., description="Normal reference range for the test")
    test_unit: Optional[str] = Field(None, description="Unit of measurement (e.g., mg/dL, %)")
    lab_test_out_of_range: bool = Field(..., description="Whether the test value is outside the reference range")

    @validator('test_value')
    def validate_test_value(cls, v):
        if isinstance(v, str):
            try:
                return float(v)
            except ValueError:
                return v
        return v

class LabTestResponse(BaseModel):
    is_success: bool = Field(..., description="Whether the request was successful")
    data: Optional[List[LabTestResult]] = Field(None, description="List of lab test results")
    error: Optional[str] = Field(None, description="Error message if request failed")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of the response") 