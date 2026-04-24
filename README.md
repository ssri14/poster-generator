# Poster Generator

Poster Generator is a Streamlit application that turns a short creative brief into poster-ready copy and a printable PDF flyer. It uses OpenRouter for text generation and produces structured content that can be reused in design tools or shared directly.

## Features

- generate poster copy from a topic, audience, tone, event details, and call to action
- produce structured output for title, tagline, body copy, highlights, layout guidance, and image prompt
- copy the generated content as Markdown
- export a flyer-style PDF from the generated poster content
- run automated tests in GitHub Actions on pushes and pull requests
- create versioned release artifacts from Git tags

## Requirements

- Python 3.12 or newer is recommended
- an OpenRouter API key

## Installation

Create or activate a virtual environment, then install dependencies:

```bash
pip install -r requirements.txt
```

## Running The App

Launch the Streamlit server with:

```bash
streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`.

## Using OpenRouter

The application expects the OpenRouter API key to be entered in the UI at runtime.

- the API key is not committed to the repository
- the application does not persist the API key in project files
- the app currently uses a text model to generate poster content

For text generation, a general chat model such as `openai/gpt-4o-mini` works well.

## Output

Each run can produce:

- poster-ready text content
- a Markdown version of that content
- a printable PDF flyer

## Project Structure

```text
.
├── app.py
├── openrouter_client.py
├── pdf_generator.py
├── poster_prompt.py
├── requirements.txt
├── tests
│   ├── conftest.py
│   ├── test_openrouter_client.py
│   ├── test_pdf_generator.py
│   └── test_prompt.py
└── .github
    └── workflows
        ├── ci.yml
        └── release.yml
```

## Development

Run the test suite with:

```bash
pytest
```

The CI workflow runs on every `push` and `pull_request`. The release workflow runs when a tag matching `v*` is pushed and publishes a zip artifact through GitHub Releases.

## Release Notes

The sections below summarize the main milestones currently published from this repository.

### v1.0.0

- initial Streamlit application for poster-content generation
- OpenRouter text generation for structured poster copy
- Markdown output for easy reuse
- CI and GitHub release workflows

### v1.1.0

- flyer-style PDF export
- improved printable layout over the earlier markdown-style export
- continued support for generated poster copy and Markdown output
