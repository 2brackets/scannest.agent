# Run all tests with coverage
test:
	pytest --cov=src --cov-report=term-missing tests/

# Run tests verbosely without coverage
test-plain:
	pytest -v tests/

# Run only tests that failed last time
test-failed:
	pytest --last-failed

# Remove cache and coverage data
clean:
	rm -rf __pycache__ .pytest_cache .coverage htmlcov

# Build the agent binary (same as your build script)
build:
	pyinstaller --clean build/agent.spec

# Format code with black
format:
	black src/ tests/

# Run linter (optional, if you add e.g. flake8)
lint:
	flake8 src/ tests/
