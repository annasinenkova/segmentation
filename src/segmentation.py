"""Image segmentation."""

from PIL import Image
import torchvision
import warnings
import torch
import random
import numpy as np
import cv2


def torch2numpy(torch_dict: dict) -> dict:
    """Return a numpy dict from a torch dict."""
    np_dict = {}

    for k in torch_dict.keys():
        np_dict[k] = torch_dict[k].cpu().numpy()

    return np_dict


def filter(output: dict) -> list | list | list:
    """Return objects with a probability >= 0.5."""
    boxes = []
    labels = []
    scores = []

    for i in range(len(output['scores'])):
        if output['scores'][i] >= 0.5:
            boxes.append(output['boxes'][i])
            labels.append(output['labels'][i])
            scores.append(output['scores'][i])

    return boxes, labels, scores


def categories_from_txt(path: str) -> list:
    """Read categories from a file and return array."""
    categories = []
    with open(path, 'r') as file:
        for line in file:
            categories.append(line.strip())

    return categories


def model_predictions(img: Image.Image) -> dict:
    """Return pretrained model predictions."""
    torch.set_grad_enabled(False)
    warnings.filterwarnings("ignore")
    pretrained_model = torchvision.models.detection.maskrcnn_resnet50_fpn(
                       pretrained=True
    )
    pretrained_model = pretrained_model.eval().cpu()

    img_tensor = torchvision.transforms.functional.to_tensor(img).cpu()

    output = pretrained_model([img_tensor])[0]
    output = torch2numpy(output)

    return output


def segmented_image(img: np.ndarray,
                    boxes: list,
                    labels: list,
                    scores: list) -> Image.Image:
    """Return a segmented image."""
    categories = categories_from_txt('../data/categories.txt')

    colors = [[random.randint(0, 255) for _ in range(3)] for _ in categories]

    for box, label, score, in zip(boxes, labels, scores):
        color = random.choice(colors)
        tl = round(0.002 * max(img.shape[0:2])) + 1
        c1, c2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
        cv2.rectangle(img, c1, c2, color, thickness=tl)
        text = "%s: %.1f%%" % (categories[label], 100*score)
        tf = max(tl - 1, 1)
        t_size = cv2.getTextSize(text, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1)
        cv2.putText(img, text,
                    (c1[0], c1[1] - 2), 0, tl / 3,
                    [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

    return Image.fromarray(img.astype(np.uint8))


def segmentation(path: str) -> Image.Image:
    """Segment an image."""
    img = Image.open(path)

    output = model_predictions(img)
    boxes, labels, scores = filter(output)

    return segmented_image(np.array(img), boxes, labels, scores)
