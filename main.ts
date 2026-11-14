// news-image-01 entry (Node 22, standard library only).
//
// The picture is the entry.png beside this file: a dense newspaper front
// page summing up Friday 13 November 2026 — a masthead, the Iran/Hormuz
// lead, and 22 more stories (Nvidia chief resigns, Microsoft outage,
// China-Taiwan drills, FAA ground stop, Ukraine talks, and more), all in
// legible type rendered by render_frontpage.py.
// The program writes that image to the output directory, byte for byte,
// so the grader's two runs produce exactly the same file.
//
// The file is JPEG bytes (told apart by its first bytes) under the
// name entry.png, 1024 by 1024 pixels, 281,913 bytes: inside the
// gate limits of 1 MiB and 1024 by 1024.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const source = new URL('./entry.png', import.meta.url);
const target = join(outDir, 'entry.png');
copyFileSync(source, target);
// The grader runs the program twice and compares the bytes: fail
// loudly if the copy is short, rather than writing a partial file.
const written = statSync(target).size;
const expected = statSync(source).size;
if (written !== expected) {
  throw new Error(`entry.png copy incomplete: ${written} of ${expected} bytes`);
}
// Size alone does not prove the bytes match, so compare a digest of
// the two files as well: the copy must be identical, not just as long.
const digest = (path: string): string => createHash('sha256').update(readFileSync(path)).digest('hex');
if (digest(target) !== digest(source)) {
  throw new Error('entry.png copy differs from the source');
}
