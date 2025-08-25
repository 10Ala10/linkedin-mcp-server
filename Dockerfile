FROM python:3.12-alpine

# Install system dependencies including Chromium and ChromeDriver
RUN apk add --no-cache \
    git \
    curl \
    chromium \
    chromium-chromedriver

# Install uv from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Sync dependencies and install project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Create a non-root user
RUN adduser -D -u 1000 mcpuser && chown -R mcpuser:mcpuser /app
USER mcpuser

# Expose port for HTTP mode
EXPOSE 8080

# Set entrypoint and default arguments for HTTP mode
ENTRYPOINT ["uv", "run", "-m", "linkedin_mcp_server"]
CMD ["--transport", "streamable-http", "--host", "0.0.0.0", "--port", "8080", "--path", "/mcp"]
