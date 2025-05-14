import json
import os
import re
from typing import Any, NotRequired, TypedDict, cast

import requests
from dotenv import load_dotenv
from langchain.schema import HumanMessage, SystemMessage

from utils.centrala import Centrala
from utils.llm import LLMProvider, get_llm_completion

load_dotenv()

AIDEVS_API_KEY = os.environ["AIDEVS_API_KEY"]
TASK_NAME = "JSON"
AIDEVS_SUBMIT_URL = "https://c3ntrala.ag3nts.org/report"


class TestField(TypedDict):
    """Structure for the 'test' field within a test-data item."""

    q: str
    a: str


class TestDataItem(TypedDict):
    """Structure for an individual item in the 'test-data' list."""

    question: str
    answer: int
    test: NotRequired[TestField]


CalibrationData = TypedDict(
    "CalibrationData",
    {
        "apikey": str,
        "description": str,
        "copyright": str,
        "test-data": list[TestDataItem],
    },
)


def parse_calibration_data(raw_json_str: str) -> CalibrationData:
    """Parses a raw JSON string into CalibrationData, performing validation.

    Args:
        raw_json_str: The JSON string to parse.

    Returns:
        A validated CalibrationData object.

    Raises:
        ValueError: If the JSON is malformed, or if the data doesn't conform
                    to the CalibrationData structure (e.g., missing keys,
                    incorrect types).
    """
    data = json.loads(raw_json_str)
    if not isinstance(data, dict):
        raise ValueError("Top-level JSON must be an object (dictionary).")

    # Validate top-level keys and types
    required_keys_spec = {
        "apikey": str,
        "description": str,
        "copyright": str,
        "test-data": list,
    }
    for key, expected_type in required_keys_spec.items():
        if key not in data:
            raise ValueError(f"Missing required top-level key: '{key}'")
        if not isinstance(data[key], expected_type):
            raise ValueError(
                f"Key '{key}' has incorrect type. Expected {expected_type.__name__}, got {type(data[key]).__name__}."
            )

    # Validate 'test-data' items
    test_data_list = data["test-data"]
    for i, item_any in enumerate(test_data_list):
        if not isinstance(item_any, dict):
            raise ValueError(f"Item at index {i} in 'test-data' is not a dictionary.")

        # Cast for type-checker assistance, but rely on runtime checks for validation
        item = cast(dict[str, Any], item_any)

        # Validate TestDataItem required fields
        if "question" not in item or not isinstance(item["question"], str):
            raise ValueError(
                f"Item at index {i} in 'test-data' is missing 'question' (string) or has wrong type."
            )
        if "answer" not in item or not isinstance(item["answer"], int):
            raise ValueError(
                f"Item at index {i} in 'test-data' is missing 'answer' (integer) or has wrong type."
            )

        # Validate optional 'test' field if present
        if "test" in item:
            test_field = item.get("test")  # Use .get() for safety, though 'in' check was done
            if not isinstance(test_field, dict):
                raise ValueError(
                    f"Optional 'test' field in 'test-data' item at index {i} is not a dictionary."
                )
            # Validate TestField required fields
            if "q" not in test_field or not isinstance(test_field.get("q"), str):
                raise ValueError(
                    f"Optional 'test' field in 'test-data' item at index {i} is missing 'q' (string) or has wrong type."
                )
            if "a" not in test_field or not isinstance(test_field.get("a"), str):
                raise ValueError(
                    f"Optional 'test' field in 'test-data' item at index {i} is missing 'a' (string) or has wrong type."
                )

    return cast(CalibrationData, cast(object, data))


def request_calibration_json() -> str:
    """Fetches calibration data from the c3ntrala server.

    The AIDEVS_API_KEY environment variable is used to construct the URL.

    Returns:
        The calibration data as a JSON string.

    Raises:
        requests.exceptions.RequestException: If the request to the server fails.
    """
    url = f"https://c3ntrala.ag3nts.org/data/{AIDEVS_API_KEY}/json.txt"
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def get_calibration_json(local_filepath: str = "json.txt") -> str:
    """Retrieves calibration data.

    Tries to read from a local file first. If the file doesn't exist,
    fetches the data from the c3ntrala server and saves it locally.

    Args:
        local_filepath: The path to the local file for caching the JSON data.
                        Defaults to "json.txt".

    Returns:
        The calibration data as a JSON string.
    """
    if os.path.exists(local_filepath):
        print(f"Reading calibration data from local file: {local_filepath}")
        with open(local_filepath, encoding="utf-8") as f:
            return f.read()
    print("Local calibration file not found. Requesting from server...")
    data_str = request_calibration_json()
    print(f"Saving calibration data to local file: {local_filepath}")
    with open(local_filepath, "w", encoding="utf-8") as f:
        f.write(data_str)
    return data_str


def inject_aidevs_api_key(data: CalibrationData, api_key: str) -> CalibrationData:
    """Replaces a placeholder API key in the data with the actual one."""
    if data.get("apikey") == "%PUT-YOUR-API-KEY-HERE%":
        data["apikey"] = api_key
        print("API key injected.")
    return data


def calculate_math_questions(data: CalibrationData) -> CalibrationData:
    """Parses math questions in 'test-data' and calculates answers."""
    print("Calculating math questions...")
    for item in data["test-data"]:
        question_str = item.get("question")
        match = re.fullmatch(r"\s*(\d+)\s*\+\s*(\d+)\s*", question_str)
        if not match:
            raise ValueError(f"Question '{question_str}' does not match the expected format.")
        num1, num2 = map(int, match.groups())
        item["answer"] = num1 + num2
    return data


def collect_test_questions(data: CalibrationData) -> list[str]:
    """Collects questions from the 'test'['q'] fields in 'test-data'."""
    questions: list[str] = []
    test_data_list_from_data = data.get("test-data")

    print("Collecting test questions...")
    for item in test_data_list_from_data:
        test_dict = item.get("test")
        if not test_dict:
            continue
        question = test_dict.get("q")
        questions.append(question)

    if questions:
        print(f"Collected {len(questions)} test questions.")
    else:
        print("No test questions found.")
    return questions


def get_llm_answers_for_questions(questions: list[str]) -> dict[str, str]:
    """Gets answers for a list of questions using an LLM.

    Instructs the LLM to return answers as a JSON mapping questions to answers.
    """
    if not questions:
        print("No questions to send to LLM.")
        return {}

    print(f"Sending {len(questions)} questions to LLM...")

    system_prompt_content = (
        "You are an AI assistant. You will be provided with a list of questions. "
        "For each question, provide a concise answer. "
        "Return your answers as a single JSON object where each key is the original question string "
        "and the value is your answer string. Ensure the JSON is well-formed."
    )

    formatted_questions = "\n".join([f"{i + 1}. {q}" for i, q in enumerate(questions)])
    human_prompt_content = f"Please answer the following questions:\n\n{formatted_questions}"

    messages = [
        SystemMessage(content=system_prompt_content),
        HumanMessage(content=human_prompt_content),
    ]

    llm_response_str: str = get_llm_completion(
        messages=messages, model=LLMProvider.OPENAI_GPT_4O_MINI
    )
    print("LLM response received.")

    answers_map = json.loads(llm_response_str)
    if not isinstance(answers_map, dict):
        print("LLM response was not a valid JSON object (dictionary).")
        return {}

    validated_answers: dict[str, str] = {}
    for q in questions:
        if q in answers_map and isinstance(answers_map[q], str):
            validated_answers[q] = answers_map[q]
        else:
            print(
                f"Warning: Answer for question '{q}' not found or not a string in LLM response. Skipping."
            )

    return validated_answers


def update_test_answers(data: CalibrationData, qa_map: dict[str, str]) -> CalibrationData:
    """Updates 'test'['a'] fields in 'test-data' with answers from the qa_map."""
    if not qa_map:
        print("No Q&A map provided to update test answers. Skipping update.")
        return data

    test_data_list_from_data = data.get("test-data")

    print("Updating test answers with LLM responses...")
    updated_count = 0
    for item in test_data_list_from_data:
        test_dict = item.get("test")
        if not test_dict:
            continue
        question = test_dict.get("q")

        if question in qa_map:
            test_dict["a"] = qa_map[question]
            updated_count += 1

    print(f"Updated {updated_count} test answers.")
    return data


def main() -> None:
    """Main function to fetch, process, update, and submit calibration data."""
    print("Attempting to get calibration JSON...")
    raw_json_str = get_calibration_json()
    parsed_json = parse_calibration_data(raw_json_str)
    print("JSON parsed and validated successfully into CalibrationData.")
    parsed_json = inject_aidevs_api_key(parsed_json, AIDEVS_API_KEY)
    parsed_json = calculate_math_questions(parsed_json)
    test_questions = collect_test_questions(parsed_json)
    llm_answers_map: dict[str, str] = {}
    if test_questions:
        print("\nCollected questions for LLM:")
        for q_idx, question_text in enumerate(test_questions):
            print(f"  {q_idx + 1}. {question_text}")
        llm_answers_map = get_llm_answers_for_questions(test_questions)
        if llm_answers_map:
            print("\nLLM Answers:")
            for q_text, ans_text in llm_answers_map.items():
                print(f"  Q: {q_text}")
                print(f"  A: {ans_text}")
        else:
            print("Could not retrieve answers from LLM or no answers processed.")

    if llm_answers_map:
        parsed_json = update_test_answers(parsed_json, llm_answers_map)
    else:
        print("Skipping update of test answers as no LLM answers were available.")

    with open("json_fixed.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(parsed_json, indent=2))

    print(f"\nAttempting to submit solution for task: {TASK_NAME}...")
    centrala_client = Centrala(task_name=TASK_NAME, apikey=AIDEVS_API_KEY, url=AIDEVS_SUBMIT_URL)
    submission_response = centrala_client.send_solution(dict(parsed_json))
    print(f"Submission response: {submission_response}")


if __name__ == "__main__":
    main()
