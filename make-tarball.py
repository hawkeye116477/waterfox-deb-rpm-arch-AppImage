import os
import sys
import time
import math
import argparse
import tarfile
from git import Repo, InvalidGitRepositoryError, GitCommandError
from tqdm import tqdm
from multiprocessing import Process, Queue
import tempfile

# Import the pigz binding
try:
    import pigz
except ImportError:
    print("Error: The 'pigz' Python binding is not installed.")
    print("Please install it using: pip install pigz")
    print("If you intend to use system pigz, you'll need to revert to subprocess calls.")
    sys.exit(1)


# --- Helper Functions ---

def human_readable_size(size_bytes):
    """Converts a byte count to a human-readable string (KB, MB, GB)."""
    if size_bytes <= 0:
        return "0KB"
    if size_bytes < 1024 and size_bytes > 0:
        return "<1KB"

    units = ("KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s}{units[i]}"

def get_repo_tracked_files_and_size(repo_path):
    """
    Uses GitPython to get all tracked files (including submodules) and their total size.
    Returns a tuple: (list of file paths relative to repo root, total bytes, number of files).
    """
    total_uncompressed_file_bytes = 0
    file_paths = []

    try:
        repo = Repo(repo_path)
    except InvalidGitRepositoryError:
        print(f"Error: '{repo_path}' is not a valid Git repository.")
        return [], 0, 0

    # This relies on submodules already being checked out
    # in the working directory for 'git ls-files --recurse-submodules' to find their contents.
    # If submodules are not initialized/checked out, their files will NOT be archived.

    # Get tracked files using git ls-files via GitPython
    try:
        ls_files_output = repo.git.ls_files('--recurse-submodules').splitlines()

        for rel_path in ls_files_output:
            full_path = os.path.join(repo_path, rel_path)
            if os.path.exists(full_path) and os.path.isfile(full_path):
                file_paths.append(rel_path)
                try:
                    total_uncompressed_file_bytes += os.path.getsize(full_path)
                except OSError as e:
                    print(f"Warning: Could not get size of '{full_path}': {e}. Skipping size for this file.")

        number_of_files = len(file_paths)
        return file_paths, total_uncompressed_file_bytes, number_of_files

    except GitCommandError as e:
        print(f"Error listing files with GitPython: {e}. Cannot determine files to archive.")
        return [], 0, 0
    except Exception as e:
        print(f"An unexpected error occurred during file listing: {e}")
        return [], 0, 0

# --- Function for compression (to be run in a separate process) ---
def compress_worker(input_tar_path, output_compressed_path, compressor_type, queue):
    """Worker function to read, compress, and write data using the specified compressor."""
    chunk_size = 65536 # 64KB chunks

    try:
        with open(input_tar_path, 'rb') as f_in, open(output_compressed_path, 'wb') as f_out:
            compressor_writer = None
            if compressor_type == "pigz":
                # Use pigz.open for parallel gzip compression
                # The 'compresslevel' argument maps to pigz's -1 to -9 levels
                # The 'threads' argument can control concurrency (defaults to # of cores)
                compressor_writer = pigz.open(fileobj=f_out, mode='wb', compresslevel=6, threads=0)
                # threads=0 means use default (all available cores)
            elif compressor_type == "xz":
                # Still use Python's native lzma for xz
                import lzma # Import locally just in case xz is not used
                compressor_writer = lzma.open(f_out, mode='wb', preset=6)
            elif compressor_type == "gzip":
                # Fallback to standard gzip if pigz not chosen or not preferred
                import gzip # Import locally just in case gzip is not used
                compressor_writer = gzip.GzipFile(fileobj=f_out, mode='wb', compresslevel=6)
            else:
                raise ValueError(f"Unsupported compressor type: {compressor_type}")

            while True:
                chunk = f_in.read(chunk_size)
                if not chunk:
                    break
                compressor_writer.write(chunk)
                queue.put(len(chunk)) # Send progress update to main process

            compressor_writer.close()
            queue.put(None) # Signal completion
    except Exception as e:
        queue.put(f"ERROR:{e}") # Send error message
    finally:
        if 'compressor_writer' in locals() and compressor_writer is not None:
            # Ensure proper closure if an error occurs mid-compression
            # pigz.open and lzma.open handle this via context manager, but good to be safe
            try:
                compressor_writer.close()
            except Exception:
                pass


# --- Main Script ---

def main():
    parser = argparse.ArgumentParser(
        description="Archives a Git repository with optional compression, using pure Python and multiprocessing.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "appname",
        help="The name of the application to archive."
    )
    parser.add_argument(
        "-c", "--compression",
        choices=["xz", "pigz", "gzip"], # Added pigz as a direct choice
        help="Specify the compression method (xz, pigz, gzip).\n"
             "Default: pigz (falls back to gzip if pigz binding fails or not chosen)."
    )
    args = parser.parse_args()

    appname = args.appname
    desired_compression_method = args.compression

    start_time_overall = time.time()

    # Determine script's directory and navigate there
    script_dir = os.path.dirname(os.path.realpath(__file__))
    try:
        os.chdir(script_dir)
        print(f"Changed current directory to: {os.getcwd()}")
    except OSError as e:
        print(f"Error: Could not change directory to {script_dir}. Exiting.")
        sys.exit(1)

    source_dir_relative = "../Waterfox"
    source_path_abs = os.path.abspath(source_dir_relative)

    # Initialize GitPython Repo object
    try:
        repo = Repo(source_path_abs)
        print(f"Successfully loaded Git repository at: {source_path_abs}")
    except InvalidGitRepositoryError:
        print(f"Error: '{source_path_abs}' is not a valid Git repository. Exiting.")
        sys.exit(1)

    # Get Git version tag using GitPython
    try:
        version = repo.git.describe("--tags", "--exact-match", "--always").strip()
        if not repo.tags:
             version = "unknown"
        else:
            try:
                version = repo.git.describe("--tags", "--exact-match").strip()
            except GitCommandError:
                version = "unknown"

    except GitCommandError as e:
        print(f"Warning: Could not get Git version tag using describe: {e}. Defaulting to 'unknown'.")
        version = "unknown"
    print(f"Git Version: {version}")

    # --- Determine compressor settings ---
    compressor_type = ""
    output_extension = ""

    # Preference: pigz (if chosen) -> xz (if chosen) -> gzip (default)
    if desired_compression_method == "pigz":
        compressor_type = "pigz"
        output_extension = ".tar.gz" # pigz outputs .gz files
        print("Using pigz for parallel compression (Python binding) as requested.")
    elif desired_compression_method == "xz":
        compressor_type = "xz"
        output_extension = ".tar.xz"
        print("Using xz compression (Python's lzma module) as requested.")
    else: # Default if no valid method specified or chosen method was not pigz/xz
        compressor_type = "gzip"
        output_extension = ".tar.gz"
        print("Using gzip compression (Python's gzip module) by default.")

    # Construct the full output filename
    output_filename = os.path.join(script_dir, f"{appname}-{version}{output_extension}")
    archive_internal_dir = os.path.basename(f"{appname}-{version}")

    print(f"Archiving current repository to '{output_filename}' with internal root '{archive_internal_dir}/'...")

    # --- Get file list and calculate estimated sizes ---
    file_paths_to_archive, total_uncompressed_file_bytes, number_of_files = \
        get_repo_tracked_files_and_size(source_path_abs)

    if not file_paths_to_archive:
        print("Info: No files found to archive. Creating an empty archive.")
        total_uncompressed_file_bytes = 0
        number_of_files = 0

    uncompressed_display_size = human_readable_size(total_uncompressed_file_bytes)

    estimated_compressed_bytes = 0
    if total_uncompressed_file_bytes > 0:
        if compressor_type == "xz":
            estimated_compressed_bytes = int(total_uncompressed_file_bytes / 5.5)
        elif compressor_type == "pigz" or compressor_type == "gzip": # pigz and gzip have similar ratios
            estimated_compressed_bytes = int(total_uncompressed_file_bytes * 2 / 7)

    if estimated_compressed_bytes <= 0 and total_uncompressed_file_bytes > 0:
        estimated_compressed_bytes = 1

    estimated_compressed_display_size = human_readable_size(estimated_compressed_bytes) if estimated_compressed_bytes > 0 else "N/A"

    print(f"Estimated total uncompressed content size (files only): {uncompressed_display_size}")
    print(f"Estimated compressed size (approx. ratio for {compressor_type} at optimal level): {estimated_compressed_display_size}")

    # --- Archiving and Compression Pipeline (Pure Python with multiprocessing for compression) ---
    pipeline_start_time = time.time()

    temp_tar_path = None # To store uncompressed tar before compression

    try:
        # Step 1: Create the .tar archive using tarfile module (in main process)
        with tempfile.NamedTemporaryFile(suffix=".tar", delete=False) as temp_tar_file:
            temp_tar_path = temp_tar_file.name
            with tarfile.open(fileobj=temp_tar_file, mode="w") as tar:
                with tqdm(total=number_of_files, unit="file", desc="Adding files to tar") as pbar_tar:
                    for file_rel_path in file_paths_to_archive:
                        full_path = os.path.join(source_path_abs, file_rel_path)
                        arcname = os.path.join(archive_internal_dir, file_rel_path) # Path inside archive

                        try:
                            tar.add(full_path, arcname=arcname, recursive=False)
                        except FileNotFoundError:
                            pbar_tar.write(f"Warning: File not found during tar.add: {full_path}. Skipping.")
                        except Exception as e:
                            pbar_tar.write(f"Warning: Error adding {full_path} to tar: {e}. Skipping.")
                        pbar_tar.update(1)

        # Step 2: Offload compression to a separate process
        actual_tar_size = os.path.getsize(temp_tar_path)
        print(f"Actual uncompressed .tar size: {human_readable_size(actual_tar_size)}")

        progress_queue = Queue() # Queue to receive progress updates from worker

        compress_process = Process(
            target=compress_worker,
            args=(temp_tar_path, output_filename, compressor_type, progress_queue)
        )
        compress_process.start()

        # Step 3: Display compression progress in main process using tqdm
        with tqdm(total=actual_tar_size, unit="B", unit_scale=True, unit_divisor=1024,
                  desc="Compressing data") as pbar_compress:
            while True:
                update = progress_queue.get()
                if update is None: # Worker signaled completion
                    break
                elif isinstance(update, str) and update.startswith("ERROR:"):
                    raise RuntimeError(f"Compression worker error: {update[6:]}")
                else: # Received chunk size
                    pbar_compress.update(update)

        compress_process.join() # Wait for the compression process to finish

        if compress_process.exitcode != 0:
            raise RuntimeError(f"Compression process exited with code {compress_process.exitcode}")

        # Check final output file size
        if os.path.exists(output_filename):
            actual_compressed_size = os.path.getsize(output_filename)
            print("Archiving complete!")
            print(f"Actual compressed size: {human_readable_size(actual_compressed_size)}")
        else:
            print("Error: Output file was not created or is empty.")
            sys.exit(1)

    except Exception as e:
        print(f"\nAn error occurred during archiving/compression: {e}")
        sys.exit(1)
    finally:
        if temp_tar_path and os.path.exists(temp_tar_path):
            os.remove(temp_tar_path) # Clean up temporary uncompressed tar

    # End timer for the archiving pipeline and display total elapsed time
    pipeline_end_time = time.time()
    elapsed_pipeline_time = int(pipeline_end_time - pipeline_start_time)
    print(f"Archiving pipeline time: {elapsed_pipeline_time} seconds.")

    # Optional: Display overall script execution time
    elapsed_overall_time = int(time.time() - start_time_overall)
    print(f"Total script execution time: {elapsed_overall_time} seconds.")

if __name__ == "__main__":
    main()
