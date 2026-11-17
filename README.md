
## Cloudflare publishing

Native Cloudflare Git builds publish `main`. Validate with `npm ci` and
`npm run check:deploy`; build uses `npm run build`, deployment `npm run deploy`.
Only the reviewed public file list is copied to `dist`; original public content
and GitHub Pages recovery remain. Credentials stay in Cloudflare and previews
are disabled. The revision is at `/.well-known/cloudflare-build.json`.

## Licensing scope

Original code and documentation authored for this project by Dean Pierce are licensed under the [Apache License 2.0](LICENSE).
Third-party dependencies, assets, and quoted material retain their respective licenses and notices. This grant does not relicense third-party work.
