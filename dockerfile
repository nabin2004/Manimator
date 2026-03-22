FROM python:3.11-slim

# Set up working directory
WORKDIR /app

# Install build tools and git (for optional dependencies)
RUN apt-get update && apt-get install -y git gcc libcairo2-dev pkg-config libpango1.0-dev ffmpeg libsndfile1 && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml ./
COPY uv.lock ./
COPY src ./src
COPY .env.example ./

# Install dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir 'uv[all]'
RUN uv pip install --system --no-cache-dir .

# Expose API port
EXPOSE 8042

# Default command: run the FastAPI app with hot reload for development
CMD ["uvicorn", "manimator.api.app:app", "--host", "0.0.0.0", "--port", "8042", "--reload"]
