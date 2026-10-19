# Release integrity

Official releases are **git tags** on [MHaghighian/MLSecOps](https://github.com/MHaghighian/MLSecOps) published as [GitHub Releases](https://github.com/MHaghighian/MLSecOps/releases). Pre-built PDF/DOCX are not attached; the release artifact is the tagged source tree (and GitHub’s automatic source archive).

## What we publish

For each official release (from the Create Release workflow / [RELEASING.md](RELEASING.md)):

| Asset | Purpose |
|-------|---------|
| Git tag (e.g. `v1.2.1`) | Immutable pointer to the release commit |
| `SHA256SUMS` | Cryptographic hashes of release-relevant paths |
| `SHA256SUMS.sigstore.json` or `.asc` | Cosign keyless bundle or maintainer GPG detached signature over `SHA256SUMS` |

## Verify a release

1. Open the [GitHub Release](https://github.com/MHaghighian/MLSecOps/releases) for the tag and confirm the publisher account.  
2. Download `SHA256SUMS` and the signature file from that release (when attached).  
3. Check out the tag and verify hashes:

```bash
git fetch --tags
git checkout v1.2.1
python scripts/generate_release_manifest.py --verify SHA256SUMS
```

4. Verify the signature (cosign keyless bundle from the Create Release workflow):

```bash
cosign verify-blob --bundle SHA256SUMS.sigstore.json SHA256SUMS
```

Or with GPG, if a `.asc` detached signature was published:

```bash
gpg --verify SHA256SUMS.asc SHA256SUMS
```

If a historical release has no `SHA256SUMS` yet, trust the **annotated tag** and commit SHA shown on the Release page; new releases follow this process.
