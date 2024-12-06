import { loadStripe } from '@stripe/stripe-js';
import { stripeCustomerIdStore, userId } from '$lib/firebase'; // Import auth and userName here
import { get } from 'svelte/store';

const isLocalhost = false
const base_url = import.meta.env.VITE_BASE_URL;

let stripePromise;

// Function to load Stripe and return the Stripe instance
export function getStripe() {
    if (!stripePromise) {
        stripePromise = loadStripe('pk_live_51Q4p5TFKyW9aNIed73wtxXwwUyjW7eGWity6yB5bQc77eLh2ZymiyricwF01PNjn83bCxn4Tqie1cbJB3inNCko500ZP75GFjJ'); // Replace with your Stripe publishable key
    }
    return stripePromise;
}

// Function to handle checkout session creation and redirection to Stripe
export async function createCheckoutSession(productId, priceId, product_name) {
    const stripe = await getStripe();

    // Get values from the Svelte stores using `get()`
    const user_id = get(userId); // Get the userId value
    const stripe_customer_id = get(stripeCustomerIdStore); // Get the Stripe customer ID

    const response = await fetch(`${base_url}/api/create-checkout-session`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            product_id: productId,
            user_id: user_id, // Pass the user ID to track it on the backend
            stripe_customer_id: stripe_customer_id, // Pass Stripe customer ID for creating session
            price_id: priceId,
            product_name: product_name
        })
    });

    const session = await response.json();

    // Redirect the user to the Stripe Checkout page
    await stripe.redirectToCheckout({ sessionId: session.id });
}

