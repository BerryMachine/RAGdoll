import ollama
import chromadb
import pypdf
import re

cli = chromadb.PersistentClient(path="./.chroma")
collection = cli.get_or_create_collection(name="curricula")

# read_pdf() takes in a relative path to a pdf file to extract text per page via pypdf.
def read_pdf(path):
    pdf = pypdf.PdfReader(path)
    pages_data = []

    for i, page in enumerate(pdf.pages):
        content = page.extract_text()
        if content:
            pages_data.append({"text": content, "page": i+1})
    return pages_data

# chunk_text() takes a list of dictionaries in the format [{"text":str, "page":int}, ...]
#   and returns chunks of <500 characters of full sentences in the same format /\
#
# [{"text":str, "page":int}, ...]
#
# according to arXiv:2407.01219, 
# 512 token chunk size performed the best (1 token = ~4 char)
def chunk_text(pages_data, size=2048, overlap=256):
    sentence_data = []
    for page in pages_data:
        # Split text into sentences ending in ". ", "! ", "? "
        sentences = re.split(r'(?<=[.!?])\s+', page["text"].strip())
        for s in sentences:
            sentence_data.append((s.replace("\n", " "), page["page"]))

    chunks = []
    curr_chunk = []
    curr_size = 0
    overlap_chunk = []
    overlap_size = 0
    overlapping = False
    curr_start_page = 1
    curr_end_page = 1

    # Add sentences to chunk until filled up
    for sentence, page in sentence_data:
        sentence_size = len(sentence)

        # If sentence brings chunk over size limit; add to chunks and reset
        if (curr_size + sentence_size > size) and curr_chunk:
            chunks.append({
                "text": " ".join(curr_chunk),
                "page": f"{curr_start_page}-{curr_end_page}"
            })
            curr_chunk = overlap_chunk.copy()
            curr_chunk.append(sentence)
            curr_size = overlap_size + sentence_size
            curr_start_page = page
            curr_end_page = page

            overlapping = False
            overlap_chunk = []
            overlap_size = 0

        # Include sentence in next chunk (overlap).
        elif (curr_size + sentence_size >= size - overlap):
            curr_chunk.append(sentence)
            curr_size += sentence_size
            curr_end_page = page

            if not overlapping:
                overlapping = True
            else:
                overlap_chunk.append(sentence)
                overlap_size += sentence_size

        else: # Add to curr_chunk
            curr_chunk.append(sentence)
            curr_size += sentence_size
            curr_end_page = page
    
    if curr_chunk:
        chunks.append({
            "text": " ".join(curr_chunk),
            "page": f"{curr_start_page}-{curr_end_page}"})

    return chunks

# add_to_db() takes a list of chunks [{"text":str, "page":int}, ...] and info about the material
#   and adds it to chromadb.
def add_to_db(chunks, source_name, course):
    if not chunks: return

    ids = []
    embeddings = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        text = chunk["text"]
        page_label = chunk["page"]

        # Ollama to embed text 
        response = ollama.embeddings(model="bge-m3", prompt=text)

        ids.append(f"{source_name}_{i}")
        embeddings.append(response["embedding"])
        documents.append(text)
        metadatas.append({
            "source": source_name,
            "course": course,
            "page": page_label
        })

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )

if __name__ == "__main__":
    target_file = "docs/CS136_StyleGuide.pdf"
    source_name = "CS136_Style_Guide"
    course = "CS136"
    
    raw_text = read_pdf(target_file)
    text_chunks = chunk_text(raw_text)
    add_to_db(text_chunks, source_name, course)
    
    print(f"\nSuccessfully ingested {source_name} from {target_file} into 'curricula' collection.")