import os
import json
import subprocess

# Configuration based on your GitHub URL
FONTS_DIR = "fonts"
CATALOG_FILE = "catalog.json"
BASE_URL = "https://raw.githubusercontent.com/voidlabsdev/PopularFonts/main/fonts/"

def update_catalog():
    print("Loading existing catalog...")
    
    # 1. Read the fonts you ALREADY have (Gemunu Libre, Teko, etc.)
    existing_catalog = []
    if os.path.exists(CATALOG_FILE):
        try:
            with open(CATALOG_FILE, "r", encoding="utf-8") as f:
                existing_catalog = json.load(f)
        except Exception as e:
            print(f"Note: Could not read existing catalog ({e}).")

    # Use a dictionary to prevent duplicate entries if a font is in both places
    catalog_dict = {item["name"]: item for item in existing_catalog}
    
    # 2. Scan the local fonts folder for the new ZIPs
    if os.path.exists(FONTS_DIR):
        print(f"Scanning '{FONTS_DIR}' for new font bundles...")
        for filename in sorted(os.listdir(FONTS_DIR)):
            if filename.endswith(".zip"):
                display_name = filename.replace(".zip", "").replace("_", " ")
                file_url = f"{BASE_URL}{filename}"
                
                # Add the new font (or update it if it somehow changed)
                catalog_dict[display_name] = {
                    "name": display_name,
                    "url": file_url
                }
    else:
        print(f"Note: '{FONTS_DIR}' directory not found locally. Only preserving existing fonts.")

    # 3. Sort the combined list alphabetically so it looks clean
    final_catalog = sorted(list(catalog_dict.values()), key=lambda x: x["name"])

    # 4. Save everything back to catalog.json
    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        json.dump(final_catalog, f, indent=2)
        
    print(f"Success! '{CATALOG_FILE}' safely merged. It now contains {len(final_catalog)} total fonts.")
    return True

def push_to_github():
    print("\nPreparing to upload to GitHub...")
    try:
        # Run standard Git commands directly from Python
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-merge 100 new fonts into catalog"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        print("\nSuccess! All fonts and your merged catalog.json are live on GitHub.")
    except Exception as e:
        print(f"\nGit automation failed: {e}")
        print("You can still upload them manually using GitHub Desktop or your terminal.")

if __name__ == "__main__":
    success = update_catalog()
    if success:
        push_to_github()