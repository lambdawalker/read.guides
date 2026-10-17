# read.guides

Small illustrated Spanish books for reading together. **Book 1: Se cayó** has six animals, twelve story pages and a cover.

[Download the latest release](https://github.com/lambdawalker/read.guides/releases/latest) · [Builds](https://github.com/lambdawalker/read.guides/actions/workflows/books.yml) · [Letter tracker and series notes](docs/book-series-notes.md)

## Build locally (Windows, macOS or Linux)

Install Python 3.11+ and [uv](https://docs.astral.sh/uv/getting-started/installation/), then run from this repository:

```sh
uv sync --locked
uv run python scripts/build_book.py books/01-se-cayo/book.yaml --output dist/01-se-cayo
```

No image API keys, system fonts or external font downloads are needed. Images and a licensed font are committed. For faster previews, add `--dpi 100`. Default: 8-inch square pages, 1600 × 1600 PNGs (200 dpi). Source paintings are approximately 880 × 887 pixels; larger exports do not add artwork detail. The PDF embeds the source art and selectable vector text. It is not a printer-imposed or bleed-ready file.

## Downloads

GitHub Releases are the permanent book downloads; GitHub Packages is intended for software packages and is unnecessary here.

| File | Contents |
|---|---|
| `01-se-cayo.pdf` | Cover and 12 story pages |
| `01-se-cayo-pages.zip` | 13 numbered finished PNG pages and manifest |
| `01-se-cayo-illustrations.zip` | 12 numbered illustrations without text |
| `01-se-cayo-assets.zip` | Portable book folder: YAML, images, font/license, editorial notes |
| `manifest.json` | Page order, sentences and render settings |
| `SHA256SUMS.txt` | Download checksums |

PNG `00.png` is the cover; `01.png`–`12.png` are the stories. A cover followed by the first action page lets each action/fall pair face each other when printed as a normal book. Duplex booklet imposition is not included.

## Edit or add a book

Edit `books/01-se-cayo/book.yaml` to change sentences, order, image paths, font, size, baseline, or color. All image and font paths are relative to that YAML and must remain inside its folder. Use `schema_version: 1`, a lowercase hyphenated `id`, and a `version` such as `1.0.1`. Each page requires `image` and `text`; `cover` is optional. `page_size_inches` is 3–16, `dpi` is 72–600, `font_size_pt` is 12–80, and `text_baseline` is a fraction of page height measured from the bottom (0.05–0.17). The renderer rejects missing assets and overflowing text before writing output. Output must be outside the book source folder. Use an empty output folder on the first build. Subsequent builds require the ownership marker written by the renderer and reject symlinks; its generated `pages/` and `illustrations/` folders are replaced on rebuild.

Copy a book folder to start another book and pass its YAML to the same script. The initial workflow builds Book 1; add a job or matrix entry for another book when its assets are ready.

## GitHub Actions and releases

- Pull requests: tests, book build and downloadable Actions artifact (30 days).
- Pushes to `main` and **Run workflow**: same checks and artifacts; publish `book-01-v<version>` if that release does not exist.
- Existing releases remain unchanged. Increase `version` in the YAML to publish revised content. Every run still provides a fresh build artifact.
- Publication uses the built-in `GITHUB_TOKEN` with `contents: write`; no personal access token is required. Repository/organization policy must allow Actions and release writes.

```sh
uv run python -m unittest discover -s tests -v
```

## Editorial rules

Keep **cayó** as the familiar repeated word. Mostly two-syllable vocabulary, at most three for content words. Make the protagonist stand out through darker outlines, stronger colors and a quieter contrasting background. See [Book 1 manuscript and art notes](books/01-se-cayo/README.md) and [implementation decisions](docs/book-production-design.md).
