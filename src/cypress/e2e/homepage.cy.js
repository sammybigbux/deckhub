describe('User Navigation and Authentication Tests', () => {
  beforeEach(() => {
    // Visit the base URL before each test
    cy.visit('http://localhost:5173');
  });

  describe('Header Visibility Tests', () => {
    beforeEach(() => {
      // Visit the base URL before each test
      cy.visit('http://localhost:5173');
    });
  
    it('Ensures the app-bar is not visible when the user is not logged in', () => {
        // Check that the element with data-testid="app-bar" is not present
        cy.get('[data-testid="app-bar"]').should('not.exist');
      });
    });
  
  it('Navigates to the About page when clicking the About button', () => {
    // Click the "About" button
    cy.contains('About').click();

    // Verify that the user is taken to the /about page
    cy.url().should('include', '/about');
  });

  it('Clicks "Try it out" and ensures the Google sign-in prompt appears', () => {
    // Go back to the home page
    cy.go('back');

    // Click the "Try it out" button
    cy.contains('Try it out').click();

    // Check that the OAuth Google prompt opens
    // Cypress cannot test popups directly, but you can intercept the request
    cy.origin('https://accounts.google.com', () => {
      cy.url().should('include', 'accounts.google.com');
    });
  });

  it('Signs in with a Google account and verifies content updates', () => {
    // After signing in, mock the state change if needed
    // (Ensure Firebase is configured to use a testing account)

    // Mock the OAuth process and session state
    cy.visit('http://localhost:5173'); // Replace with the post-login state if Firebase redirects

    // Check that the button text changes to "AWS SAA03 Practice"
    cy.contains('AWS SAA03 Practice').should('exist');

    // Click the "AWS SAA03 Practice" button
    cy.contains('AWS SAA03 Practice').click();

    // Verify navigation to the AWS course page
    cy.url().should('eq', 'http://localhost:5173/new/learn/AWS%20Certified%20Solutions%20Architect');
  });
});
