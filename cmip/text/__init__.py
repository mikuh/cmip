from cmip.text.ac_automation import ACAutomation
from cmip.text.normalize import Normalize
from joblib import Parallel, delayed
import multiprocessing
import re

n_cpus = multiprocessing.cpu_count()
default_pattern = re.compile("[^\u4E00-\u9FEF\u3400-\u4DB5a-zA-Z0-9]+", re.U)


class Text(object):

    def __init__(self, case_sensitive=True):
        self.aca = ACAutomation(case_sensitive=case_sensitive)
        self.norm = Normalize()
        self.add_keywords_from_list = self.aca.add_keywords_from_list
        self.get_keywords = self.aca.get_keywords
        self.replace_keywords = self.aca.replace_keywords
        self.extract_keywords = self.aca.extract_keywords
        self.normalize = self.norm.normalize
        self.pinyin = self.norm.pinyin

    def clean(self, sentence, patten: str = None, keep_space: bool = True, norm: bool = True, lower: bool = True,
              digital_norm: bool = False, max_repeat: int = 0) -> str:
        if patten is None:
            patten = default_pattern
        else:
            patten = re.compile(patten, re.U)
        if norm:
            sentence = self.normalize(sentence)
        if lower:
            sentence = sentence.lower()
        sentence = patten.sub(" ", sentence)
        if keep_space:
            sentence = re.sub(r" +", " ", sentence)
        else:
            sentence = re.sub(r" +", "", sentence)
        if digital_norm:
            sentence = re.sub(r'\d+', '𝝢', sentence)
        if max_repeat > 0:
            sentence = re.sub(r'(.)\1{' + str(max_repeat) + r',}', r'\1' * max_repeat, sentence)
        return sentence

    def batch_extract_keywords(self, sentences, n_jobs=n_cpus, batch_size=1000):
        out = Parallel(n_jobs=n_jobs, verbose=9, batch_size=batch_size)(delayed(self.extract_keywords)(s) for s in sentences)
        return out

    def batch_replace_keywords(self, sentences, n_jobs=n_cpus, batch_size=1000):
        out = Parallel(n_jobs=n_jobs, verbose=9, batch_size=batch_size)(delayed(self.replace_keywords)(s) for s in sentences)
        return out

    def batch_clean(self, sentences, n_jobs=n_cpus, batch_size=1000, patten: str = None, keep_space: bool = True, norm: bool = True,
                    lower: bool = True, digital_norm: bool = False, max_repeat: int = 0):
        out = Parallel(n_jobs=n_jobs, verbose=9, batch_size=batch_size)(
            delayed(self.clean)(s, patten, keep_space, norm, lower, digital_norm, max_repeat) for s in sentences)
        return out

    def batch_cut(self, sentences, tokenizer, n_jobs=n_cpus, verbose=10, batch_size=1000):
        assert hasattr(tokenizer, 'lcut')

        def cut(s):
            return tokenizer.lcut(s)

        out = Parallel(n_jobs=n_jobs, verbose=verbose, batch_size=batch_size)(delayed(cut)(s) for s in sentences)
        return out
