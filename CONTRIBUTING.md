# Contributing to Solar & Wind Deployment Intelligence Platform

First off, thank you for considering contributing to the platform! It's people like you that make open source and collaborative projects such a great community.

## Development Workflow

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Solar_and_Wind_Deployment_Intelligence_Platform.git
   ```
3. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bugfix-name
   ```
4. **Make your changes**. 
5. **Commit your changes** using descriptive commit messages:
   ```bash
   git commit -m "Add short description of the feature/fix"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Submit a Pull Request** against the `main` branch of the original repository.

## Setting Up Your Development Environment

Please refer to the `README.md` for complete, step-by-step instructions on how to set up the PostgreSQL database, FastAPI backend, and React frontend.

## Running Tests

Before submitting a pull request, please ensure that all tests pass. 

We use `pytest` for the backend:
```bash
cd backend
# Ensure your virtual environment is active
pytest
```
Currently, the test suite covers API routes, services, and ML integrations (164 tests). Please add new tests if you introduce new features or fix bugs.

## Coding Guidelines

- **Python (Backend)**: Follow PEP 8 guidelines. Use Pydantic for data validation.
- **JavaScript (Frontend)**: Use modern React constructs (Hooks, functional components).
- **Documentation**: If you change API endpoints, update the docstrings so that FastAPI's Swagger UI (`/docs`) stays accurate.

## Issues and Feature Requests

If you find a bug or have a feature request, please open an issue in the GitHub repository. Provide as much detail as possible, including steps to reproduce the issue.
