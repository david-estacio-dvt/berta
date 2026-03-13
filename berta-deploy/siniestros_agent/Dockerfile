FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for document parsing
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY siniestros_agent/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the agent package
COPY siniestros_agent/ ./siniestros_agent/

# Environment variables (defaults, overridden by Cloud Run env vars)
ENV GOOGLE_CLOUD_PROJECT=pmo-piloto-gemini-enterprise
ENV GOOGLE_CLOUD_LOCATION=europe-west1
ENV GOOGLE_GENAI_USE_VERTEXAI=TRUE
ENV CAS_MODEL=gemini-2.5-flash
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["uvicorn", "siniestros_agent.api_server:app", "--host", "0.0.0.0", "--port", "8080"]
