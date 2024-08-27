import unittest
from trie import Trie
from spellcheck import analyze_word, generate_suggestions_for_word, process_misspelled_word, setup_trie

paradigm_tables = {
    "1": ["ತ್ತಿದ್ದಳು", "ತ್ತಿದ್ದನು", "ತ್ತಿದ್ದಾರೆ", "ತ್ತೀಯ", "ತ್ತಾರೆ"],
    "2": ["ಗಳನ್ನು", "ಗಳಲ್ಲಿ", "ಗಳ"],
    "3": ["ದ್ದನು", "ದ್ದಳು", "ದ್ದರು"],
    "4": ["ದ", "ದಲ್ಲಿ", "ದಿಂದ"],
}

class TestDataPreprocessing(unittest.TestCase):
    def test_clean_text(self):
        print("\nRunning test_clean_text...")
        text = "Some text with ನಾನ್ non-Kannada characters!"
        cleaned_text = clean_text(text)
        print("Cleaned text:", cleaned_text)
        self.assertEqual(cleaned_text, "ನಾನ್")
        print("Test passed: test_clean_text")

    def test_categorize_suffix(self):
        print("\nRunning test_categorize_suffix...")
        paradigm_tables = {
            "1": ["ತ್ತಿದ್ದಳು", "ತ್ತಿದ್ದನು", "ತ್ತಿದ್ದಾರೆ", "ತ್ತೀಯ", "ತ್ತಾರೆ"],
            "2": ["ಗಳನ್ನು", "ಗಳಲ್ಲಿ", "ಗಳ"],
        }
        word = "ಪ್ರೀತಿಸುತ್ತಿದ್ದಳು"
        category = categorize_suffix(word, paradigm_tables)
        print("Suffix category for '{}': {}".format(word, category))
        self.assertEqual(category, "1")
        print("Test passed: test_categorize_suffix")

class TestTrieOperations(unittest.TestCase):
    def test_insert_and_search(self):
        print("\nRunning test_insert_and_search...")
        trie = Trie()
        trie.insert("ಕನ್ನಡ")
        result = trie.search("ಕನ್ನಡ")[0]
        print("Searching for 'ಕನ್ನಡ':", result)
        self.assertTrue(result)
        print("Test passed: test_insert_and_search")
        print("------------------------------------------------------------")


    def test_search_nonexistent(self):
        print("\nRunning test_search_nonexistent...")
        trie = Trie()
        trie.insert("ಕನ್ನಡ")
        result = trie.search("ಭಾರತ")[0]
        print("Searching for 'ಭಾರತ':", result)
        self.assertFalse(result)
        print("Test passed: test_search_nonexistent")
        print("------------------------------------------------------------")

    def test_stemming(self):
        print("\nRunning test_stemming...")
        root, suffix = analyze_word("ಪ್ರೀತಿಸುತ್ತಿದ್ದಳು", paradigm_tables)
        print(f"Analyzed 'ಪ್ರೀತಿಸುತ್ತಿದ್ದಳು' -> Root: '{root}', Suffix: '{suffix}'")
        self.assertEqual(root, "ಪ್ರೀತಿಸು")
        self.assertEqual(suffix, "ತ್ತಿದ್ದಳು")
        print("Test passed: test_stemming")
        print("------------------------------------------------------------")

def clean_text(text):
    import re
    return re.sub(r"[^\u0C80-\u0CFF]", "", text).strip()

def categorize_suffix(word, paradigm_tables):
    for category, suffixes in paradigm_tables.items():
        for suffix in suffixes:
            if word.endswith(suffix):
                return category
    return None

class TestSpellChecking(unittest.TestCase):
    def setUp(self):
        # Set up the trie for testing
        self.trie = setup_trie()
        self.paradigm_tables = {
            "1": ["ತ್ತಿದ್ದಳು", "ತ್ತಿದ್ದನು", "ತ್ತಿದ್ದಾರೆ", "ತ್ತೀಯ", "ತ್ತಾರೆ"],
            "2": ["ಗಳನ್ನು", "ಗಳಲ್ಲಿ", "ಗಳ"],
            "3": ["ದ್ದನು", "ದ್ದಳು", "ದ್ದರು"],
            "4": ["ದ", "ದಲ್ಲಿ", "ದಿಂದ"],
        }

    def test_correct_words(self):
        print("\nRunning test_correct_words...")
        result = process_misspelled_word("ಕನ್ನಡ", self.trie, self.paradigm_tables)
        print("Spell check result for 'ಕನ್ನಡ':", result)
        self.assertFalse(result)
        print("Test passed: test_correct_words")

    def check_suggestions(self, word, correct_word):
        suggestions = generate_suggestions_for_word(word, self.trie, self.paradigm_tables)
        print(f"Suggestions for '{word}': {suggestions}")
        try:
            index = suggestions.index(correct_word) + 1
            print(f"'{correct_word}' is suggestion number {index}")
            return index
        except ValueError:
            print(f"'{correct_word}' not found in suggestions")
            return None

    def test_completely_misspelled_words(self):
        print("\nRunning test_completely_misspelled_words...")
        test_cases = [
            ("ಅಶ್ಯವಾಗವಂಥ", "ಅವಶ್ಯವಾಗುವಂಥ"),
            ("ಸಾಕಾಣಿಗ", "ಸಾಕಾಣಿಗೆ"),
            ("ಉತ್ತರಕಾಶ್ಮೀರಾ", "ಉತ್ತರಕಾಶ್ಮೀರ"),
            ("ಉತ್ತರಕುಮಾರನ್", "ಉತ್ತರಕುಮಾರ"),
            ("ಪಚಪ್ರಣಗಳಲ್ಲಿ", "ಪಂಚಪ್ರಾಣಗಳಲ್ಲಿ"),
            ("ಪಂಚಬ್ಹ್ದೇವತಾರ್ನೆ", "ಪಂಚಬ್ರಹ್ಮದೇವತಾರ್ಚನೆ"),
            ("ಅರ್ಥನಿರಣೆ", "ಅರ್ಥನಿರೂಪಣೆ"),
            ("ವಾಯುಗುದೊದಿಗೆ", "ವಾಯುಗುಣದೊಂದಿಗೆ"),
            ("ಶಿಶ್ಯಪರರೆಯಲ್ಲಿ", "ಶಿಶ್ಯಪರಂಪರೆಯಲ್ಲಿ"),
            ("ಕ್ವಪಿನವತ್ತೀಷ್ಟನಿಷ್ಟಂ", "ಕ್ವಾಪಿನವೇತ್ತೀಷ್ಟಮನಿಷ್ಟಂ")
        ]

        # Initialize counters for ranking statistics
        top_1_count = 0
        top_5_count = 0
        top_8_count = 0
        total_tests = len(test_cases)

        for word, correct_word in test_cases:
            rank = self.check_suggestions(word, correct_word)
            if rank is not None:
                if rank == 1:
                    top_1_count += 1
                if rank <= 5:
                    top_5_count += 1
                if rank <= 8:
                    top_8_count += 1

        # Calculate percentages
        top_1_percentage = (top_1_count / total_tests) * 100
        top_5_percentage = (top_5_count / total_tests) * 100
        top_8_percentage = (top_8_count / total_tests) * 100

        # Print summary
        print(f"Correct suggestions rate:")
        print(f"Top 1 candidate: {top_1_percentage:.2f}%")
        print(f"Top 5 candidates: {top_5_percentage:.2f}%")
        print(f"Top 8 candidates: {top_8_percentage:.2f}%")
        print("Test passed: test_completely_misspelled_words")

    def test_invalid_root_with_valid_suffix(self):
        print("\nRunning test_invalid_root_with_valid_suffix...")
        test_cases = [
            ("ಅಂಗಡೆಗಳನ್ನು", "ಅಂಗಡಿಗಳನ್ನು"),
            ("ಅಂಗವಾಡಿಗಳನ್ನು", "ಅಂಗನವಾಡಿಗಳನ್ನು"),
            ("ಅಡಮನಗಳ", "ಅಡಮಾನಗಳ"),
            ("ೊಡುತ್ತಿದ್ದನು", "ಕೊಡುತ್ತಿದ್ದನು"),
            ("ಅಡಗೆಪುಸ್ಕಗಳಲ್ಲಿ", "ಅಡುಗೆಪುಸ್ತಕಗಳಲ್ಲಿ"),
            ("ಮಾತಡತ್ತಿದ್ದಳು", "ಮಾತಾಡುತ್ತಿದ್ದಳು")
        ]

        # Initialize counters for ranking statistics
        top_1_count = 0
        top_5_count = 0
        top_8_count = 0
        total_tests = len(test_cases)

        for word, correct_word in test_cases:
            rank = self.check_suggestions(word, correct_word)
            if rank is not None:
                if rank == 1:
                    top_1_count += 1
                if rank <= 5:
                    top_5_count += 1
                if rank <= 8:
                    top_8_count += 1

        # Calculate percentages
        top_1_percentage = (top_1_count / total_tests) * 100
        top_5_percentage = (top_5_count / total_tests) * 100
        top_8_percentage = (top_8_count / total_tests) * 100

        # Print summary
        print(f"Correct suggestions rate:")
        print(f"Top 1 candidate: {top_1_percentage:.2f}%")
        print(f"Top 5 candidates: {top_5_percentage:.2f}%")
        print(f"Top 8 candidates: {top_8_percentage:.2f}%")
        print("Test passed: test_invalid_root_with_valid_suffix")


if __name__ == '__main__':
    print("Starting tests...")
    unittest.main()
    print("All tests completed.")