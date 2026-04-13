import ollama
from C_query import get_context

model = "deepseek-r1:1.5b"

def prompt_engineering(user_input: str, course: str):
    print("1. Querying...")

    context_chunks, metadatas, dists = get_context(user_input, course)

    print("--- SUCCESS 1 ---")
    print()
    print("2. Prompt Augmentation...")
    
    formatted_context_list = []
    for i in range(len(context_chunks)):
        block = f"SOURCE: {metadatas[i]['source']}\nPAGE: {metadatas[i]['page']}\nCONTENT: {context_chunks[i]}"
        formatted_context_list.append(block)
    
    context_text = "\n\n---\n\n".join(formatted_context_list)
    print(context_text)
    print()

    # DEBUGGING
    print(f"\n--- Top {len(context_chunks)} Relevant Chunks ---")
    for i, chunk in enumerate(context_chunks):
        print(f"\n[Source: {metadatas[i]["source"]}] [Page: {metadatas[i]["page"]}]")
        print(f"Distance: {dists[i]}")
        print(f"Content: {chunk[:200]}...") # Print first 200 chars

    system_prompt = f"""
    You are a helpful academic assistant for a student at the University of Waterloo.
    Use the following pieces of retrieved context from the student's course materials to answer the question.
    
    Rules:
    - If the answer isn't in the context, say you don't know based on the notes.
    - Be concise! Speak English unless asked otherwise.
    - Use LaTeX for any mathematical formulas.
    - ALWAYS cite which document the information came from and which pages.
    
    Context:
    {context_text}
    """

    print("--- SUCCESS 2 ---")
    print()
    print(f"3. Generating Response... ({model})")

    # We use stream=True for that cool "typing" effect
    response = ollama.generate(
        model=model, # Or 1.5b/7b if 8GB RAM is struggling
        system=system_prompt,
        prompt=user_input,
        stream=True
    )

    for chunk in response:
        print(chunk['response'], end='', flush=True)


if __name__ == "__main__":
    query = input("Ask RAGdoll a question about your notes: ")
    course = input("What course is this for?: ")
    prompt_engineering(query, course)