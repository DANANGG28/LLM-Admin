import chromadb
from pathlib import Path

def search_knowledge_base(query: str, n_results: int = 3) -> str:
    """Search ChromaDB for relevant chunks"""
    try:
        chroma_db_path = Path(__file__).parent.parent / "chroma_db"
        client = chromadb.PersistentClient(path=str(chroma_db_path))
        
        collection = client.get_collection(name="katalog_toko")
        
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        if not results or not results['documents'] or len(results['documents'][0]) == 0:
            return "Informasi tidak tersedia"
        
        # Combine results
        combined = "\n---\n".join(results['documents'][0])
        return combined
        
    except Exception as e:
        print(f"[retriever] Error searching knowledge base: {str(e)}")
        return "Informasi tidak tersedia"

if __name__ == "__main__":
    result = search_knowledge_base("cara pemesanan")
    print("=== Query: cara pemesanan ===")
    print(result)
    
    print("\n" + "="*50 + "\n")
    
    result2 = search_knowledge_base("minimum order lusin")
    print("=== Query: minimum order lusin ===")
    print(result2)
