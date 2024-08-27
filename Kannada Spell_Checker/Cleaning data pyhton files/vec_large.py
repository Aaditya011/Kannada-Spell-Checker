def extract_words_from_vec_file(vec_file_path, output_file_path):
    with open(vec_file_path, 'r', encoding='utf-8') as vec_file:
        # Skip the first line containing metadata
        next(vec_file)
        # Open the output file to write the words
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for line in vec_file:
                # Extract the word (the first element in each line)
                word = line.split(' ', 1)[0]
                # Write the word to the output file
                output_file.write(word + '\n')
    print("Words have been extracted to", output_file_path)

# Specify the path to your .vec file and the output file
vec_file_path = 'Large_vec.vec'
output_file_path = 'extracted_words.txt'

# Extract words
extract_words_from_vec_file(vec_file_path, output_file_path)
