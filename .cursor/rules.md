# Project Rules and Guidelines

## Python Environment
- Python version must be >=3.13
- Use `uv` as the package manager

## LLM Development
- Only use langchain and litellm for LLM interactions
- Direct API calls to LLM providers are prohibited

## Code Quality
- All code must pass basedpyright static analysis
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Document all functions and classes with docstrings