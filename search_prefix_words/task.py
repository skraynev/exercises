class FindTree():
    def __init__(self, words, tree=None):
        self.words = words
        self.tree = tree or {}
        self.sorted_words = sorted(words)

    def add_to_tree(self):
        for word in self.words:
            val = self.tree
            for s in word:
               if s not in val:
                   val[s] = {}
               val = val[s]

    def _find(self, sub_tree):
        r = []
        for k in sub_tree:
            if sub_tree[k] == {}:
                r.append(k)
            else:
                for v in self._find(sub_tree[k]):
                    r.append(k+v)
        return r

    def _queue_find(self, sub_tree):
        res = []
        tasks = []
        tasks.append(('', sub_tree))
        for parent, tree in tasks:
            for k in tree:
                if tree[k] == {}:
                    res.append(parent+k)
                else:
                    tasks.append((parent+k, tree[k]))
        return res

    # with recursion and tree
    def find_in_tree(self, prefix, with_recursion):
        self.add_to_tree()
        #import json
        #print(json.dumps(ft.tree, indent=5))
        val = self.tree
        for s in prefix:
            if s not in self.tree:
                return []
            else:
                val = val[s]
        method = self._find if with_recursion else self._queue_find
        return [prefix + k for k in method(val)]

    # binary search
    def binary_find(self, prefix, start=0, end=None):
        if end is None:
            end = len(self.sorted_words)
        half = start + ((end - start) / 2)
        mid = self.sorted_words[half]
        if mid.startswith(prefix):
            res = []
            val = mid
            count = half
            while val.startswith(prefix):
                res.append(val)
                count -= 1
                if count < 0:
                    break
                val = self.sorted_words[count]
            res.pop(0) #remove this duplicate
            val = mid
            count = half
            while val.startswith(prefix):
                res.append(val)
                count += 1
                if count >= len(self.sorted_words):
                    break
                val = self.sorted_words[count]
            return res

        elif mid < prefix:
            new_start=half
            new_end=end
        else:
            new_start=start
            new_end=half
        if new_start == start and new_end == end:
            return []
        return self.binary_find(prefix, start=new_start, end=new_end)

if __name__ == '__main__':
    words = ['kjasdhf', 'ADSadgds', 'fdasf', 'dsggg',
             'dfgsdfg', 'dfdfdf', 'kldasda', 'klsdfsd']
    print words

    ft = FindTree(words)
    for prefix in ('d', 'df', 'dfa'):
        print('Search', prefix, ft.find_in_tree(prefix, True))
        print('No_req', prefix, ft.find_in_tree(prefix, False))
        print('Binary', prefix, ft.binary_find(prefix))
