# Deploy Berta CAS to Cloud Run - europe-west1
# Proyecto: pmo-piloto-gemini-enterprise

gcloud run deploy siniestros-agent `
  --source . `
  --project pmo-piloto-gemini-enterprise `
  --region europe-west1 `
  --allow-unauthenticated `
  --memory 1Gi `
  --timeout 300 `
  --set-env-vars="CAS_MODEL=gemini-2.5-pro,GOOGLE_CLOUD_PROJECT=pmo-piloto-gemini-enterprise,GOOGLE_CLOUD_LOCATION=europe-west1,GOOGLE_GENAI_USE_VERTEXAI=TRUE,SIAX_ENVIRONMENT=produccion" `
  --set-env-vars="SIAX_USERNAME=GeminiUsr#25" `
  --set-env-vars="SIAX_PASSWORD=GeminiP4ss#25" `
  --set-env-vars="SIAX_URL=https://www.senassur.com:8086/Xena/ServiciosGemini.svc"
