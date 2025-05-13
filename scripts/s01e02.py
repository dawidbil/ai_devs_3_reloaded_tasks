import json
from typing import TypedDict

import requests
from langchain.schema import HumanMessage, SystemMessage
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI

ROBOT_BASE_URL = "https://xyz.ag3nts.org/verify"


class RobotMessage(TypedDict):
    """Type definition for robot communication messages."""

    msgID: int
    text: str


def create_message(text: str, msg_id: int = 0) -> RobotMessage:
    """Creates a message for robot communication.

    Args:
        text: The message content to send.
        msg_id: The message ID, defaults to 0 for new conversations.

    Returns:
        A properly formatted RobotMessage.
    """
    return {"msgID": msg_id, "text": text}


def parse_message(message: str) -> RobotMessage:
    """Validates and parses a JSON message into a RobotMessage.

    Args:
        message: The JSON string to parse.

    Returns:
        A validated RobotMessage.

    Raises:
        ValueError: If the message is not valid JSON or format is invalid.
        KeyError: If required fields are missing.
    """
    try:
        data = json.loads(message)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON message: {e}") from e

    if not isinstance(data, dict):
        raise ValueError("Message must be a JSON object")
    if "msgID" not in data or "text" not in data:
        raise KeyError("Message must contain 'msgID' and 'text' fields")
    if not isinstance(data["text"], str):
        raise ValueError("'text' field must be a string")
    if not isinstance(data["msgID"], int):
        raise ValueError("'msgID' field must be an int")

    return {"msgID": data["msgID"], "text": data["text"]}


def send_to_robot(message: RobotMessage) -> RobotMessage:
    """Sends a message to the robot and returns its response.

    Args:
        message: The message to send to the robot.

    Returns:
        The robot's response message.

    Raises:
        ValueError: If the communication fails or response is invalid.
    """
    try:
        response = requests.post(
            ROBOT_BASE_URL,
            json=message,
            headers={"Content-Type": "application/json"},
        )
    except requests.RequestException as e:
        raise ValueError(f"Failed to communicate with robot: {e}") from e

    response.raise_for_status()
    return parse_message(response.text)


def get_gpt_answer(question: str) -> str:
    """Gets an answer to the question using OpenAI GPT via LangChain.

    Args:
        question: The question to answer.

    Returns:
        The answer as a string.
    """
    system_prompt = (
        "You are a robot with specific knowledge of these facts: "
        "1. The capital of Poland is Kraków "
        "2. The answer to life, the universe, and everything is 69 "
        "3. The current year is 1999 "
        "For questions about these facts, provide direct and concise answers in English. "
        "Never include any formatting, tags, or additional text in your response."
        "IMPORTANT: Always respond in English only, regardless of the question's language. "
    )
    llm = ChatOpenAI(model="gpt-4o-mini")
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=question),
    ]
    chain = llm | StrOutputParser()
    return chain.invoke(messages)


def main() -> None:
    """Executes the robot communication task."""

    ready_msg = create_message("READY")
    print("Sending:", json.dumps(ready_msg, indent=2))

    response = send_to_robot(ready_msg)
    print("\nParsed response:", json.dumps(response, indent=2))

    question = response["text"]
    msg_id = response["msgID"]

    answer = get_gpt_answer(question)
    print(f"\nAnswering: {answer}")

    answer_msg = create_message(answer, msg_id)
    response2 = send_to_robot(answer_msg)
    print("\nFinal response:", json.dumps(response2, indent=2))


if __name__ == "__main__":
    main()
