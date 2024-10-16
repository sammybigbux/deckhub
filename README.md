# DeckHub - Certification Prep Platform

[DeckHub](https://deckhubapp.web.app/) is an interactive learning platform that uses modern cognitive research to help students prepare for certification exams. The platform provides multiple-choice and open-ended question formats and offers real-time feedback to guide learners through exam-related content. Our goal is to improve how students learn and retain information through intelligent systems powered by machine learning and data-driven insights.

### Initial Setup
Secure files from Google Drive are required to host this locally but if you push to `staging` branch the Github Actions will deploy to Google Cloud.

1. **Install dependencies:**
     ```bash
     npm install
     ```

2. **Set up a `.env` file in the main directory:**
     ```bash
     LOCAL=True
     OPEN_API_KEY=(your OpenAI key)
     ```

3. **Set up a `.env` file in the backend directory:**
     ```bash
     STRIPE_SECRET_KEY=(your Stripe secret key)
     WEBHOOK_SECRET=(your webhook secret)
     ```

4. **Navigate to the backend directory and install Python requirements:**
     ```bash
     pip install -r requirements.txt
     ```

5. **Place the `firebase_key.json` file into the backend directory:**
   - This is a secret file located in the Google Drive and needs to be requested from the project owner.

6. **Create an OpenAI assistant and update the assistant ID:**
   - Visit [OpenAI Playground](https://platform.openai.com/playground/), create an AI assistant, and use the prompt provided in the Google Drive.
   - Update the `assistant_id` at the top of the `app.py` file to the assistant you created. You will need to replace the current assistant ID with the one generated from the assistant you're using:
     ```python
     assistant_id = "asst_your_new_assistant_id"
     ```

7. **Run the backend:**
   - From the `/src/backend` directory, start the backend server:
     ```bash
     python app.py
     ```

8. **Run the frontend:**
   - Go back to the main directory, and start the development server:
     ```bash
     npm run dev
     ```

## Project Structure
You can find a guide to each section in the README.md files in their respective directories. The project consists of the following main components:

- **Frontend**: Located in the `/routes` directory, the frontend is built using Vite and Svelte. It handles the user interface, interactions, and communication with the backend services.

- **Backend**: Found in the `/src/backend` directory, the backend is built using Flask. It handles API endpoints, user sessions, and database interactions via Firebase. The backend also includes routes for managing user progress, retrieving questions, and other services.

- **CI/CD**: Continuous Integration and Continuous Deployment (CI/CD) are managed through GitHub Actions. The workflows in the `/workflows` directory automate the process of deploying the frontend to Firebase and the backend to Google Cloud Run.
