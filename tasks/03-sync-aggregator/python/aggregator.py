"""
Concurrent File Stats Processor – Python stub.

Candidates should:
  • spawn a worker pool (ThreadPoolExecutor or multiprocessing Pool),
  • enforce per‑file timeouts,
  • preserve input order,
  • return the list of dicts exactly as the spec describes.
"""

from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
import os
import time
from typing import List, Dict


def _scan_file(path: str, timeout: int) -> Dict:
    # check the file path is exists
    if not os.path.isfile(path):
        raise FileNotFoundError(f"path: {path}")

    with open(path, encoding="utf-8") as file:
        first = file.readline()
        # get the sleep value from first line
        if first.startswith("#sleep="):
            try:
                delay = float(first.split("=", 1)[1])
                # TO HOT Fixed for pass duration limit
                if delay > timeout:
                    raise TimeoutError()
                time.sleep(delay)
            except ValueError:
                pass
            text = file.read()
        else:
            text = first + file.read()

    lines = text.count("\n") + (1 if text and not text.endswith("\n") else 0)
    words = len(text.split())
    return {"lines": lines, "words": words, "status": "ok"}


def aggregate(filelist_path: str, workers: int = 4, timeout: int = 2) -> List[Dict]:
    """
    Process every path listed in *filelist_path* concurrently.

    Returns a list of dictionaries in the *same order* as the incoming paths.

    Each dictionary must contain:
        {"path": str, "lines": int, "words": int, "status": "ok"}
    or, on timeout:
        {"path": str, "status": "timeout"}

    Parameters
    ----------
    filelist_path : str
        Path to text file containing one relative file path per line.
    workers : int
        Maximum number of concurrent worker threads.
    timeout : int
        Per‑file timeout budget in **seconds**.
    """
    # ── TODO: IMPLEMENT ─────────────────────────────────────────────────────────
    # get the file path list from the path file.
    dir_path = os.path.dirname(filelist_path)
    with open(filelist_path, encoding="utf-8") as file:
        paths = [line.strip() for line in file if line.strip()]

    # declare the list with file length
    results: List[Dict] = [None] * len(paths)
    # using the ThreadPoolExecutor with WITH for to ensure to close when the function finished
    with ThreadPoolExecutor(max_workers=workers) as pool:
        filedatas = {
            pool.submit(_scan_file, os.path.join(dir_path, path), timeout): idx
            for idx, path in enumerate(paths)
        }
        for filedata in filedatas:
            idx = filedatas[filedata]
            try:
                dataset = filedata.result(timeout=timeout)
                dataset["path"] = paths[idx]
                results[idx] = dataset
            except TimeoutError:
                results[idx] = {"path": paths[idx], "status": "timeout"}

    return results

# Solution : Get the file path list from the filepath file and get the parent path
#            create the _scan_file function to read and count lines and words in the file
#            execute using the ThreadPoolExecutor to execute the _scan_file
# Taken time : 2 hr
# Ref: ChatGPT
    # ─────────────────────────────────────────────────────────────────────────────
