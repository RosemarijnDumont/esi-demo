// This file is a placeholder to indicate where old API calls were made.
// You need to replace all direct API calls that exposed API keys with calls to `makeProxiedApiRequest`.
// Example of an old API call that needs to be migrated:
// fetch(`https://external-api.com/data?apiKey=${YOUR_API_KEY}`)
//   .then(response => response.json())
//   .then(data => console.log(data));

// After migration, it should look something like this:
// import { makeProxiedApiRequest } from './services/api-proxy';
// makeProxiedApiRequest('get', '/data', { params: { someParam: 'value' } })
//   .then(data => console.log(data));

// Make sure to remove any client-side storage or hardcoding of API keys after migration.