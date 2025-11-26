import os
import site

def find_string_in_dir(directory, search_string):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        if search_string in f.read():
                            print(f"Found in: {path}")
                except Exception:
                    pass

# Hardcoded path based on previous output
site_packages = r"C:\Users\Dell\AppData\Local\Programs\Python\Python313\Lib\site-packages"
print(f"Searching in {site_packages}...")
# Search in langchain folders
for lib in ["langchain", "langchain_community", "langchain_core"]:
    path = os.path.join(site_packages, lib)
    if os.path.exists(path):
        print(f"Scanning {lib}...")
        find_string_in_dir(path, "def create_retrieval_chain")
