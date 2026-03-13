FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY siniestros_agent/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the agent package
COPY siniestros_agent/ ./siniestros_agent/

# Environment
ENV GOOGLE_CLOUD_PROJECT=pmo-piloto-gemini-enterprise
ENV GOOGLE_CLOUD_LOCATION=europe-west1
ENV GOOGLE_GENAI_USE_VERTEXAI=TRUE
ENV CAS_MODEL=gemini-2.5-flash
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["uvicorn", "siniestros_agent.api_server:app", "--host", "0.0.0.0", "--port", "8080"]
