from typing import Any

class Centrala:
    task_name: str
    apikey: str
    url: str

    def __init__(self, task_name: str, apikey: str, url: str) -> None: ...
    def send_solution(self, answer: str | list[Any] | dict[str, Any]) -> str: ...
