def load_dictionary_words(file_path):
    dictionary_words = set()
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            dictionary_words.add(line.strip())
    return dictionary_words

#Rule based suffix stripping
def categorize_words(dictionary_words):
    complex_suffixes = {
        1: ["ತ್ತಿದ್ದಳು","ತ್ತಿದ್ದನು","ತ್ತಿದ್ದಾರೆ","ತ್ತೀಯ","ತ್ತಾರೆ"], #present tense of verbs
        2: ["ಗಳನ್ನು", "ಗಳಲ್ಲಿ", "ಗಳ"],
        3: ["ದ್ದನು","ದ್ದಳು","ದ್ದರು"],  #past tense of verbs
        4: ["ದ", "ದಲ್ಲಿ", "ದಿಂದ"],
    }
    categorized_roots = {category: set() for category in complex_suffixes}
    all_categorized_words = set()

    for word in dictionary_words:
        for category, suffixes in complex_suffixes.items():
            for suffix in suffixes:
                if word.endswith(suffix):
                    root = word[:-len(suffix)]
                    if all(root + s in dictionary_words for s in suffixes):
                        categorized_roots[category].add(root)
                        all_categorized_words.add(word)

    return categorized_roots, all_categorized_words

def write_categorized_results(categorized_roots, all_categorized_words, dictionary_words, file_path):
    uncategorized_words = dictionary_words - all_categorized_words
    all_categorized_roots = set()
    for roots in categorized_roots.values():
        all_categorized_roots.update(roots)
    filtered_uncategorized_words = sorted([word for word in uncategorized_words if word not in all_categorized_roots])

    with open(file_path, "w", encoding="utf-8") as f:
        for category, roots in categorized_roots.items():
            f.write(f"Category {category}:\n" + "\n".join(sorted(roots)) + "\n\n")
        f.write("Uncategorized:\n" + "\n".join(filtered_uncategorized_words))

def read_categorized_file(file_path):
    sub_dictionaries = {}
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    current_category = None
    for line in lines:
        line = line.strip()
        if "Category" in line:
            current_category = line.split(":")[0].split(" ")[1]
            sub_dictionaries[current_category] = set()
        elif "Uncategorized" in line:
            current_category = "Uncategorized"
            sub_dictionaries[current_category] = set()
        elif line and current_category:
            sub_dictionaries[current_category].add(line)

    return sub_dictionaries

def main():
    file_path = "Final_dictionary.txt"
    dictionary_words = load_dictionary_words(file_path)
    categorized_roots, all_categorized_words = categorize_words(dictionary_words)
    write_categorized_results(categorized_roots, all_categorized_words, dictionary_words, "categorized.txt")
    sub_dictionaries = read_categorized_file("categorized.txt")

    for category, words in sub_dictionaries.items():
        print(f"Category {category} has {len(words)} words.")
    
    print(f"Total words loaded: {len(dictionary_words)}")
    

if __name__ == "__main__":
    main()
