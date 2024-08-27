def remove_empty_lines(input_file_path, output_file_path):
    """Remove empty lines from a file and write the result to another file."""
    with open(input_file_path, 'r', encoding='utf-8') as infile, \
         open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            if line.strip():  # Checks if the line is not just whitespace or empty
                outfile.write(line)
# Usage example
input_file_path = 'final_filter_wiki.txt' 
output_file_path = 'wiki.txt' 
remove_empty_lines(input_file_path, output_file_path)
print('Kannada file cleaned ')
