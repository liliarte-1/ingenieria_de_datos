# Importamos las bibliotecas necesarias
import os
import re
import logging as log
import datetime
from utils.string_mapping import MAPPING

# -- Configuration ---
INPUT_DIRECTORY = "./files"
CATALOG_DIRECTORY = f"{INPUT_DIRECTORY}/catalogs/"
LOGS_DIRECTORY = "./logs/"

OUTPUT_DIRECTORY = f"{INPUT_DIRECTORY}/cleaned/"
ROOT = "https://acordes.lacuerda.net"
URL_ARTIST_INDEX = "https://acordes.lacuerda.net/tabs/"
MIN_LINES = 5
SONG_VERSION = 0
INDEX = "abcdefghijklmnopqrstuvwxyz#"


# === LOGGING ===
os.makedirs(LOGS_DIRECTORY, exist_ok=True)

logger = log.getLogger(__name__)
log.basicConfig(
    filename=os.path.join(LOGS_DIRECTORY, "cleaner.log"),
    filemode="w",
    encoding="utf-8",
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=log.INFO,
)


# original code
# # === FUNCIONES ===
# def list_files_recursive(path="."):
#     if not os.path.exists(path):
#         raise FileNotFoundError(f"La carpeta no existe: {path}")

#     for entry in os.listdir(path):
#         full_path = os.path.join(path, entry)
#         if os.path.isdir(full_path):
#             list_files_recursive(full_path)
#         else:
#             dir_list.append(full_path)

#     return [dir.replace("\\", "/") for dir in dir_list]


dir_list = list()
#this function is used to list every file using recursive algorithm
def list_files_recursive(path=INPUT_DIRECTORY):
    print(INPUT_DIRECTORY)
    if not os.path.exists(path):
        raise FileNotFoundError(f"La carpeta no existe: {path}")
    
    #prints are for debugging
    for entry in os.listdir(path):
        print(entry)
        full_path = os.path.join(path, entry)
        print(full_path)

        # avoid avoiding the catalog we improve the execution time because we dont process the catalog, we do not need the catalog after extracting the songs.
        # avoiding cleaned is used to avoid saving cleaned songs inside de cleaned folder more than once.
        if entry in ("catalogs", "cleaned"):
            print("IGNORA ESTAS CARPETAS")
            print(full_path)
            continue

        #this is the logic to go inside the folders until the last one. example cleaned/songs/abelpintos/**3** <- until there
        if os.path.isdir(full_path):
            list_files_recursive(full_path)
        else:
            dir_list.append(full_path)

    # return routes with / por if Windows
    return [p.replace("\\", "/") for p in dir_list]



def remove_email_sentences(text: str):
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    sentence_pattern = r"[\n^.!?]*" + email_pattern + r"[^.!?]*[.!?\n]"
    return re.sub(sentence_pattern, "", text)


def apply_format_rules(text: str):
    formatted_text = remove_email_sentences(text)
    for key, value in MAPPING.items():
        formatted_text = re.sub(
            key, value, formatted_text, flags=re.DOTALL | re.IGNORECASE
        )
    return formatted_text


def main():
    start_time = datetime.datetime.now()
    log.info(f"Cleaner started at {start_time}")
    print("Starting cleaner...")

    # Crear las carpetas necesarias
    os.makedirs(INPUT_DIRECTORY, exist_ok=True)
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

    cleaned = 0

    for file_path in list_files_recursive(INPUT_DIRECTORY):
        log.info(f"Processing file -> {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
        except Exception as e:
            print(file_path, "---> ", e)
            continue

        if text.count("\n") < MIN_LINES:
            log.info("Empty or too small tab. Skipping...")
            continue

        formatted_text = apply_format_rules(text)

        output_file = file_path.replace(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
        dir_path = os.path.dirname(output_file)
        os.makedirs(dir_path, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(formatted_text)

        cleaned += 1
        print(f"{cleaned} -- {output_file} CREATED!!")

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    log.info(f"Cleaner ended at {end_time}")
    log.info(f"Total duration: {duration}")
    print(
        f"Cleaner finished. Duration in seconds: {duration.total_seconds():.2f} "
        f"({duration.total_seconds() / 60:.2f} minutes)."
    )


if __name__ == "__main__":
    main()
