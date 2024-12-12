import { writable } from 'svelte/store';

export const totalTerms = writable(1);  // Start with an initial value of 1
export const solvedTerms = writable(0);  // Start with an initial value of 0


export const totalCompleted = writable(0); // these are just for the timer block
export const totalIncorrect = writable(0);
export const total_questions = writable(0);

export const sectionName = writable(''); // this is for the section name
export const term_from_overview = writable(''); // this is for the term from the overview page
export const moduleName = writable(''); // this is for the module name
export const active_section_title = writable(''); // this is for the active section title
export const already_initialized = writable(true) // this is to see if we clicked the resume or overview before going into chat
