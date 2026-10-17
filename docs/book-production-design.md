# Book 1 production design

Approved direction: six animals, two pages per story, short Spanish sentences, repeated **se cayó**, and strong protagonist/background separation. The user authorized implementation and GitHub Actions delivery on 2026-10-16.

## Content and art

Pato, gato, mono, vaca, llama and oso. Alternate an action with a gentle fall. All animal names use the initial letter set. Two-syllable action words saltó and bailó repeat; caminó has three syllables. D is deliberately reserved for Book 2. Speaking a word is not recorded as reading mastery.

Use the approved duck with blue/purple/pink flowers as the style reference. Warm saturated characters, dark loose outlines, textured watercolor/crayon, soft cool backgrounds and blank bottom text space. Preserve character identity within each pair. Each asset is text-free. Artwork was generated as paired scenes and the panels separated for the requested individual illustration files; no generative alterations occur during the build.

## Renderer

`books/01-se-cayo/book.yaml` is the content source. A portable font and license live beside it. `scripts/build_book.py` validates the config, creates a ReportLab PDF with embedded TrueType text, and renders that PDF to PNG with PyMuPDF. This gives identical layout and accents in both formats. Default page: 8 inches square, text 32 pt, PNG 200 dpi. Cover is followed by twelve story pages.

Deliver PDF, rendered-page ZIP, text-free illustration ZIP and source-asset ZIP. Include manifest and checksums. Preserve source images at their generated resolution; do not imply that enlarged PNGs contain more illustration detail.

## Automation

GitHub Releases fit downloadable books better than GitHub Packages. Every PR/main/manual run tests and renders the book, retaining Actions downloads for 30 days. Successful main builds publish a versioned release if absent. `book.yaml` version controls release naming. Do not overwrite an existing release; bump the version for revised content. Use the workflow token, no personal token or paid image generation in CI.

## Verification

Check PDF page count, exact accented sentences and six occurrences of se cayó. Check PNG counts and archive contents, missing asset behavior, source/output separation and overflow. Visually inspect a contact sheet and full-size duck pages. Observe Actions to verify publication, and report any access/policy failure honestly.
