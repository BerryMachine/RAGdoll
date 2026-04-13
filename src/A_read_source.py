import config
import subprocess
import os
import re

#TODO: fix md reader

def pdf_to_md(path):
    output_dir = os.path.dirname(path)
    output_path = f"{output_dir}{os.path.basename(path).replace(".pdf", "")}"

    if os.path.exists(output_path):
        print(f"-> Using cached markdown: {output_path}")
        return output_path
    
    print()
    print(f"-> Converting {path} to markdown.")

    subprocess.run([
        "marker_single", path,
        "--output_dir", output_dir,
        "--paginate_output"
    ], check=True)

    print("--- SUCCESS ---")

    return output_path

def parse_paginated_md(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Marker's default pagination format is usually: \n\n{PAGE_NUMBER}\n------------------------------------------------\n\n
    # We use regex to split by this pattern
    page_splits = re.split(r'\n\n\d+\n-{10,}\n\n', content)
    
    pages_data = []
    for i, page_text in enumerate(page_splits):
        if page_text.strip():
            pages_data.append({
                "text": page_text,
                "page": i + 1
            })
            
    return pages_data

# TESTING
if __name__ == "__main__":
    path = "./docs/CS136_Makefile.pdf"
    pdf_to_md(path)