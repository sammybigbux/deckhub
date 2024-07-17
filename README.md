# Deckhub
![Deckhub](https://github.com/sammybigbux/deckhub/assets/150755716/aed88691-d658-461e-bef3-a442c6ba8a61)




# Summary
A platform to buy and sell flashcard decks for Quizlet and Anki where every flashcard deck is:
- **Comprehensive**: Covers all the information in the relevant text.
- **Relevant**: Is up to date.

The platform offers the following tools to help creators ensure these two characteristics:
- **Verification Model (RAG)**: Ensures that the given flashcards are broadly representative of the information.
- **Generative Model**: Helps produce large flashcard sets.



# Development Roadmap

## Define Requirements
- Identify features and create a requirements document.
- Determine the technology stack.

## Design the Architecture
- Develop the database schema (database diagram) and insert test data.
- Define the API (RESTful) endpoints to communicate between front and back end (look at Firebase).

## Front End Development
- Create a wireframe of the expected end goal (Figma).
- Use Svelte to develop the front end using mobile-first design principles.
- Use Bootstrap to style components (I love Bootstrap).

## Back End Development
- Set up Firebase and configure it.
- Use Firebase Authentication for user management, Firestore for storage, and Cloud Functions for the backend logic.
- Integrate Firestore for database operations.

## Payment Integration
- Integrate Stripe (we love Stripe).
- Implement logic with Firebase Cloud Functions to handle payments, generate receipts, and manage transactions.

## Testing
- Write unit tests using the Robot Framework (front end) or Cypress and Python with Pytest for the API calls. 
- Set up user testing with connections.

## Deployment
- Deploy the website using Firebase Hosting.
- Set up GitHub Actions to create a CI/CD pipeline.
- Use Firebase Hosting to set up a domain name.

## Maintenance
- Use Firebase Analytics and Crashlytics to track performance and errors.
- Add a channel for users to report incidents.

## Other notes
- Use angolia for search (eventually)



# Created by
![Logo](https://github.com/sammybigbux/deckhub/assets/150755716/ff21b68b-7861-41ff-9635-6dfccae00150)


