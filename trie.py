class Trie:
    def __init__(self):
        self.children = {}
        self.end_of_word = 0
        self.word = ''

    def __repr__(self):
        return f'{self.word} {self.end_of_word}'

    def __str__(self):
        return self.__repr__()

    def put(self, word: str, cnt=1):
        node = self

        for char in word:
            child = node.children.get(char)
            if child:
                node = child
            else:
                new_node = Trie()
                node.children[char] = new_node
                node = new_node
        node.end_of_word += int(cnt)
        node.word = word

    def get(self, prefix: str):
        node = self
        if not node.children:
            return 0

        for char in prefix:
            child = node.children.get(char)
            if child:
                node = child
            else:
                return 0

        words = []
        if node.end_of_word:
            words.append(node)
        Trie.get_words(node, words)
        words = sorted(words, key=lambda x: x.end_of_word, reverse=True)
        return words

    @staticmethod
    def get_words(node, words):
        for child in node.children.values():
            if child.end_of_word:
                words.append(child)
            Trie.get_words(child, words)
