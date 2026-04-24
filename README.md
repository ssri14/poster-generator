# Poster Generator

Poster Generator is a Streamlit application that turns a short creative brief into poster-ready copy, optional AI-generated artwork, and a printable PDF flyer. It uses OpenRouter for text generation and, optionally, image generation through OpenRouter-compatible image models.

## Features

- generate poster copy from a topic, audience, tone, event details, and call to action
- produce structured output for title, tagline, body copy, highlights, layout guidance, and image prompt
- optionally generate poster artwork with an OpenRouter image model
- preview and download the generated image
- export a polished one-page PDF flyer
- copy the generated content as Markdown
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
- text generation and image generation can use different model names

For text generation, a general chat model such as `openai/gpt-4o-mini` works well.

For image generation, `v1.2.0` defaults to `google/gemini-2.5-flash-image`, which is an image-capable model available on OpenRouter as of April 24, 2026.

## Output

Each run can produce:

- poster-ready text content
- a Markdown version of that content
- an optional AI-generated image
- a printable PDF flyer that can include the generated image

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

### v1.0.0

- initial Streamlit app
- OpenRouter text generation for poster content
- Markdown export
- CI and release workflows

### v1.1.0

- improved flyer-style PDF export

### v1.2.0

- optional OpenRouter image generation
- image preview and download in the UI
- PDF export can include generated artwork
- README refreshed for general project use
