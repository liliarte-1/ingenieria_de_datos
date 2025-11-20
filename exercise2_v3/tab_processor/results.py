import os

INPUT_DIRECTORY = "./files/"
DOWNLOADED_DIRECTORY = f"{INPUT_DIRECTORY}songs"
CLEANED_DIRECTORY = f"{INPUT_DIRECTORY}cleaned"
OUTPUT_DIRECTORY_OK = f"{INPUT_DIRECTORY}validations/ok"
OUTPUT_DIRECTORY_KO = f"{INPUT_DIRECTORY}validations/ko"


def count_files(path):
    #recursive counting
    total = 0
    #we dont need the root or the dir, because we are only counting files
    for _, _, files in os.walk(path):
        total += len(files)
    return total


def main():
    print("RESULTS")
    songs = count_files(DOWNLOADED_DIRECTORY)
    cleaned = count_files(CLEANED_DIRECTORY)
    ok = count_files(OUTPUT_DIRECTORY_OK)
    ko = count_files(OUTPUT_DIRECTORY_KO)

    print(f"DOWNLOADED:{songs}")
    print(f"CLEANED:{cleaned}")
    print(f"VALIDATIONS/OK: {ok}")
    print(f"VALIDATIONS/KO: {ko}")

if __name__ == "__main__":
    main()
