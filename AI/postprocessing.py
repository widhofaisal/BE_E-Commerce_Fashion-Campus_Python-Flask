import torch
import torchvision


def postpreprocessing(self):
    dict_map = {
        0: "T-shirt",
        1: "Trouser",
        2: "Pullover",
        3: "Dress",
        4: "Coat",
        5: "Sandals",
        6: "Shirt",
        7: "Sneaker",
        8: "Bag",
        9: "Ankle Boot",
        10: "Hat"
    }
    label = dict_map[self.result.tolist()[0]]
    self._label = label

    @property
    def get_results(self):
        return self._label
