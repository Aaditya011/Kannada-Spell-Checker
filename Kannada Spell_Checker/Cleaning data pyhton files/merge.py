def merge_and_deduplicate_kannada_files(file_path1, file_path2, output_file_path):
    # Use a set to store unique words
    unique_words = set()

    # Function to process lines from the file
    def process_line(line):
        # Strip leading and trailing whitespace and split by whitespace
        # This is basic and might need adjustment for specific cases
        return line.strip().split()

    # Read and process the first file
    with open(file_path1, 'r', encoding='utf-8') as file1:
        for line in file1:
            unique_words.update(process_line(line))

    # Read and process the second file
    with open(file_path2, 'r', encoding='utf-8') as file2:
        for line in file2:
            unique_words.update(process_line(line))

    # Write the unique words to the output file
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        for word in sorted(unique_words):
            outfile.write(word + '\n')
# Usage example
file_path1 = 'wiki.txt'  # Update this to your first file path
file_path2 = 'Root_word_dictionary_3.txt'  # Update this to your second file path
output_file_path = 'Final_dictionary.txt'  # Update this to your desired output file path

merge_and_deduplicate_kannada_files(file_path1, file_path2, output_file_path)
