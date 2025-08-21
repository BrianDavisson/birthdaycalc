# GCP Deployment Commands for Birthday Calculator

# 1. Set your project ID (replace with your actual project ID)
export PROJECT_ID="your-gcp-project-id"
gcloud config set project $PROJECT_ID

# 2. Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# 3. Build and deploy using Cloud Build
gcloud builds submit --config cloudbuild.yaml .

# Alternative: Manual deployment steps
# Build the container
# gcloud builds submit --tag gcr.io/$PROJECT_ID/bdaycalcwebappv082025 .

# Deploy to Cloud Run
# gcloud run deploy bdaycalcwebappv082025 \
#   --image gcr.io/$PROJECT_ID/bdaycalcwebappv082025 \
#   --region us-west1 \
#   --platform managed \
#   --allow-unauthenticated \
#   --min-instances 0 \
#   --max-instances 1 \
#   --memory 512Mi \
#   --cpu 1000m \
#   --port 5000

# 4. Get the service URL
gcloud run services describe bdaycalcwebappv082025 --region=us-west1 --format='value(status.url)'
