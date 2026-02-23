import ollama
import chromadb

cli = chromadb.PersistentClient(path="./.chroma")
collection = cli.get_collection(name="curricula")

def get_context(query, course, n_results=3):
    response = ollama.embeddings(model="bge-m3", prompt=query)
    query_embedding = response["embedding"]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where={"course": course}
    )

    return results["documents"][0], results["metadatas"][0], results["distances"][0]

# TESTING
if __name__ == "__main__":
    query = "What should I comment for my structs?"
    course = "CS136"
    context_chunks, sources, dist = get_context(query, course)
    
    print(f"\n--- Top {len(context_chunks)} Relevant Chunks ---")
    for i, chunk in enumerate(context_chunks):
        print(f"\n[Source: {sources[i]["source"]}] [Page: {sources[i]["page"]}]")
        print(f"Distance: {dist[i]}")
        print(f"Content: {chunk[:200]}...") # Print first 200 chars