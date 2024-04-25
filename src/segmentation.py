from PIL import Image
import torchvision

def segmentation():
    path = 'St5FF-zqLHE.jpg'
    img = Image.open(path)
    
    warnings.filterwarnings("ignore")
    pretrained_model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
    pretrained_model = pretrained_model.eval().cpu()

    img_tensor = torchvision.transforms.functional.to_tensor(img).cpu()
    output = pretrained_model([image_tensor])[0]

