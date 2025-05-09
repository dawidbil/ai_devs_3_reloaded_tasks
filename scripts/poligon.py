import os
import requests
from typing import Any

from dotenv import load_dotenv

_ = load_dotenv()

TASK_NAME = "POLIGON"
AIDEVS_API_KEY = os.getenv("AIDEVS_API_KEY")

def get_input() -> str:
    response = requests.get("https://poligon.aidevs.pl/dane.txt")
    response.raise_for_status()
    return response.text


def send_solution(solution: str | list[Any]):
    payload = {
        "task": TASK_NAME,
        "apikey": AIDEVS_API_KEY,
        "answer": solution,
    }
    response = requests.post("https://poligon.aidevs.pl/verify", json=payload)
    response.raise_for_status()
    return response.text


if __name__ == "__main__":
    input_data = get_input()
    solution = input_data.split("\n")
    solution = [s for s in solution if s]
    print(solution)
    output = send_solution(solution)
    print(output)
