# Five Layers Monthly: how to update

The monthly page is one self-contained HTML file built from three pieces:

- `template.html`: layout, styles and animations. Change only for design updates.
- `framework.json`: the evergreen framework (what each layer converts, how it gets paid, its scarce input, what drives its multiple; the three principles; the bottleneck timeline). Update the timeline once a year or when the bottleneck moves.
- `data_YYYY_MM.py`: the month's content and its sources. Copy last month's file and edit.

Build:

```
python3 data_2026_10.py oct.json      # writes the month's data
python3 build.py oct.json five_layers_2026-10.html
python3 make_blank.py oct.json blank.json && python3 build.py blank.json five_layers_TEMPLATE.html   # optional skeleton
```

Writing rules used in the data file:
- `**bold**` for emphasis; `_word_` gives the gradient accent (titles only).
- Cite with `[@key]` or `[@a,@b]`, where the key is in `SOURCES`. Footnotes are numbered automatically in page order; the build fails on an unknown key.
- Layer `pulse`: `tight` (0–100, supply tightness, editorial), `temp` (1 cool, 2 warm, 3 hot), `flow` (1 in, 0 mixed, −1 out), `move` (simple average of the ITIN names listed in `basket`).
- Holdings come from iA Clarington's public top-25 list; the "other" weight is computed so the donut sums to 100%.

Monthly checklist: refresh the public top 25 (iaclarington.com fund page), the share-price moves, the five layers' themes, movers, headline, handoff and radar, the rotations, ripples, calendar and talking points; then have compliance review.
