import os
import sys
import logging as log
import subprocess

# --- Logging setup ---
LOGS_DIRECTORY = "./logs/"
os.makedirs(LOGS_DIRECTORY, exist_ok=True)

PIPELINE_LOG = os.path.join(LOGS_DIRECTORY, "pipeline.log")

log.basicConfig(
    filename=PIPELINE_LOG,
    filemode="w",
    encoding="utf-8",
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=log.INFO,
)

def run_script(script):
    try:
        log.info(f"Running {script}")
        subprocess.run([sys.executable, script], check=True)
        log.info(f"SUCCESS: {script}")
    except Exception as e:
        log.error(f"FAILED: {script} | Error: {e}")
        print(f"Pipeline failed executing {script}. Check pipeline.log")
        sys.exit(1)

def main():

    run_script("scrapper/main.py")
    run_script("tab_cleaner/main.py")
    run_script("tab_validator/main.py")
    run_script("results.py")
    run_script("lyrics.py")

    print("Pipeline finished successfully!")
    log.info("Pipeline finished successfully")

if __name__ == "__main__":
    main()
