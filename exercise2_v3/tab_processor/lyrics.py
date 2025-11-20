# lyrics.py
import os
import re

# Base directory containing the validated OK files
INPUT_DIRECTORY = "./files/"
OK_DIRECTORY = f"{INPUT_DIRECTORY}validations/ok"


def list_files_recursive(path: str):

    # Recursively list all files inside a directory.
    # Normalizes Windows paths to use '/'.

    files = []
    for root, _, file_names in os.walk(path):
        for name in file_names:
            full_path = os.path.join(root, name)
            files.append(full_path.replace("\\", "/"))  # Normalize path separators
    return files


def remove_chords(text: str) -> str:

    # Removes chord lines using a very simple heuristic:
    # - If a line contains at least one lowercase letter → treat it as lyrics.
    # - If a line has NO lowercase letters → assume it's a chord line and remove it.

    lyric_lines = []

    for line in text.splitlines():
        # Keep only lines that contain lowercase letters (lyrics)
        if re.search(r"[a-záéíóúñü]", line):
            lyric_lines.append(line)

    return "\n".join(lyric_lines) + "\n"


def main():
    print("Starting lyrics processor...\n")

    files = list_files_recursive(OK_DIRECTORY)
    processed = 0

    for file_path in files:
        # Read original validated file
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except Exception as e:
            print(f"[ERROR] Could not read {file_path}: {e}")
            continue

        # Remove chords (simple heuristic)
        lyrics_only = remove_chords(text)

        # Save the lyrics version next to the original file
        root, ext = os.path.splitext(file_path)
        output_path = root + "_lyrics" + ext

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(lyrics_only)
            processed += 1
            print(f"{processed} -- {output_path} CREATED")
        except Exception as e:
            print(f"[ERROR] Could not write {output_path}: {e}")
            continue

    print(f"\nLyrics processor finished. Total processed: {processed}")


if __name__ == "__main__":
    main()
