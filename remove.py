import os

def remove_files(extension_list):
    for root, dirs, files in os.walk('.'):
        for file in files:
            if any(file.endswith(ext) for ext in extension_list):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Removed: {file_path}")
                except Exception as e:
                    print(f"Error removing {file_path}: {e}")

if __name__ == "__main__":
    extensions_to_remove = ['.csv', '.png']
    remove_files(extensions_to_remove)
