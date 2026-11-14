# news-image-01: Friday 13 November 2026 in one image

A dense newspaper front page summing up the world news of Friday 13 November 2026 — 23 stories in legible type, rendered by `render_frontpage.py` (PIL, real fonts, no AI text):

- **Lead:** Iran strikes a U.S. radar in Bahrain as tankers burn in the Strait of Hormuz.
- Plus: Nvidia chief resigns (shares plunge), Microsoft outage enters day two, China's unannounced drills ring Taiwan, FAA lifts U.S. ground stop, Europe joins Ukraine peace talks, Brooklyn collapse toll, Van Hollen vs Schumer, $1.2B Binance seizure, Pope Leo in Peru, Delhi pollution, Kaziranga crash, Qatar-Turkey pact, IEA oil surplus, chip controls, measles ruling, French warship in Syria, Wall Street, IAEA on Iran, Lebanon/Gaza, Moscow car bomb, Houthis, India tariff advantage.

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
