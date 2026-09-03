# Portfolio readiness fixes

## Fixed
- BM25 now indexes the full in-memory corpus instead of only the most recently uploaded PDF.
- BM25 supports removing deleted chunks.
- Graph entity/chunk state is cleaned when documents are removed.
- Graph construction is maintained during ingestion instead of being rebuilt on every query.
- Persisted Qdrant chunk payloads are restored into the in-memory registry, BM25 index, and concept graph on backend startup.
- Vector search now returns an empty result when no query is supplied or the Qdrant collection does not exist.
- Qdrant document deletion now uses an explicit point-ID selector.
- Added focused regression tests for multi-document BM25 behavior and graph cleanup.
- README wording was tightened: `Hit@5` now describes the implemented metric semantics, the broken screenshot reference was removed, and the placeholder live-demo link was made explicit.

## Verification
- Python `compileall` passed for the backend.
- Focused regression suite: 3 tests passed.

The full application/integration suite was not run in this environment because the repository's third-party runtime dependencies are not installed and external package installation is unavailable here.
