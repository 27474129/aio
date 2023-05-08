from datetime import datetime

from pydantic import BaseModel


class Notification(BaseModel):
    html_file: str
    created_by: int
    starting_at: datetime
