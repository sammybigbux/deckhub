import { writable } from 'svelte/store';

export const totalTerms = writable(1);  // Start with an initial value of 1
export const solvedTerms = writable(0);  // Start with an initial value of 0


export const totalCompleted = writable(0); // these are just for the timer block
export const totalIncorrect = writable(0);
export const total_questions = writable(0);
