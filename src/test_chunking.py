from ingest import read_pdf, chunk_text

def test_pdf_chunking():
    file_path = "./docs/CS136_StyleGuide.pdf"
    
    print(f"Reading {file_path}...")
    try:
        pages_data = read_pdf(file_path)
        print(f"Successfully read {len(pages_data)} pages.\n")
    except FileNotFoundError:
        print(f"Error: Could not find '{file_path}'. Please ensure the PDF is in the same directory.")
        return

    # for p in pages_data:
    #     print()
    #     print("-" * 60)
    #     print(f"{p["page"]}")
    #     print(f"{p["text"]}")

    print("Chunking text...")

    chunks = chunk_text(pages_data)
    print(f"Generated {len(chunks)} total chunks.\n")
    
    print("=" * 60)
    print("CHUNKING RESULTS")
    print("=" * 60)
    
    for i, chunk in enumerate(chunks):
        text = chunk["text"]
        page_label = chunk["page"]
        
        print(f"\n--- Chunk {i + 1} ---")
        print(f"Page(s) : {page_label}")
        print(f"Length  : {len(text)} characters")
        print("Text    :")
        print(f"{text}")
        print("-" * 60)

if __name__ == "__main__":
    test_pdf_chunking()