/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Bind resources to your worker in `wrangler.jsonc`. After adding bindings, a type definition for the
 * `Env` object can be regenerated with `npm run cf-typegen`.
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

// !mark(10:11)
import * as Sentry from "@sentry/cloudflare";

export default Sentry.withSentry(
  (env) => ({
    dsn: "https://[SENTRY_KEY]@[SENTRY_HOSTNAME].ingest.us.sentry.io/[SENTRY_PROJECT_ID]",
    tracesSampleRate: 1.0,
  }),
  {
    async fetch(request, env, ctx) {
      // ✅ Bug fixed: Removed undefined.call() that was causing TypeError
      return new Response("Hello World!");
    },
  } satisfies ExportedHandler<Env>,
);
