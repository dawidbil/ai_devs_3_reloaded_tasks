# Project Rules and Guidelines

## Python Environment
- Python version must be >=3.13
- Use `uv` as the package manager

## LLM Development
- Only use langchain for LLM interactions
- Direct API calls to LLM providers are prohibited

## Code Quality
- All code must pass basedpyright static analysis
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Use Google-style docstrings:
  ```
  """One line summary.

  Longer description if needed.

  Args:
      param1: Description of param1.
      param2: Description of param2.

  Returns:
      Description of return value.
  """
  ```
- Use modern Python syntax (e.g., `int | str` instead of `(int, str)` for type unions)
- Use `raise ... from err` in except blocks to preserve exception context
- Code comments should explain why, not what (what is clear from the code itself)
- Keep try/except blocks focused on specific operations that might fail

## Cursor Rules
- Code diffs should only address what the user specifically requested. No other changes should be made.