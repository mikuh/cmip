from cmip.web.simhash_utils import SimHash
from cmip.web.html import Html
from cmip.web.utils import hamming_distance_array, is_valid_url, url2domain, top_domain, decode_image
from cmip.web.web_scraping import web_scraping
import numpy as np

sh = SimHash()
html = Html()

simhash = sh.simhash
simhash_array = sh.simhash_array
simhash_string = sh.simhash_string


def hamming_distance_array(a: np.ndarray, b: np.ndarray, axis=1) -> int:
    return np.sum(np.not_equal(a, b), axis=axis)


__all__ = ['simhash', 'simhash_array', 'simhash_string', 'html', 'url2domain', 'top_domain', 'decode_image',
           'web_scraping', 'hamming_distance_array']
