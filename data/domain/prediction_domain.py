from pydantic import BaseModel
from typing import List, Optional

class MSDSRequest(BaseModel):
    MSDS_input: List[str]


class MSDSResponse(BaseModel):
    status: Optional[str] = 'SUCCESS'
    status_detail: Optional[str] = 'SUCCESS'
    code: Optional[str] = '200'