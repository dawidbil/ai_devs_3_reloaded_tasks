from typing import Any

class Centrala:
    BASE_URL: str

    task_name: str
    apikey: str

    def __init__(self, task_name: str, apikey: str) -> None: ...
    def send_solution(self, answer: str | list[Any] | dict[str, Any]) -> str: ... 