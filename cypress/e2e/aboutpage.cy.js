describe('About page component rendering tests', () => {
    // Start on the about page, being logged in is irrelevant
    beforeEach(() => {
        cy.visit('http://localhost:5173/about');
    });
    
    it('Ensures the "About" component renders correctly', () => {
        // Check that the component exists and is visible
        cy.contains('h1', 'About')
            .should('exist')
            .should('be.visible');
    });

    it('Ensures the "Why is it faster?" component renders correctly', () => {
        cy.contains('h3', 'Why is it faster?')
            // Check that the component exists invisibly
            .should('exist')
            .should('not.be.visible')

            // Check that the component becomes visible when scrolled to        
            .scrollIntoView()
            .should('be.visible');
    });

    it('Ensures the "Adaptivity" component renders correctly', () => {
        cy.contains('h3', 'Adaptivity')
            // Check that the component exists invisibly
            .should('exist')
            .should('not.be.visible')

            // Check that the component becomes visible when scrolled to
            .scrollIntoView()
            .should('be.visible');
    });

    it('Ensures the "Instant feedback" component renders correctly', () => {
        cy.contains('h3', 'Instant feedback')
            // Check that the component exists invisibly
            .should('exist')
            .should('not.be.visible')

            // Check that the component becomes visible when scrolled to
            .scrollIntoView()
            .should('be.visible');
    });

    it('Ensures the "Fast mastery." component renders correctly', () => {
        cy.contains('h3', 'Fast mastery.')
            // Check that the component exists invisibly
            .should('exist')
            .should('not.be.visible')

            // Check that the component becomes visible when scrolled to
            .scrollIntoView()
            .should('be.visible');
    });

    it('Ensures the "No Subscription" component renders correctly', () => {
        cy.contains('h3', 'No Subscription')
            // Check that the component exists invisibly
            .should('exist')
            .should('not.be.visible')

            // Check that the component becomes visible when scrolled to
            .scrollIntoView()
            .should('be.visible');
    });

    it('Ensures the Back to Top button works', () => {
        // Check that the back to Top button exists
        cy.contains('Back to Top')
            .click();

        // Ensure the back to top button sends the user to the top of the screen
        cy.url().should('include', '#top');
    });
  });