import sys
import os
import numpy as np
import torch
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "src")))

import segmentation


def test_torch2numpy():
    d = {
         'boxes': torch.ones(5 * 4).view(5, 4),
         'labels': torch.ones(5),
         'scores': torch.ones(5)
        }
    output = segmentation.torch2numpy(d)

    assert type(output) is dict
    assert type(output['boxes']) is np.ndarray
    assert type(output['labels']) is np.ndarray
    assert type(output['scores']) is np.ndarray


def test_filter():
    d = {
         'boxes': np.zeros((5, 4)),
         'labels': np.zeros(5),
         'scores': np.array([0.7, 0, 0.4, 0.8, 0.9])
        }
    boxes, labels, scores = segmentation.filter(d)

    assert type(labels) is list
    assert type(scores) is list
    assert labels == [0, 0, 0]
    assert scores == [0.7, 0.8, 0.9]


def test_categories_from_txt():
    path = '../data/tests_data/categories.txt'
    categories = segmentation.categories_from_txt(path)

    assert type(categories) is list
    assert categories == ['a', 'b', 'c', 'd']


def test_model_predictions():
    path = '../data/tests_data/test.jpg'
    output = segmentation.model_predictions(Image.open(path))

    boxes, labels, scores = segmentation.filter(output)

    assert type(labels) is list
    assert type(scores) is list
    assert len(labels) == 2
    assert len(scores) == 2
    assert len(boxes) == 2
    assert labels[0] == 2 or labels[1] == 2
    assert labels[0] == 3 or labels[1] == 3


def test_segmentation():
    path = '../data/tests_data/test.jpg'

    img = segmentation.segmentation(path)

    assert type(img) is Image.Image
    assert img.width == 1280
    assert img.height == 853
