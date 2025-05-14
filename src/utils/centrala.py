from typing import Any

import requests


class Centrala:
    """Handles sending solutions to a verification endpoint."""

    def __init__(self, task_name: str, apikey: str, url: str):
        """Initializes the Centrala client.

        Args:
            task_name: The name of the task.
            apikey: The API key for authentication.
            url: The base URL of the verification endpoint.
        """
        self.task_name: str = task_name
        self.apikey: str = apikey
        self.url: str = url

    def send_solution(self, answer: str | list[Any] | dict[str, Any]) -> str:
        """Sends the provided solution to the verification endpoint.

        Args:
            answer: The solution to send, can be a string, list, or dict.

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
        response = requests.post(self.url, json=payload)
        response.raise_for_status()
        return response.text
