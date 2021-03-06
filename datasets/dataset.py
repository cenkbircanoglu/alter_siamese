import random

import PIL.ImageOps
import numpy as np
from PIL import Image
from torch.utils.data import Dataset

random.seed(1137)
np.random.seed(1137)


class NetworkDataset(Dataset):
    def __init__(self, image_folder_dataset, transform=None, should_invert=True, channel=1, train=True, val=False):
        self.train = train
        if self.train:
            random.shuffle(image_folder_dataset.imgs)
        self.image_folder_dataset = image_folder_dataset
        self.transform = transform
        self.should_invert = should_invert
        self.channel = channel

        self.num_inputs = 1
        self.num_targets = 1
        self.labels = [x[1] for x in image_folder_dataset.imgs]

    def get_items(self, index):
        img0_tuple = self.image_folder_dataset.imgs[index]
        # we need to make sure approx 50% of images are in the same class

        img0 = Image.open(img0_tuple[0])
        if self.channel == 1:
            img0 = img0.convert("L")
        elif self.channel == 3:
            img0 = img0.convert("RGB")

        if self.should_invert:
            img0 = PIL.ImageOps.invert(img0)

        if self.transform is not None:
            img0 = self.transform(img0)
        return img0, img0_tuple[1]

    def __getitem__(self, index):
        if self.train:
            return self.get_items(index)
        return self.get_items(index)

    def __len__(self):
        return len(self.image_folder_dataset.imgs)
