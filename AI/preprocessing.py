# this file is for handling all of the preprocssing

from PIL import Image
from torchvision.transforms import transforms
import torch
import numpy as np
import base64
from io import BytesIO


class Preprocessing:
    device = torch.device("cpu")
    image_transforms_test = transforms.Compose([
        # merubah ukuran gambar menjadi 256px * 256px
        transforms.Resize((256, 256)),
        # memutar gambar secara horizontal yang diberikan secara acak dengan probabilitas tertentu.
        transforms.RandomHorizontalFlip(),
        # konversi gambar menjadi tensor
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    def __init__(self, img_name):
        self.img_name = img_name

    def load_image(self):

        image = Image.open(
            BytesIO(base64.b64decode(self.img_name))).convert('RGB')
        # image = Image.open(self.img_name)
        image = self.image_transforms_test(image).float()
        image = image.to(self.device)
        self.image = image.unsqueeze(0)
        # return self.image

    @property
    def real_image(self):
        return self.img_name

    @property
    def get_image_(self):
        return self.image
