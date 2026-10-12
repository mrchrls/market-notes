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

## v2 (short, tabbed) edition
`template_v2.html` shows the month as five tabs (The month, Money moves, ITIN, Radar, Talking points); each layer opens in a side drawer.
It reads the same data plus a `brief` block (headline takeaways, shorter decks) and a `watch` block: the forward radar of model cycles, IPOs, launches, policy deadlines and disputes, each tagged confirmed / likely / speculative and grouped by horizon. Earnings dates stay in `calendar`. The header uses the all-white reversed logo (`logo_en_white.txt`).

    python3 data_2026_10.py oct.json
    python3 data_2026_10_brief.py oct.json oct_v2.json
    python3 extract_i18n.py oct_v2.json strings_en.json     # adds any new English strings, keeps existing ids
    # translate the new ids into strings_fr.json (Québec French; keep [@keys], **bold**, _accent_)
    python3 build.py oct_v2.json out_v2.html template_v2.html --fr strings_fr.json

### English / French
The page has an EN/FR toggle (header). It opens in the reader's browser language, remembers the choice,
and `?lang=fr` forces French. Interface labels live in the `UI` dictionary in `template_v2.html`; month
content comes from `strings_fr.json`, paired with `strings_en.json` by id. The build lists any English
string with no French yet (it stays in English until translated). French uses the terms from Charles's
own decks: étage, le Fonds, titres, Puces, Jeton, À l’usage exclusif des courtiers.
