import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions

load_dotenv()

def ingest_katalog():
    print("[ingest] Reading katalog.txt ...")
    
    katalog_path = Path(__file__).parent.parent / "data" / "katalog.txt"
    if not katalog_path.exists():
        print(f"[ingest] Error: {katalog_path} not found")
        sys.exit(1)
    
    with open(katalog_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    print(f"  File length: {len(content)} characters")
    
    chunk_size = 300
    overlap = 50
    chunks = []
    
    for i in range(0, len(content), chunk_size - overlap):
        chunk = content[i:i + chunk_size]
        if chunk.strip():
            chunks.append(chunk)
    
    print(f"  Split into {len(chunks)} chunks (size={chunk_size}, overlap={overlap})")
    
    print("[ingest] Setting up ChromaDB ...")
    
    chroma_db_path = Path(__file__).parent.parent / "chroma_db"
    client = chromadb.PersistentClient(path=str(chroma_db_path))
    
    # Use default embedding function (no internet needed)
    collection = client.get_or_create_collection(
        name="katalog_toko",
        metadata={"hnsw:space": "cosine"}
    )
    
    print("[ingest] Storing chunks into ChromaDB ...")
    
    for idx, chunk in enumerate(chunks, 1):
        try:
            collection.add(
                ids=[f"chunk_{idx}"],
                documents=[chunk],
                metadatas=[{"source": "katalog", "chunk_id": idx}]
            )
            print(f"  ✓ Chunk {idx}/{len(chunks)}")
        except Exception as e:
            print(f"  ✗ Error on chunk {idx}: {str(e)}")
    
    print(f"\n[ingest] ✅ Ingest complete! {len(chunks)} chunks stored in ./chroma_db")

if __name__ == "__main__":
    ingest_katalog()
