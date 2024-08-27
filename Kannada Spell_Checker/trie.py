from Dictionary_load import read_categorized_file
class TrieNode:
    def __init__(self):
        self.children = {}
        self.isEndOfWord = False
        self.category = None

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, category=None):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.isEndOfWord = True
        node.category = category

    def search(self, word):
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                return False, None
        return node.isEndOfWord, node.category

    def get_all_words(self, node=None, word='', words=None):
        if words is None:
            words = []
        if node is None:
            node = self.root

        if node.isEndOfWord:
            words.append(word)

        for char, next_node in node.children.items():
            self.get_all_words(next_node, word + char, words)

        return words
    
    def get_all_words_with_categories(self, node=None, word='', words_with_cats=None):
        if words_with_cats is None:
            words_with_cats = []
        if node is None:
            node = self.root

        if node.isEndOfWord:
            words_with_cats.append((word, node.category))

        for char, next_node in node.children.items():
            self.get_all_words_with_categories(next_node, word + char, words_with_cats)

        return words_with_cats
 
    #Check for words with invalid suffix:
    def get_longest_valid_root(self, word):
        node = self.root
        valid_root = ""
        for i, char in enumerate(word):
            if char in node.children:
                node = node.children[char]
                if node.isEndOfWord:
                    valid_root = word[:i+1]
            else:
                break
        return valid_root

def setup_trie_with_categories(sub_dictionaries):
    trie = Trie()
    for category, words in sub_dictionaries.items():
        for word in words:
            trie.insert(word, category)
    return trie

def setup_trie_with_full_forms(sub_dictionaries, paradigm_tables):
    trie = Trie()
    # Insert root words
    for category, words in sub_dictionaries.items():
        for word in words:
            trie.insert(word, category)

    # Insert full forms by combining roots with suffixes
    for category, roots in sub_dictionaries.items():
        suffixes = paradigm_tables.get(category, [])
        for root in roots:
            for suffix in suffixes:
                full_form = root + suffix
                trie.insert(full_form, category)
    return trie

def test_trie_operations(trie):
    test_words = ["ಪ್ರಪಂಚದಲ್ಲಿ", "ಮುಖ್ಯವೇನೆಂದರೆ", "ಆಟದಲ್ಲಿ", "ಸಮಾಜದ", "ಸೋತುಬಿಡುತ್ತೇವೆ"]
    print("Testing trie operations...")
    for word in test_words:
        exists, category = trie.search(word)
        print(f"Word: {word}, Exists: {exists}, Category: {category if exists else 'N/A'}")

def main():
    sub_dictionaries = read_categorized_file("categorized.txt")
    paradigm_tables = {
        "1": ["ತ್ತಿದ್ದಳು", "ತ್ತಿದ್ದನು", "ತ್ತಿದ್ದಾರೆ", "ತ್ತೀಯ", "ತ್ತಾರೆ"],
        "2": ["ಗಳನ್ನು", "ಗಳಲ್ಲಿ", "ಗಳ"],
        "3": ["ದ್ದನು", "ದ್ದಳು", "ದ್ದರು"],
        "4": ["ದ", "ದಲ್ಲಿ", "ದಿಂದ"]
    }
    trie = setup_trie_with_full_forms(sub_dictionaries, paradigm_tables)
    test_trie_operations(trie)

if __name__ == "__main__":
    main()


def map_root_words_to_suffixes(category, root_words):
    """
    Map each root word in the given category to its valid inflections based on the suffixes.
    This function helps in generating all possible inflected forms of root words based on their category,
    which can be used for efficient suggestion generation and error detection in a spell checker.
    """
    # Define the paradigm tables with suffixes for different categories
    paradigm_tables = {
        "1": ["ತ್ತಿದ್ದಳು", "ತ್ತಿದ್ದನು", "ತ್ತಿದ್ದಾರೆ", "ತ್ತೀಯ", "ತ್ತಾರೆ"],  # Present tense of verbs
        "2": ["ಗಳನ್ನು", "ಗಳಲ್ಲಿ", "ಗಳ"],  # Plural forms
        "3": ["ದ್ದನು", "ದ್ದಳು", "ದ್ದರು"],  # Past tense of verbs
        "4": ["ದ", "ದಲ್ಲಿ", "ದಿಂದ"],  # Case endings
    }

    # Fetch the suffixes for the given category from the paradigm tables
    suffixes = paradigm_tables.get(category, [])

    # Initialize an empty dictionary to store the mapping
    root_word_mappings = {}

    # Iterate over each root word
    for root in root_words:
        # Generate all possible inflections for the root word based on the suffixes
        inflections = [root + suffix for suffix in suffixes]

        # Map the root word to its inflections
        root_word_mappings[root] = inflections

    return root_word_mappings






