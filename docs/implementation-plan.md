# First book implementation plan

Goal: ship the first approved animal book and a repeatable GitHub Actions build.
Spec: book-production-design.md and book-series-notes.md.

1. Create the six paired scenes with the approved contrast rule; split the art into twelve numbered text-free assets. Preserve the approved duck.
2. Write book.yaml, include a portable licensed font, and record the manuscript and letter coverage.
3. Implement scripts/build_book.py with config validation, selectable PDF text, matching PNG rendering, source and illustration bundles, manifest and checksums. Test page count, exact accents, missing assets, overflow and source/output overlap.
4. Build and inspect all pages. Check that the portable bundle can be rebuilt outside the repo's books folder.
5. Add the Actions workflow: test/build artifacts on PR, main and manual runs, versioned immutable-by-convention releases on main. Publish the first version and verify the run.

Execution: implement inline under the user's instruction to proceed. Use a separate final code review. Decisions: twelve story pages plus cover; 8-inch square pages; DejaVu Sans; F remains the tentative next consonant in Book 3. Future books are out of scope.
