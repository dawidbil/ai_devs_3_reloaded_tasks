# Project Rules and Guidelines

## Python Environment
- Python version must be >=3.13
- Use `uv` as the package manager
- Add new dependencies using `uv add <package-name>`

## LLM Development
- Only use langchain for LLM interactions
- Direct API calls to LLM providers are prohibited

## Code Quality
- All code must pass basedpyright static analysis
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Declare type hints for all instance attributes, typically within the `__init__` method (e.g., `self.attribute: type = value`).
- Avoid using `typing.Any` for type hints if a more specific type can be used. Strive for the most precise type information possible.
- Annotate all class attributes with their respective types (e.g., `MY_CONSTANT: str = "value"` or `class_var: list[int]`).
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
- Use the `|` operator for union types (e.g., `int | str`) instead of `typing.Union` for modern type hinting.
- Use `raise ... from err` in except blocks to preserve exception context
- Code comments should explain why, not what (what is clear from the code itself)
- Keep try/except blocks focused on specific operations that might fail
- Avoid running executable code directly in the global scope. Instead, encapsulate it within functions. The `if __name__ == "__main__":` block should primarily be used to call a main entry-point function (e.g., `main()`).
- Employ if-guards and early returns to reduce nesting and improve code clarity. If a condition can determine the outcome of a function or a block of code, handle it and return/continue early rather than using nested `if/else` structures.
- For docstrings:
  - Include a `Raises:` section only for exceptions explicitly raised within the function, or for specific, non-obvious exceptions propagated from internal calls that are critical for the caller to know.
  - Do not list common runtime errors (e.g., `TypeError`) or errors from incorrect developer usage of parameters (e.g., passing an invalid enum value when the type hint specifies the enum).

## Cursor Rules
- Code diffs should only address what the user specifically requested. No other changes should be made.
- Absolutely no unsolicited refactoring or minor code adjustments outside the direct scope of the request.