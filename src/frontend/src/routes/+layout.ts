// Render entirely on the client: the Firebase Web SDK reads Firestore in the
// browser, so there is no server pass to prerender.
export const ssr = false;
export const prerender = false;
