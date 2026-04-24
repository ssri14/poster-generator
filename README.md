# Poster Generator

Poster Generator is a classroom-friendly CI/CD demo project built with Python and Streamlit. It uses the OpenRouter chat completion API to generate poster-ready content from a topic, audience, tone, and event details.

## Project Purpose

This project demonstrates:

- a simple Streamlit application
- clean separation between UI, prompt-building, and API logic
- automated testing with `pytest`
- continuous integration with GitHub Actions
- release automation with GitHub Releases

## Setup

1. Create or activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running Locally

Start the Streamlit app:

```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit in your browser.

## Using Your OpenRouter API Key

- Enter your OpenRouter API key in the app UI.
- The key is not stored in the repository.
- The app sends the key only in the request to OpenRouter.
- For classroom demos, students can use their own key at runtime.

## Release Plan

### v1.0.0

- poster content generation
- clean Streamlit interface
- markdown output for easy copy/paste
- basic error handling
- CI workflow
- GitHub release workflow

### v1.1.0

- add OpenRouter credit or rate-limit checks
- improve prompt options and layout suggestions
- expand test coverage

## CI/CD Classroom Demonstration Flow

1. Make a small code change locally.
2. Run tests with `pytest`.
3. Push a branch or open a pull request to trigger CI.
4. Show GitHub Actions running tests on `push` and `pull_request`.
5. Create a tag such as `v1.0.0`.
6. Push the tag to trigger the release workflow.
7. Show the generated GitHub Release and attached zip artifact.

## Project Structure

```text
.
├── app.py
├── openrouter_client.py
├── poster_prompt.py
├── requirements.txt
├── tests
│   ├── test_openrouter_client.py
│   └── test_prompt.py
└── .github
    └── workflows
        ├── ci.yml
        └── release.yml
```
