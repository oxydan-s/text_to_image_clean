# Gemini Project Configuration for text_to_image

This file provides context and instructions for the Gemini AI agent to ensure it adheres to the project's standards and conventions.

## Project Overview

This project is a Python application that converts text into images. It uses the Pillow library for image manipulation. The main script is `coscode.py`.

## Coding Style and Conventions

- **Language:** Python 3
- **Style Guide:** Follow PEP 8 for all Python code.
- **Naming:**
    - Functions: `snake_case`
    - Variables: `snake_case`
    - Classes: `PascalCase`
- **Comments:** Add comments to explain complex logic, not to describe what the code does.
- **Dependencies:** Use `requirements.txt` to manage dependencies. The primary dependency is `Pillow`.

## Tooling

- **Linter:** Use a linter like `flake8` or `pylint` if available.
- **Testing:** (No testing framework is currently set up, but if one were, it would be specified here, e.g., `pytest`).

## Interaction Protocols

These sections guide Gemini's behavior during different phases of a task.

<PROTOCOL:EXPLAIN>
When explaining code, be concise. Focus on the *why* behind the implementation. Start with a high-level summary before diving into details. Reference specific functions or classes by name.
</PROTOCOL:EXPLAIN>

<PROTOCOL:PLAN>
When planning a change, break it down into small, logical steps. List the files that will be modified for each step. If there are potential risks or side effects, mention them.
</PROTOCOL:PLAN>

<PROTOCOL:IMPLEMENT>
When implementing changes:
1.  Adhere strictly to the coding style defined above.
2.  Ensure new code is clear, readable, and well-documented where necessary.
3.  If adding a new dependency, mention that `requirements.txt` needs to be updated.
4.  Do not introduce breaking changes without prior confirmation.
</PROTOCOL:IMPLEMENT>
