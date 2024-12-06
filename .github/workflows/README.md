# GitHub Actions CI/CD System Summary

The project uses GitHub Actions to automate the deployment of both the backend and frontend. Separate workflows handle deployments to the production and staging environments for both the backend and frontend.

---

#### 1. **Backend Deployment to Production** (`deployment-production-backend.yml`)

- **Trigger**: This workflow triggers when changes are pushed to the `main` branch and those changes are within the `src/backend/` directory.
- **Key Steps**:
  1. Checkout the code using `actions/checkout@v4`.
  2. Authenticate with Google Cloud using a service account.
  3. Build a Docker image for the backend and push it to Google Container Registry (GCR).
  4. Deploy the Docker image to Google Cloud Run (production) and set environment variables like `OPENAI_API_KEY`, `STRIPE_SECRET_KEY`, etc.
  5. Run backend tests using `unittest`.

#### 2. **Frontend Deployment to Production** (`deployment-production-frontend.yml`)

- **Trigger**: This workflow triggers on pushes to the `main` branch.
- **Key Steps**:
  1. Checkout the code using `actions/checkout@v4`.
  2. Install dependencies and build the frontend using `npm ci` and `npm run build`.
  3. Authenticate with Google Cloud and deploy the frontend to Firebase Hosting (production) using the Firebase CLI.
  4. Echo the production URL for easy reference (`https://deckhub.web.app/`).

---

#### 3. **Backend Deployment to Staging** (`deploy-staging-backend.yml`)

- **Trigger**: This workflow triggers on pushes to the `staging` branch and only runs if there are changes in the `src/backend/` directory.
- **Key Steps**:
  1. Checkout the code using `actions/checkout@v4`.
  2. Authenticate with Google Cloud using a service account.
  3. Build a Docker image for the backend and push it to GCR.
  4. Deploy the Docker image to Google Cloud Run (staging) and set environment variables.
  5. Run backend tests using `unittest`, but this time against the staging URL (`https://deckhub-backend-staging-1086653848406.us-central1.run.app`).

#### 4. **Frontend Deployment to Staging** (`deploy-staging-frontend.yml`)

- **Trigger**: This workflow triggers on pushes to the `staging` branch.
- **Key Steps**:
  1. Checkout the code using `actions/checkout@v4`.
  2. Install dependencies and build the frontend using `npm ci` and `npm run build`.
  3. Authenticate with Google Cloud and deploy the frontend to Firebase Hosting (staging).
  4. Echo the staging URL for easy reference (`https://deckhubapp--staging-8dva1oxn.web.app/`).

---

### Summary of Deployment Process:
- **Backend**: The backend is deployed to Google Cloud Run for both staging and production environments, with Docker images built for each push.
- **Frontend**: The frontend is deployed to Firebase Hosting, with separate channels for staging and production.
- **Environment Variables**: Sensitive information like API keys and credentials are stored in GitHub secrets and passed as environment variables during deployment.
