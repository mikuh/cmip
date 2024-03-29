import validators
import numpy as np
from urllib.parse import urlparse
import base64


def hamming_distance_array(a: np.ndarray, b: np.ndarray, axis=1) -> int:
    return np.sum(np.not_equal(a, b), axis=axis)


def is_valid_url(url: str) -> str:
    return validators.url(url)


def url2domain(url: str) -> str:
    if validators.url(url):
        return urlparse(url).hostname.lower().strip('.')
        # return urlparse(url).netloc.lower().strip('.')


def top_domain(domain: str) -> str:
    parts = domain.lower().split(".")
    if len(parts) > 1:
        if parts[-2] in {'com', 'edu', 'net', 'org', 'co'}:
            return '.'.join(parts[-3:])
        return '.'.join(parts[-2:])


def decode_image(src: str):
    data = src.split(",")[-1]
    img = base64.urlsafe_b64decode(data)
    return img
