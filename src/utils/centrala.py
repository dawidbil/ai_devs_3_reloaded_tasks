from typing import Any

import requests


class Centrala:
    """Handles sending solutions to the AiDevs verification endpoint."""

    BASE_URL: str = "https://poligon.aidevs.pl/verify"

    def __init__(self, task_name: str, apikey: str):
        """Initializes the Centrala client.

        Args:
            task_name: The name of the task.
            apikey: The API key for authentication.
        """
        self.task_name: str = task_name
        self.apikey: str = apikey

    def send_solution(self, answer: str | list[Any] | dict[str, Any]) -> str:
        """Sends the provided solution to the verification endpoint.

        Args:
            answer: The solution to send, can be a string or list.

        Returns:
            The text content of the response from the server.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        payload = {
            "task": self.task_name,
            "apikey": self.apikey,
            "answer": answer,
        }
        response = requests.post(self.BASE_URL, json=payload)
        response.raise_for_status()
        return response.text
