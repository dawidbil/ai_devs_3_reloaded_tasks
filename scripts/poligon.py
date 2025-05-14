import os

import requests
from dotenv import load_dotenv

from utils.centrala import Centrala

load_dotenv()

TASK_NAME = "POLIGON"
AIDEVS_API_KEY = os.environ["AIDEVS_API_KEY"]


def get_input() -> str:
    response = requests.get("https://poligon.aidevs.pl/dane.txt")
    response.raise_for_status()
    return response.text


def main():
    if not AIDEVS_API_KEY:
        raise ValueError("AIDEVS_API_KEY not found in environment variables.")

    input_data = get_input()
    solution_list = [s for s in input_data.split("\n") if s]
    print(f"Solution prepared: {solution_list}")

    centrala_client = Centrala(task_name=TASK_NAME, apikey=AIDEVS_API_KEY)
    output = centrala_client.send_solution(solution_list)
    print(f"Output from AiDevs: {output}")


if __name__ == "__main__":
    main()
