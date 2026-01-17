// Import with `import * as Sentry from "@sentry/node"` if you are using ESM
const Sentry = require("@sentry/node");

Sentry.init({
  dsn: "https://66f1182e2b7fdc0a34150100e3d0c6a3@o4509759301877760.ingest.us.sentry.io/4509799280410624",

  // Setting this option to true will send default PII data to Sentry.
  // For example, automatic IP address collection on events
  sendDefaultPii: true,
});