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
    cy.contains('About').should('be.visible');
    cy.contains('About').click();

    // Verify that the user is taken to the /about page
    cy.url().should('include', '/about');
  });

  it('Clicks "Try it out" and ensures the Google sign-in prompt appears', () => {
    // Go to the about page
    cy.contains('About').click();
    
    // Go back to the home page
    cy.go(-1);

    // Click the "Try it out" button
    cy.contains('Try it out').click();

    // Check that the OAuth Google prompt opens
    // Cypress cannot test popups directly, but you can intercept the request
    cy.origin('https://accounts.google.com', () => {
      cy.url().should('include', 'accounts.google.com');
    });
  });
});
