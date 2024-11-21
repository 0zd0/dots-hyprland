import os


def remove_comments_and_empty_lines(input_file: str, output_file: str) -> None:
    """
    Removes comments and empty lines from a file and writes the result to another file.

    Args:
        input_file (str): Path to the input file.
        output_file (str): Path to the output file.
    """
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        for line in infile:
            # Remove comments and strip whitespace
            line = line.split("#", 1)[0].strip()
            # Write non-empty lines to the output file
            if line:
                outfile.write(line + "\n")
