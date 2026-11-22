"""Build the Netixsol Chroma index from source_documents.json."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from google import genai
from google.genai import types


WEEK4 = Path(__file__).resolve().parent
SOURCE_PATH = WEEK4 / "source_documents.json"
COLLECTION_NAME = "netixsol_public_knowledge"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a new index without overwriting an existing folder."
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional output folder, relative to the current working directory.",
    )
    args = parser.parse_args()

    load_dotenv(WEEK4 / ".env", override=True)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit(
            "GEMINI_API_KEY is missing. Configure week4/.env first."
        )

    output_path = (
        Path(args.output).resolve()
        if args.output
        else WEEK4 / "chroma_db"
    )

    if output_path.exists():
        raise SystemExit(
            f"Refusing to overwrite an existing folder: {output_path}\n"
            "Choose a new folder with --output."
        )

    source_bytes = SOURCE_PATH.read_bytes()
    source_documents = json.loads(source_bytes.decode("utf-8-sig"))

    if not isinstance(source_documents, list) or not source_documents:
        raise SystemExit(
            "source_documents.json must contain a non-empty list."
        )

    for document in source_documents:
        if not isinstance(document, dict):
            raise SystemExit("Each source document must be an object.")

        for field in ("url", "title", "text"):
            value = document.get(field)
            if not isinstance(value, str) or not value.strip():
                raise SystemExit(
                    f"Each source document needs a non-empty '{field}'."
                )

    model = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
    client = genai.Client(api_key=api_key)

    ids = []
    documents = []
    metadatas = []
    embeddings = []

    for document in source_documents:
        words = document["text"].split()

        for start in range(0, len(words), 350):
            chunk = " ".join(words[start:start + 400])

            for attempt in range(3):
                try:
                    response = client.models.embed_content(
                        model=model,
                        contents=[chunk],
                        config=types.EmbedContentConfig(
                            task_type="RETRIEVAL_DOCUMENT"
                        ),
                    )

                    if not response.embeddings:
                        raise RuntimeError("No embedding was returned.")

                    vector = response.embeddings[0].values
                    if not vector:
                        raise RuntimeError("An empty embedding was returned.")

                    break

                except Exception:
                    if attempt == 2:
                        raise
                    time.sleep(2 ** (attempt + 1))

            chunk_id = hashlib.sha256(
                f"{document['url']}|{start}|{chunk}".encode("utf-8")
            ).hexdigest()

            ids.append(chunk_id)
            documents.append(chunk)
            metadatas.append({
                "source": document["url"],
                "title": document["title"],
            })
            embeddings.append(vector)

            print(f"Embedded chunk {len(ids)}: {document['title']}")

            if start + 400 >= len(words):
                break

    if len(ids) != len(set(ids)):
        raise SystemExit(
            "Duplicate source chunks detected. Inspect the source file."
        )

    dimensions = {len(vector) for vector in embeddings}
    if len(dimensions) != 1:
        raise RuntimeError("Embedding dimensions are inconsistent.")

    database = chromadb.PersistentClient(path=str(output_path))
    collection = database.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    if collection.count() != len(ids):
        raise RuntimeError("Index count verification failed.")

    manifest = {
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "embedding_model": model,
        "embedding_dimensions": len(embeddings[0]),
        "embedding_task": "RETRIEVAL_DOCUMENT",
        "collection": COLLECTION_NAME,
        "chunk_count": collection.count(),
        "chunk_size_words": 400,
        "chunk_overlap_words": 50,
    }

    (output_path / "build_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    print(f"\nBUILD PASSED: {collection.count()} chunks")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Embedding model: {model}")
    print(f"Dimensions: {len(embeddings[0])}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()