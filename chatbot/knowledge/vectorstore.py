import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from django.conf import settings


_client = None
_collection = None


def _get_collection():
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=settings.KNOWLEDGE_BASE_DIR + "/.chromadb")
        embedding_fn = SentenceTransformerEmbeddingFunction(model_name=settings.EMBEDDING_MODEL)
        _collection = _client.get_or_create_collection(
            name="knowledge_base",
            embedding_function=embedding_fn,
        )
    return _collection


def add_documents(chunks, metadatas):
    """Add document chunks to the vector store."""
    collection = _get_collection()
    ids = [f"doc_{i}" for i in range(collection.count(), collection.count() + len(chunks))]
    collection.add(documents=chunks, metadatas=metadatas, ids=ids)
    return len(ids)


def search(query, top_k=3):
    """Search for relevant chunks."""
    collection = _get_collection()
    if collection.count() == 0:
        return []
    results = collection.query(query_texts=[query], n_results=min(top_k, collection.count()))
    docs = []
    for i, doc in enumerate(results["documents"][0]):
        docs.append({
            "content": doc,
            "source": results["metadatas"][0][i].get("source", ""),
            "distance": results["distances"][0][i] if results.get("distances") else None,
        })
    return docs


def reset():
    """Clear the entire knowledge base."""
    global _collection
    collection = _get_collection()
    _client.delete_collection("knowledge_base")
    _collection = None


def count():
    return _get_collection().count()
