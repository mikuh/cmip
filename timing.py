import random
import string
import re
import time


from flashtext import KeywordProcessor
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

class Trie(object):

    def __init__(self, case_sensitive=False):
        self.root = {}
        self._case_sensitive = case_sensitive
        self._key = "**"
        self._replace_key = "&&"
        self._fail = "##"

    def __insert(self, word):
        if not self._case_sensitive:
            word = word.lower()
        current = self.root
        replace_word = None
        if isinstance(word, tuple):
            word, replace_word = word

        for char in word:
            current = current.setdefault(char, {})
            current[self._fail] = None
        # mark the end of the word
        current[self._key] = word
        current[self._replace_key] = replace_word

    def __build_links(self):
        queue = [self.root]
        is_root = True
        while queue:
            curr = queue.pop(0)
            for k, v in curr.items():
                if k == self._key or k == self._replace_key or k == self._fail:
                    continue
                if is_root:
                    v[self._fail] = self.root
                else:
                    if k in curr[self._fail]:
                        v[self._fail] = curr[self._fail][k]
                    else:
                        v[self._fail] = self.root
                queue.append(v)
            is_root = False

    def add_keywords_from_list(self, words: list):
        for word in words:
            self.__insert(word)
        self.__build_links()

    def get_all_keywords(self):
        ws = []
        currents = [self.root]
        while len(currents) > 0:
            current = currents.pop(0)
            for key in current:
                if key != self._key and key != self._replace_key and key != self._fail:
                    if self._key in current[key]:
                        ws.append(current[key][self._key])
                    currents.append(current[key])
        return ws

    def extract_keywords(self, sentence: str, all_mode=False, index_info=False):
        N = len(sentence)
        current = self.root
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
                            keywords.append(current[self._key])
                        else:
                            w = current[self._key]
                    j += 1
                else:
                    if all_mode:
                        current = self.root
                    else:
                        current = current.get("fail", self.root)
                    break
            if all_mode:
                i += 1
            else:
                if w:
                    keywords.append(w)
                    i = j
                elif current == self.root:
                    i += 1
        return keywords

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
                self._prefix_dic[w] = False
        self._prefix_dic[w] = True

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
        self._prefix_dic[word] = False

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
                if self._prefix_dic[flag]:
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


def get_word_of_length(str_length):
    # generate a random word of given length
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(str_length))


# generate a list of 100K words of randomly chosen size
all_words = [get_word_of_length(random.choice([3, 4, 5, 6, 7, 8])) for i in range(1000000)]
# all_words2 = [get_word_of_length(random.choice([3, 4, 5, 6, 7, 8])) for i in range(1000000)]
print(len(all_words))
print('Count  | FlashText | Regex | CMIP   ')
print('-------------------------------')
X = []
y1, y2, y3 = [], [], []
for keywords_length in range(0, 200001, 10000):
    # chose 5000 terms and create a string to search in.
    all_words_chosen = random.sample(all_words, 5000)
    story = ' '.join(all_words_chosen)

    # get unique keywords from the list of words generated.
    unique_keywords_sublist = list(set(random.sample(all_words, keywords_length)))

    # compile regex
    # compiled_re = re.compile('|'.join([r'\b' + keyword + r'\b' for keyword in unique_keywords_sublist]))

    # add keywords to flashtext
    keyword_processor = KeywordProcessor()
    keyword_processor.add_keywords_from_list(unique_keywords_sublist)

    # cmip
    trie = Trie()
    trie.add_keywords_from_list(unique_keywords_sublist)
    # time the modules
    start = time.time()
    a = keyword_processor.extract_keywords(story)
    mid1 = time.time()
    # _ = compiled_re.findall(story)
    mid2 = time.time()
    b = trie.extract_keywords(story)


    end = time.time()


    X.append(keywords_length)
    y1.append(mid1 - start)
    # y2.append(mid2 - mid1)
    y3.append(end - mid2)
    # print output
    print(str(keywords_length).ljust(6), '|',
          "{0:.5f}".format(mid1 - start).ljust(9), '|',
          "{0:.5f}".format(mid2 - mid1).ljust(9), '|',
          "{0:.5f}".format(end - mid2).ljust(9), '|',)



    fig, ax = plt.subplots()
    ax.plot(X, y1, label="flashtext")
    # ax.plot(X, y2)
    ax.plot(X, y3, label="该多模态信息处理工具")

    plt.xlabel("Num of keywords")
    plt.ylabel("Time(sec)")
    ax.set_title("extract speed compare on different scales keywords")
    ax.legend()
    plt.show()