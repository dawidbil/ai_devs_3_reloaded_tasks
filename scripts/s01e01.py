import re
from typing import cast

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.schema import HumanMessage, SystemMessage

from utils.llm import (
    LLMProvider,
    get_llm_completion,
)

load_dotenv()


def get_captcha_question(content: str) -> str:
    soup = BeautifulSoup(content, "html.parser")
    question = soup.find("p", attrs={"id": "human-question"})
    if question is None:
        raise ValueError("Question not found")
    return cast(str, question.text)


def get_captcha_answer(question: str) -> str:
    messages = [
        SystemMessage(
            content="You are a captcha solver. You are given a question and you need to answer it. Return only the answer, nothing else."
        ),
        HumanMessage(content=question),
    ]
    answer = get_llm_completion(messages=messages, model=LLMProvider.OPENAI_GPT_4O_MINI)
    return answer


def login(url: str, captcha_answer: str) -> requests.Response:
    response = requests.post(
        url,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data=f"username=tester&password=574e112a&answer={captcha_answer}",
    )
    response.raise_for_status()
    return response


def main():
    url = "https://xyz.ag3nts.org/"
    print(f"Getting {url}")
    response = requests.get(url)
    response.raise_for_status()

    question = get_captcha_question(response.text)
    print(question)

    answer = get_captcha_answer(question)
    print(answer)

    response = login(url, answer)
    print(response.text)

    flag = re.search(r"{{FLG:(.*?)}}", response.text)
    if flag is None:
        raise ValueError("Flag not found")
    print(flag.group(1))


if __name__ == "__main__":
    main()
