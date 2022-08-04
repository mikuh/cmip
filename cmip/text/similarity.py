def jaccard(s1: set, s2: set):
    return len(s1 & s2) / len(s1 | s2)


class Similarity(object):

    def __init__(self):
        pass

    def shingle(self, t1: str, t2: str, k=9):
        pass
