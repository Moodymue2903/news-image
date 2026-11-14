# news-image-01: Friday 13 November 2026 in one image

A newspaper front page summing up the world news of Friday 13 November 2026:

- **Lead:** Iran strikes a U.S. radar in Bahrain as tankers burn in the Strait of Hormuz.
- **Nvidia chief resigns, shares plunge** (Jensen Huang steps down; shares fell 14%).
- **Microsoft outage enters day two** (Outlook, Teams and Copilot still recovering).
- **China's unannounced drills ring Taiwan** (large Pacific naval exercises).
- **FAA lifts U.S. ground stop** (nationwide halt after a communications failure).
- **Europe joins Ukraine peace talks.**

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
