class ACAutomation(object):

    def __init__(self, case_sensitive=True):
        self.trie = {}
        self._case_sensitive = case_sensitive
        self._key = "**"
        self._replace_key = "&&"
        self._fail = "##"

    def __insert(self, word):
        replace_word = None
        if isinstance(word, tuple):
            word, replace_word = word
        if not self._case_sensitive:
            word = word.lower()
        current = self.trie
        for char in word:
            current = current.setdefault(char, {})
            current[self._fail] = None
        # mark the end of the word
        current[self._key] = word
        current[self._replace_key] = replace_word

    def __build_links(self):
        queue = [self.trie]
        is_root = True
        while queue:
            curr = queue.pop(0)
            for k, v in curr.items():
                if k == self._key or k == self._replace_key or k == self._fail:
                    continue
                if is_root:
                    v[self._fail] = self.trie
                else:
                    if k in curr[self._fail]:
                        v[self._fail] = curr[self._fail][k]
                    else:
                        v[self._fail] = self.trie
                queue.append(v)
            is_root = False

    def add_keywords_from_list(self, words: list):
        """
        Add the keywords you want to match
        :param words:
        :return: None
        """
        for word in words:
            self.__insert(word)
        self.__build_links()

    def get_all_keywords(self):
        """
        get all the keywords in trie
        :return: a list of keywords
        """
        ws = []
        currents = [self.trie]
        while len(currents) > 0:
            current = currents.pop(0)
            for key in current:
                if key != self._key and key != self._replace_key and key != self._fail:
                    if self._key in current[key]:
                        ws.append(current[key][self._key])
                    currents.append(current[key])
        return ws

    def extract_keywords(self, sentence: str, all_mode: bool = False, index_info: bool = False) -> list:
        """
        extract the keywords from the sentence
        :param sentence: the sentence string
        :param all_mode: whether all keywords are identified,otherwise only scan the longest parts
        :param index_info: contains coordinates or not
        :return: a list of keywords like [key1,key2,key3],
                 if index_info is True,  return like [(key1, start_pos, end_pos),...]
        """
        if not self._case_sensitive:
            sentence = sentence.lower()
        N = len(sentence)
        current = self.trie
        keywords = []
        i = 0
        while i < N:
            j = i
            w = None
            while j < N:
                c = sentence[j]
                if c in current:
                    current = current[c]
                    if self._key in current:
                        if all_mode:
                            if index_info:
                                keywords.append((current[self._key], (i, j + 1)))
                            else:
                                keywords.append(current[self._key])
                        else:
                            w = current[self._key]
                    j += 1
                else:
                    if all_mode:
                        current = self.trie
                    else:
                        current = current.get(self._fail, self.trie)
                    break
            if w:
                if index_info:
                    keywords.append((w, i, i + len(w)))
                else:
                    keywords.append(w)
                i = j
            elif current == self.trie:
                i += 1
        return keywords

    def replace_keywords(self, sentence: str) -> str:
        """
        Replace keywords in sentences
        :param sentence: the sentence string
        :return: the new sentence string after replace
        """
        if not self._case_sensitive:
            sentence = sentence.lower()
        N = len(sentence)
        new_sentence = []
        i = 0
        while i < N:
            current = self.trie
            j = i
            w = None
            while j < N:
                c = sentence[j]
                if c in current:
                    current = current[c]
                    if self._replace_key in current and self._replace_key:
                        w = current[self._replace_key]
                    j += 1
                else:
                    break
            if w:
                new_sentence.append(w)
                i += len(w) + 1
            else:
                new_sentence.append(sentence[i])
                i += 1
        return ("{}" * len(new_sentence)).format(*new_sentence)