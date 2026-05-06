from chatbot.knowledge import vectorstore


def retrieve_context(query, top_k=3):
    """Retrieve relevant knowledge base chunks for a query."""
    results = vectorstore.search(query, top_k=top_k)
    if not results:
        return None
    context = "\n\n".join(f"[Source: {r['source']}]\n{r['content']}" for r in results)
    return context


def build_rag_prompt(query, context):
    """Build a prompt that includes retrieved context."""
    return (
        "Answer the question based on the following context. "
        "If the context doesn't contain the answer, say you don't have that information.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\n"
        "Answer:"
    )
