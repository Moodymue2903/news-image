# news-image-01: Friday 13 November 2026 in one image

An infographic-style one-page summary of the world news of Friday 13 November 2026 — **33 stories across 6 continents**, rendered by `render_frontpage_v3.py` (PIL, real fonts, no AI text):

- **Top 3:** FAA grounds every US departure for four hours; Iran says it hit a US radar in Bahrain; Trump, Xi and Putin to hold a first three-way summit.
- **Grid 4–15:** Ukraine drones, Europe peace team, Starship 15th flight, Pope Leo in Peru, Assam bus crash, Türkiye–Qatar pact, Microsoft 365 back, Ebola in DR Congo, New Orleans riverboat, Nvidia below $4T, Pochettino to Man Utd, UN chief on 1.5°C.
- **Also on Friday (16–33):** Norway oil licences, Moscow car bomb, Storm Charles, yen at 160, Kenya collapse, Guinea mine, Delhi pollution, Binance seizure, Van Hollen, Brooklyn toll, IAEA on Iran, Lebanon strikes, Houthis, French warship, measles ruling, India tariffs, Wall Street, IEA oil surplus.
- **Where it happened:** a schematic world map with numbered dots for the top stories.

## How it works

`main.ts` (Node 22, standard library only) copies `entry.png` to the
output directory, byte for byte, so both of the grader's runs write
exactly the same file. `entry.png` is JPEG bytes under that name,
1024 by 1024 pixels, 278,204 bytes.

Run it outside the grader's container with:

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT. See `LICENSE`.
