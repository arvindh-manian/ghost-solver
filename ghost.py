import queue

NUM_PLAYERS = 2


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode('*', parent=None)

    def add(self, word: str) -> None:
        '''adds a node to the Trie'''
        node = self.root
        for char in word:
            flag = False
            flag = char in node.children.keys()
            if not flag:
                new_node = TrieNode(char, parent=node)
                node.children[char] = new_node
            node = node.children[char]
        node.finished = True

    def __find_node__(self, word: str):
        word = word.upper()
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                return None
        return node

    def starting_with_prefix(self, prefix: str) -> [str]:
        '''returns a list of words starting with the desired prefix'''
        node = self.__find_node__(prefix)
        new_lst = []
        length = len(prefix)
        if node is None:
            return []
        for child in node.children.values():
            lst = child.__starting_with__()
            flag = True
            for word in lst:
                if (len(word) - length) % NUM_PLAYERS == 1:
                    flag = False
                    break
            if flag:
                return lst
            new_lst.append(lst)
        return []


class TrieNode:
    def __init__(self, char: str, parent, finished=False):
        self.char = char
        self.children = {}
        self.finished = finished
        self.parent = parent

    def __str__(self):
        if not self.parent:
            return ''
        return str(self.parent) + self.char

    def __starting_with__(self) -> [str]:
        q = queue.Queue()
        lst = []
        for child in self.children.values():
            q.put(child)
        while not q.empty():
            node = q.get()
            if node.finished:
                lst.append(str(node))
            else:
                for child in node.children.values():
                    q.put(child)
        return lst


if __name__ == '__main__':
    t = Trie()
    print('Initializing...')
    with open('words.txt') as words:  # fill the Trie
        for line in words:
            t.add(line[:-1])
    NUM_PLAYERS = input('How many players are there?\n')
    while True:
        try:
            NUM_PLAYERS = int(NUM_PLAYERS)
            break
        except ValueError:
            print('Invalid response')
            NUM_PLAYERS = input('How many players are there?\n')
    print('Done with setup! Enter query, "q" to quit:')
    query = input()
    while query != 'q':
        ans = t.starting_with_prefix(query)
        if ans:
            print(f'You should say {ans[0][len(query)]}')
        else:
            print(f'You cannot force a win')
        query = input('Enter query, "q" to quit:\n')
