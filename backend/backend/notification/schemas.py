import base64
from datetime import datetime

from pydantic import BaseModel, validator


class NotificationSchema(BaseModel):
    html_file: bytes
    created_by: int
    starting_at: datetime

    @validator('html_file')
    def validate_html_file(cls, html_file):
        return base64.b64encode(html_file)
