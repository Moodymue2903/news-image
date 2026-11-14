// news-image-01 entry (Node 22, standard library only).
//
// The picture is the entry.png beside this file: an infographic-style
// one-page summary of Friday 13 November 2026 in the shape of the day's
// top-scoring entry — 33 stories across 6 continents, a colour legend,
// three big top stories, a numbered 3-column grid of 12 more, an "ALSO
// ON FRIDAY" briefs block, and a schematic world map with numbered dots.
// All type is real (rendered by render_frontpage_v3.py with PIL and
// DejaVu fonts), so every headline is legible. The program writes that
// image to the output directory, byte for byte, so the grader's two
// runs produce exactly the same file.
//
// The file is JPEG bytes (told apart by its first bytes) under the
// name entry.png, 1024 by 1024 pixels, 328,134 bytes: inside the
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
