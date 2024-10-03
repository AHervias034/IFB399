import json
import multiprocessing
import os

from tqdm import tqdm

def find_title_for_asin(file_path, target_asin, start_line, end_line):
    """Find the title of a product with the specified parent_asin in a specific range of lines."""
    titles = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for _ in range(start_line):
            next(f)  # Skip to the start line

        for line_number in range(start_line, end_line):
            line = f.readline()
            if not line:
                break  # End of file

            item = json.loads(line.strip())
            if item.get('parent_asin') == target_asin:
                titles.append(item.get('title', 'Title not found'))

    return titles

def find_titles_in_parallel(file_path, target_asin, num_processes):
    """Divide the file reading into multiple processes."""
    with open(file_path, 'r', encoding='utf-8') as f:
        total_lines = sum(1 for _ in f)  # Count total lines in the file

    # Define line ranges for each process
    chunk_size = total_lines // num_processes
    processes = []
    results = []

    for i in range(num_processes):
        start_line = i * chunk_size
        # Ensure the last process goes to the end of the file
        end_line = total_lines if i == num_processes - 1 else (i + 1) * chunk_size
        p = multiprocessing.Process(target=lambda q, arg1, arg2, arg3: q.append(find_title_for_asin(arg1, arg2, arg3[0], arg3[1])),
                                    args=(results, file_path, target_asin, (start_line, end_line)))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    # Flatten the list of results
    titles = [title for sublist in results for title in sublist]
    return titles

if __name__ == "__main__":
    directory = os.path.join(os.getcwd(), 'data')
    jsonl_file_path = os.path.join(directory, 'meta_Home_and_Kitchen.jsonl')  # Replace with your actual file path
    target_asin = 'B07ZPKR714'  # Replace with the target parent_asin you are looking for
    num_processes = multiprocessing.cpu_count()  # Use the number of available CPU cores

    titles = find_titles_in_parallel(jsonl_file_path, target_asin, num_processes)

    if titles:
        print(f"Found titles for ASIN {target_asin}: {titles}")
    else:
        print(f"No titles found for ASIN {target_asin}.")

