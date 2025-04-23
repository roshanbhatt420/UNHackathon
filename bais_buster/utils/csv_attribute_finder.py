import csv

def get_attributes_from_csv(file_path):
    """
    Reads the header row of a CSV file and returns the list of attributes (column names).

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list: List of attribute names (column headers) from the CSV file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty or does not contain a header row.
    """
    try:
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            headers = next(reader, None)
            if headers is None:
                raise ValueError("The CSV file is empty or does not contain a header row.")
            return headers
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the file: {e}") from e

# Example usage:
# attributes = get_attributes_from_csv('path/to/file.csv')
# print(attributes)