from pydantic import BaseModel
from typing import List


class ImageModel(BaseModel):
    #Id: int
    image_name: str
    sensitive_structures: List[str]
    incident_id: str
    
    