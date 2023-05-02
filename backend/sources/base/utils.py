import json
from typing import Dict, List


def get_response_template() -> Dict[str, List]:
    return {
        'warnings': [],
        'errors': [],
        'rows': []
    }


def serialize_response(response: Dict[str, List]) -> str:
    return json.dumps(response, indent=4, sort_keys=True, default=str)
