import re

from trie import Trie

lex = Trie('*')

with open('data.txt', 'r', encoding='UTF-8') as f:
    words = f.read().lower()
    f.close()

words = words[:10000]
words = re.split("[:.,;!?\-\[\]\n\t() ]+", words)

for word in words:
    lex.put(word)

print(lex.get('при'))
print(lex.get('фр'))
