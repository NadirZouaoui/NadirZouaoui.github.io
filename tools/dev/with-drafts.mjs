// Run an astro command with draft entries visible (cross-platform replacement for `SHOW_DRAFTS=1 astro ...`).
//   npm run build:drafts      -> builds into dist-drafts/ (NOT dist/) with draft entries included. Preview only, never deploy.
//   npm run preview:drafts    -> build:drafts, then serve dist-drafts/
import { spawn } from 'node:child_process';

const args = process.argv.slice(2);
const run = (cmd) =>
  new Promise((resolve) => {
    const p = spawn(cmd[0], cmd.slice(1), { stdio: 'inherit', shell: process.platform === 'win32', env: { ...process.env, SHOW_DRAFTS: '1' } });
    p.on('exit', (code) => resolve(code ?? 1));
  });

let code = await run(['npx', 'astro', 'build', '--outDir', 'dist-drafts']);
if (code === 0 && args.includes('--preview')) code = await run(['npx', 'astro', 'preview', '--outDir', 'dist-drafts']);
process.exit(code);
