from nltk.util import ngrams


class Similarity(object):

    def __init__(self):
        pass

    def jaccard(self, s1: set, s2: set):
        if len(s1) == 0 and len(s2) == 0:
            return 1
        return len(s1 & s2) / len(s1 | s2)

    def shingle(self, t1: str, t2: str, k=9, f=lambda x: x):
        s1 = set(ngrams(f(t1), k))
        s2 = set(ngrams(f(t2), k))
        return self.jaccard(s1, s2)


if __name__ == '__main__':
    simi = Similarity()

    print(simi.shingle("我是中国人", "我是中华人", k=1))
