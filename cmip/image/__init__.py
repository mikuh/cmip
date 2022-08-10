import cv2
import numpy as np


def ahash(fp, resize=8):
    im = cv2.imread(fp, cv2.IMREAD_UNCHANGED)
    im = cv2.resize(im, (resize, resize), cv2.INTER_AREA)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ahash = (im >= np.mean(im)) * 1
    ahash = np.array2string(ahash.flatten(), separator="", max_line_width=resize * resize + 2)
    return ahash[1:-1]


def dhash(fp, resize=8):
    im = cv2.imread(fp, cv2.IMREAD_UNCHANGED)
    im = cv2.resize(im, (resize + 1, resize), cv2.INTER_AREA)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    dhash = (im[:, :-1] >= im[:, 1:]) * 1
    dhash = np.array2string(dhash.flatten(), separator="", max_line_width=resize * resize + 2)
    return dhash[1:-1]


def phash(fp, resize=32, keep=8):
    im = cv2.imread(fp, cv2.IMREAD_UNCHANGED)
    im = cv2.resize(im, (resize, resize), cv2.INTER_AREA)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    gray_img_dct = cv2.dct(np.float32(im))
    gray_img_low_dct = gray_img_dct[0:keep, 0:keep]
    avg = np.mean(gray_img_low_dct)

    phash = (gray_img_low_dct >= avg) * 1

    phash = np.array2string(phash.flatten(), separator="", max_line_width=keep * keep + 2)
    return phash[1:-1]


if __name__ == '__main__':
    print(ahash("16199680.png"))
    print(dhash("16199680.png"))
    print(phash("16199680.png"))
