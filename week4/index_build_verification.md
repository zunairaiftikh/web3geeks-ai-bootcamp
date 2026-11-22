# Source-based index build verification

Date: 2026-11-21

Observed local checks:
- build_chroma.py passed Python syntax checking.
- The separate index contains 5 chunks.
- Collection: netixsol_public_knowledge
- Embedding model: gemini-embedding-001
- Embedding dimensions: 3072
- Document task: RETRIEVAL_DOCUMENT
- Sample metadata includes source and title.
- Source SHA-256: d44a8259d492b217acb71293940e8c378cc00ab7720a6e8d1b8b5efc3d90a935

The existing working index was not replaced.
This verifies index construction, not answer quality or fresh-clone setup.
Historical evaluation chunks differ from this source snapshot.
