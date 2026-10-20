from pathlib import Path


def list_directory(target_path="."):
    
    p = Path(target_path).resolve()

    if not p.exists():
        return {"error": f"Path '{target_path}' does not exist"}

    if not p.is_dir():
        return {"error": f"Path '{target_path}' is not a directory"}

    items = []
    for item in p.iterdir():
        items.append({
            "name": item.name,
            "is_directory": item.is_dir(),
            "size_kb": round(item.stat().st_size / 1024, 2) if item.is_file() else None
        })

    return {"directory": str(p), "contents": items}


def search_files(keyword, start_path="."):
    
    p = Path(start_path).resolve()
    
    if not p.exists():
        return {"error": f"Directory '{start_path}' does not exist"}

   
    matched = list(p.rglob(f"*{keyword}*"))
    return {
        "query": keyword,
        "count": len(matched),
        "results": [str(m) for m in matched[:20]]
    }


def read_file_content(file_path):
    
    p = Path(file_path).resolve()

    if not p.exists():
        return {"error": "File does not exist"}

    if not p.is_file():
        return {"error": "Given path is a directory, not a file"}

    try:
        content = p.read_text(encoding="utf-8")
        return {"file": p.name, "content": content}
    except Exception as e:
        return {"error": f"Failed to read file: {str(e)}"}


def write_file_content(file_path, content):
    p = Path(file_path).resolve()
    try:
        
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return {"status": "success", "file": str(p)}
    except Exception as e:
        return {"error": f"Failed to write file: {str(e)}"}


# --- Quick Self-Test ---
if __name__ == "__main__":
    import pprint

    print("--- 1. Testing Directory Listing (Current Folder) ---")
    pprint.pprint(list_directory("."))

    print("\n--- 2. Testing Search for Python Files ---")
    pprint.pprint(search_files(".py", "."))
