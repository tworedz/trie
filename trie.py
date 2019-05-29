class Trie:
    def __init__(self, char: str):
        self.char = char
        self.children = []
        self.end_of_word = False
        self.word = ''

    def __repr__(self):
        return f'{self.char} - {self.children}'

    def put(self, word: str):
        node = self

        for char in word:
            found_in_child = False
            for child in node.children:
                if child.char == char:
                    node = child
                    found_in_child = True
                    break

            if not found_in_child:
                new_node = Trie(char)
                node.children.append(new_node)
                node = new_node
        node.end_of_word = True
        node.word = word

    def get(self, prefix: str):
        node = self
        if not node.children:
            return 0

        for char in prefix:
            char_not_found = True
            for child in node.children:
                if child.char == char:
                    char_not_found = False
                    node = child
                    break
            if char_not_found:
                return 0

        words = []
        Trie.get_words(node, words)
        words = sorted(words)
        return words

    @staticmethod
    def get_words(node, words):
        for child in node.children:
            if child.end_of_word:
                words.append(child.word)
            Trie.get_words(child, words)
