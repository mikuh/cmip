class PrefixSet(object):

    def __init__(self):
        self._prefix_dic = {}
        self._replace_map = {}

    def get_keywords(self):
        return {w for w, f in self._prefix_dic.items() if f == 1}

    def get_replace_map(self):
        return {a: b for a, b in self._replace_map.items() if b is not None}

    def add_keywords_from_list(self, words: list):
        for word in words:
            self.add_keyword(word)

    def add_keyword(self, word):
        w = ""
        for ch in word:
            w += ch
            if w not in self._prefix_dic:
                self._prefix_dic[w] = 0
        self._prefix_dic[w] = 1

    def add_keywords_replace_map_from_dict(self, source_target_map: dict):
        for a, b in source_target_map.items():
            w = ""
            for ch in a:
                w += ch
                if w not in self._replace_map:
                    self._replace_map[w] = None
            self._replace_map[a] = b

    def remove_keywords_from_list(self, words: list):
        for word in words:
            self.remove_keyword(word)

    def remove_keyword(self, word: str):
        self._prefix_dic[word] = 0

    def extract_keywords(self, sentence: str, skip_match=False) -> list:
        """Extract keywords involved in sentences
        Args:
            sentence: str, Sentences to be extracted.
            skip_match: bool,When the keywords are matched, whether to skip this area and
                        no longer detect the communicative part of words;
                        for a example sentence: `cattention`, and keywords is ['cat', 'attention'],
                        if set False, return: ['cat', 'attention'],
                        if set True, return  first match only: ['cat']
        """
        N = len(sentence)
        keywords = []
        i = 0
        while i < N:
            flag = sentence[i]
            j = i
            word = None
            while j < N and (flag in self._prefix_dic):
                if self._prefix_dic[flag] == 1:
                    if not skip_match:
                        keywords.append(flag)
                    word = flag
                j += 1
                flag = sentence[i: j + 1]
            if word and skip_match:
                keywords.append(word)
                i += len(word) - 1
            i += 1
        return keywords

    def extract_keywords_with_index(self, sentence: str, skip_match=False):
        N = len(sentence)
        keywords = []
        i = 0
        while i < N:
            flag, index = sentence[i], [i, i + 1]
            j = i
            word = None
            while j < N and (flag in self._prefix_dic):
                if self._prefix_dic[flag] == 1:
                    if not skip_match:
                        keywords.append((flag, index))
                    word, _index = flag, index
                j += 1
                flag, index = sentence[i: j + 1], [i, j + 1]
            if word and skip_match:
                keywords.append((word, _index))
                i += len(word) - 1
            i += 1
        return keywords

    def replace_keywords(self, sentence: str) -> str:
        """Replace word use keywords map.
        Args:
            sentence: str, Sentences that need to replace keywords.
        Return:
            the new sentence after replace keywords.
        """
        N = len(sentence)
        new_sentence = ""
        i = 0
        while i < N:
            flag = sentence[i]
            j = i
            word = None
            while j < N and (flag in self._replace_map):
                if self._replace_map[flag]:
                    word = flag
                j += 1
                flag = sentence[i: j + 1]
            if word:
                new_sentence += self._replace_map[word]
                i = j
            else:
                new_sentence += sentence[i]
                i += 1
        return new_sentence


if __name__ == '__main__':
    ps = PrefixSet()
    ps.add_keywords_from_list(["中华人民共和国", "国人", "共和国"])
    founds = ps.extract_keywords("我是中华人民共和国人", skip_match=True)
    print(founds)