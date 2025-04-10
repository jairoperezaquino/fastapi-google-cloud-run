# FastAPI - Google Cloud Run

A template for deploying a FastAPI application on Google Cloud Run.

## Features

- **Cloud Logging**: Integration with Google Cloud Logging, ensuring logs are captured with the appropriate severity levels. ⭐ Credits to Florian Flock's [article](https://dev.to/floflock/enable-feature-rich-logging-for-fastapi-on-google-cloud-logging-j3i).
- **CI/CD**: Automated deployment using GitHub Actions. 🚀
- **HTTP Async Support**: Built-in support for async HTTP requests using [httpx](https://github.com/encode/httpx) for better performance and scalability.
- **API Key Authentication**: Support for API Key authentication through both Query Parameters and HTTP Headers.

## Setup

### Prerequisites

- Python 3.12+
- Docker

### Run Locally

1. **Create a virtual environment**: You can follow the [FastAPI guide](https://fastapi.tiangolo.com/virtual-environments/).

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   fastapi dev
   ```

### Deployment

Deployment is automated with GitHub Actions, but you'll need to set up a few items first:

1. **GCP Project**: Of course!

2. **Workload Identity Federation**: This allows GitHub to authenticate to your GCP project for deployment. [This video](https://youtu.be/ZgVhU5qvK1M?si=K2r1wz1wAv1FwtJn) is a helpful resource.

3. **Google Artifact Registry Repository**: This is where Docker images will be stored.

#### Required Secrets

Set the following secrets in your GitHub repository (do not expose these publicly):

- `SERVICE_NAME`: Name of your service, e.g., `fastapi-cloud-run`.
- `GCP_PROJECT_ID`: Your project ID, e.g., `9876543210`.
- `GCP_WIF_PROVIDER`: Your Workload Identity Federation provider full name, formatted as `projects/${PROJECT_ID}/locations/global/workloadIdentityPools/${POOL_NAME}/providers/${PROVIDER_NAME}`.
- `GCP_WIF_SA_EMAIL`: Service account email to impersonate.

The deployment workflow will:
1. Run Ruff checks for code quality
2. Build and push the Docker image to Google Artifact Registry
3. Deploy the service to Cloud Run in the specified region

Refer to `.github/workflows/push_main.yml` for more details on the deployment process.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
