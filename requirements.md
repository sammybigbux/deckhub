# Deckhub Requirements Document

## Introduction
### Purpose
The purpose of this document is to outline the requirements for Deckhub, a platform for buying and selling flashcard decks for Quizlet and Anki.

### Scope
This document covers all functional and non-functional requirements for the development of Deckhub.

### Definitions, Acronyms, and Abbreviations
- **RAG**: Retrieval-Augmented Generation

## Project Overview
### Project Description
Deckhub is a platform where users can buy and sell flashcard decks for Quizlet and Anki. The platform ensures flashcard decks are comprehensive and relevant.

## Functional Requirements
### User Authentication
- **FR-01**: The system shall allow users to register using email and password.
- **FR-02**: The system shall allow users to log in using email and password.
- **FR-03**: The system shall allow users to reset their password.

### Flashcard Deck Management
- **FR-04**: The system shall allow users to create new flashcard decks.
- **FR-05**: The system shall allow users to edit existing flashcard decks.
- **FR-06**: The system shall allow users to delete flashcard decks.
- **FR-07**: The system shall allow users to search for flashcard decks.
- **FR-08**: The system shall allow users to view their purchased flashcards.
- **FR-09**: The system shall allow users to download their purchased flashcards.

### Buying and Selling
- **FR-10**: The system shall allow users to list flashcard decks for sale.
- **FR-11**: The system shall allow users to purchase flashcard decks.
- **FR-12**: The system shall process payments using Stripe.
- **FR-13**: The system shall generate receipts for purchases.

## Non-Functional Requirements
### Performance
- **NFR-01**: The system shall support up to 10,000 simultaneous users.

### Security
- **NFR-02**: The system shall enforce SSL for all communications.

### Usability
- **NFR-03**: The system shall have a responsive design, usable on both desktop and mobile devices.

## Use Cases
### Use Case 1: User Registration
- **Actors**: User
- **Description**: A user registers an account using their email and password.
- **Preconditions**: User is prompted to register upon navigating to the homepage
- **Postconditions**: User account is created.
- **Steps**:
  1. User navigates to the registration page.
  2. User enters their email and password or selects a federated account.
  3. User submits the registration form.
  4. System validates the information and creates the user account.
  5. System sends a confirmation email to the user.

### Use Case 2: User Login
- **Actors**: User
- **Description**: A user logs into their account using their email and password or federated account.
- **Preconditions**: User has a registered account and is on the login page.
- **Postconditions**: User is logged into their account.
- **Steps**:
  1. User navigates to the login page.
  2. User enters their email and password or selects their registered account.
  3. User submits the login form.
  4. System validates the credentials.
  5. System logs the user into their account and redirects to the dashboard.

### Use Case 3: Upload Flashcard Deck
- **Actors**: User
- **Description**: A user uploads a new flashcard deck.
- **Preconditions**: User created a deck in Quizlet or Anki and exported to csv and has selected 
- **Postconditions**: A new flashcard deck is created and saved in the system.
- **Steps**:
  1. User navigates to the "Upload Deck" page.
  2. User enters the deck title and description.
  3. User enters the asking price
  4. User selects a payment method
  5. User chooses a .csv file to upload
  6. User saves the deck.
  7. System saves the deck in the database and confirms the creation to the user.

### Use Case 4: Delete Flashcard Deck
- **Actors**: User
- **Description**: A user deletes an existing flashcard deck.
- **Preconditions**: User is logged into their account and has an existing deck.
- **Postconditions**: The flashcard deck is removed from the system.
- **Steps**:
  1. User navigates to their flashcard decks list.
  2. User selects the deck they want to delete.
  3. User confirms the deletion.
  4. System deletes the deck from the database and confirms the deletion to the user.

### Use Case 5: Search for Flashcard Decks
- **Actors**: User
- **Description**: A user searches for flashcard decks.
- **Preconditions**: User is logged into their account.
- **Postconditions**: User is presented with a list of flashcard decks that match the search criteria.
- **Steps**:
  1. User navigates to the search page.
  2. User enters search criteria (e.g., keywords, subject).
  3. User submits the search form.
  4. System searches the database for decks that match the criteria.
  5. System displays the search results to the user.

### Use Case 6: Purchase Flashcard Deck
- **Actors**: User
- **Description**: A user purchases a flashcard deck.
- **Preconditions**: User is logged into their account and has selected a deck to purchase.
- **Postconditions**: The transaction is processed, and the user gains access to the purchased deck.
- **Steps**:
  1. User selects a flashcard deck to purchase.
  2. User clicks the "Buy" button.
  3. User enters payment information.
  4. User confirms the purchase.
  5. System processes the payment via Stripe.
  6. System confirms the purchase and adds the deck to "my decks"
  7. A recipt is emailed to the user

### Use Case 7: Handle Payment Transaction
- **Actors**: System, User, Stripe
- **Description**: The system handles payment transactions via Stripe.
- **Preconditions**: User has initiated a purchase.
- **Postconditions**: The payment is processed, and the transaction details are saved.
- **Steps**:
  1. User initiates a purchase.
  2. System collects payment information.
  3. System sends payment information to Stripe.
  4. Stripe processes the payment.
  5. System receives payment confirmation from Stripe.
  6. System saves the transaction details in the database.
  7. System confirms the purchase to the user.

### Use Case 8: User Password Reset
- **Actors**: User
- **Description**: A user resets their password using their email.
- **Preconditions**: User has forgotten their password and has access to the password reset page.
- **Postconditions**: User's password is reset.
- **Steps**:
  1. User navigates to the password reset page.
  2. User enters their email address.
  3. User submits the password reset form.
  4. System sends a password reset email to the user.
  5. User clicks the link in the email and is redirected to a reset page.
  6. User enters a new password and submits the form.
  7. System updates the user's password in the database and confirms the reset to the user.
 
**TO BE ADDED UPON NEXT MILESTONE, Generative AI tools**


## User Stories
- **As a user, I want to register an account so that I can access the platform.**
- **As a user, I want to log into an account so that I can access the platform.**
- **As a seller, I want to list my flashcard decks for sale so that I can earn money.**
- **As a buyer, I want to purchase flashcard decks so that I can use them for studying.**

## Assumptions and Dependencies
### Assumptions
- Users will have internet access.
- Users will have basic digital literacy.

### Dependencies
- Integration with Stripe for payment processing.
- Usage of Firebase for backend services.

## Glossary
- **RAG**: Retrieval-Augmented Generation
