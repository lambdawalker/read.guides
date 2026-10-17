# read.guides

Small illustrated Spanish books for reading together. **Se cayó** has six animals, twelve landscape story pages and a cover. Each animal has two separate images/pages: an action, then a gentle fall.

[Download the latest release](https://github.com/lambdawalker/read.guides/releases/latest) · [Builds](https://github.com/lambdawalker/read.guides/actions/workflows/books.yml) · [Letter tracker](docs/book-series-notes.md)

## Downloads

Only two release files:

- **01-se-cayo.pdf** — landscape book, 12 × 8 inches, with bookmarks for pato, gato, mono, vaca, llama and oso.
- **01-se-cayo-assets.zip** — one `assets/` folder with the group cover and twelve separate landscape PNG illustrations, `book.yaml`, font/license and editorial notes.

The PDF has 13 pages: cover, then six two-page stories. Llama occupies story pages 9–10; bear occupies 11–12. Illustrations are text-free, approximately 1086 pixels wide; text is added by Python as selectable PDF text. The renderer preserves image proportions. This is a reading/home-print PDF, without press bleed or booklet imposition.

## Build locally (Windows, macOS or Linux)

Install Python 3.11+ and [uv](https://docs.astral.sh/uv/getting-started/installation/). From the repository:

```sh
uv sync --locked
uv run python scripts/build_book.py books/01-se-cayo/book.yaml --output dist/01-se-cayo
```

Output contains the PDF, the uncompressed `assets/` folder and its ZIP for downloading. No separate page/illustration ZIPs, manifest or checksum download is generated. No image API key or system font is needed.

To rebuild an extracted assets bundle:

```sh
uv run python scripts/build_book.py path/to/assets/book.yaml --output dist/rebuilt
```

## Edit a book

Edit `book.yaml`: ordered pages with `image`, `text` and `animal`; `animals` lists the expected stories in order. The renderer requires exactly two consecutive pages per listed animal. An optional `cover` has `image`, `text` and `subtitle`. Image/font paths are relative to the YAML and must stay inside its folder.

Layout: `page_width_inches` and `page_height_inches` (3–16), `font_size_pt` (12–80), `text_baseline` (0.05–0.17 of page height from the bottom), and `text_color`. Current format is 12 × 8 inches, with 32-point text. The bottom 22% is reserved for text. Missing assets and overflowing text fail before output is changed.

Use a dedicated empty output folder initially. Rebuilds require the renderer's ownership marker and reject symlinks. The tool replaces its generated assets folder and removes the old page/illustration bundles when upgrading an owned output folder.

## Actions and releases

PRs, pushes to `main` and **Run workflow** run tests and build the PDF/assets. Actions keeps downloadable build artifacts for 30 days. Successful main builds publish `book-01-v<version>` when absent. Bump `version` in the YAML for a new release; existing releases remain unchanged. Publication uses the built-in workflow token with `contents: write`.

```sh
uv run python -m unittest discover -s tests -v
```

The tests verify all six stories, explicit llama/bear text, landscape PDF pages, bookmarks, simplified bundle contents, and validation failures.

## Editorial rules

Keep **cayó**. Content words have mostly two syllables, at most three. Make the protagonist stand out: saturated animal, dark outlines, soft contrasting background. See [manuscript and art notes](books/01-se-cayo/README.md).
