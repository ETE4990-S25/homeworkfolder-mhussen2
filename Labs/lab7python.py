import os
import hashlib

def menu():
    """Display a menu for user interaction."""
    while True:
        print("\n—— File Duplicate Finder ——")
        print("1. Enter directories to search")
        print("2. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            directories = input("Enter directories separated by commas: ").split(',')
            directories = [d.strip() for d in directories if os.path.isdir(d.strip())]

            if directories:
                duplicates = find_duplicates(directories)
                save_results(duplicates)
                print_results(duplicates)
            else:
                print("Invalid directories. Please try again.")
        elif choice == "2":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

def find_duplicates(directories):
    """Recursively searches for duplicate files using SHA-256 hashing."""
    checksum_dict = {}
    duplicates = {}

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_hash = get_checksum(file_path)

                    if file_hash in checksum_dict:
                        duplicates.setdefault(file_hash, []).append(file_path)
                    else:
                        checksum_dict[file_hash] = file_path
                except Exception as e:
                    print(f"Skipping {file_path}: {e}")

    return duplicates

def get_checksum(file_path):
    """Generate SHA-256 checksum for a file."""
    hash_obj = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        raise RuntimeError(f"Error reading file {file_path}: {e}")

def print_results(duplicates):
    """Print duplicate file paths to the console."""
    found = False
    print("\n—— Duplicate Files Found ——")
    for paths in duplicates.values():
        if len(paths) > 1:
            found = True
            print("\nDuplicate Group:")
            for path in paths:
                print(f" - {path}")
    if not found:
        print("No duplicate files found.")

def save_results(duplicates):
    """Save duplicate file paths to a text file."""
    with open("duplicate_files.txt", "w") as f:
        f.write("—— Duplicate Files Found ——\n")
        found = False
        for paths in duplicates.values():
            if len(paths) > 1:
                found = True
                f.write("\nDuplicate Group:\n")
                for path in paths:
                    f.write(f" - {path}\n")
        if not found:
            f.write("No duplicate files found.\n")
    
    print("\nResults saved to 'duplicate_files.txt'.")

if __name__ == "__main__":
    menu()
