# Contributing to VM Manager

First off, thanks for taking the time to contribute! ❤️

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**
* **Include your environment details (OS, browser, versions)**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and expected behavior**
* **Explain why this enhancement would be useful**

### Pull Requests

* Follow the Python/JavaScript styleguides
* Include appropriate test cases
* Update documentation as needed
* End all files with a newline

## Development Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Frontend

```bash
cd frontend
npm install
npm start
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Styleguides

### Python

* Follow PEP 8
* Use type hints
* Max line length: 100 characters
* Use descriptive variable names

### JavaScript

* Use ESLint configuration
* Use meaningful variable names
* Use functional components in React
* Include prop types or TypeScript

### Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

## Additional Notes

### Issue and Pull Request Labels

* `bug` - Something isn't working
* `enhancement` - New feature or request
* `documentation` - Improvements or additions to documentation
* `good first issue` - Good for newcomers
* `help wanted` - Extra attention is needed

## Project Structure

```
vm-manager/
├── backend/          # FastAPI backend
├── frontend/         # React frontend
├── docker-compose.yml
└── README.md
```

## Getting Help

* Check the documentation
* Search existing issues
* Ask on GitHub Discussions

---

Thank you for contributing to VM Manager! 🎉
