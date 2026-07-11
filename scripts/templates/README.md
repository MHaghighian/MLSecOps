# DOCX reference template

Pandoc uses `reference.docx` only for **Word styles** (headings, body text, tables, captions).

## Default behaviour

`scripts/build-docx.py` looks for a template in this order:

1. `--reference` CLI argument
2. `MLSECOPS_REFERENCE_DOCX` environment variable
3. `scripts/templates/reference.docx` (this folder)
4. Legacy workspace files (`MLSecOps-Guide-v0.1.pre-v0.1.2-backup.docx`, etc.)
5. **Auto-download** from the [v1.0.0 GitHub Release DOCX](https://github.com/l4tr0d3ctism/MLSecOps/releases/download/v1.0.0/MLSecOps-Practical-Reference-Guide-v1.0.0.docx) on first run

## Use your own template

Copy your styled Word file here as `reference.docx`, or pass `--reference path/to/file.docx`.

To create a minimal style-only template from an existing guide export:

```bash
pandoc -o reference.docx --print-default-data-file reference.docx
# then paste styles from your guide into that file in Word, or use a prior release DOCX as-is
```

`reference.docx` is gitignored (large binary). Keep your canonical styled export in the workspace or download from Releases.
