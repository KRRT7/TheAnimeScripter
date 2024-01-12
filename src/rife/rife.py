import os
import torch
import numpy as np
import logging

from torch.nn import functional as F


class Rife:
    def __init__(self, interpolation_factor, half, width, height, UHD):
        self.interpolation_factor = interpolation_factor
        self.half = half
        self.UHD = UHD
        self.scale = 1.0
        self.width = int(width)
        self.height = int(height)
        self.modelDir = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "rife4_14")

        self.handle_model()

    def handle_model(self):

        if not os.path.exists(os.path.join(self.modelDir, "rife_414.pkl")):
            self.get_rife()

        # Apparently this can improve performance slightly
        torch.set_float32_matmul_precision("medium")

        if self.UHD == True:
            self.scale = 0.5

        ph = ((self.height - 1) // 64 + 1) * 64
        pw = ((self.width - 1) // 64 + 1) * 64
        self.padding = (0, pw - self.width, 0, ph - self.height)

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")

        # Doing a torch cuda check is rather expensive on start-up times so I just decided to keep it simple
        self.cuda_available = False
        torch.set_grad_enabled(False)
        if torch.cuda.is_available():
            self.cuda_available = True
            torch.backends.cudnn.enabled = True
            torch.backends.cudnn.benchmark = True
            if self.half:
                torch.set_default_tensor_type(torch.cuda.HalfTensor)

        try:
            from .rife4_14.RIFE_HDv3 import Model
        except:
            print(
                "Failed to import the Rife Model, this is probably because RIFE was not downloaded successfully, do you have internet connection?")
            logging.error(
                "Failed to import the Rife Model, do you have internet connection?")
            return

        self.model = Model()
        self.model.load_model(self.modelDir, -1)
        self.model.eval()

        if self.cuda_available == True:
            if self.half:
                self.model.half()

        self.model.device()

    def get_rife(self):
        import wget

        print("Downloading RIFE model...")
        logging.info(
            "Couldn't find RIFE model, downloading it now...")
        
        url = "https://github.com/NevermindNilas/TAS-Modes-Host/releases/download/main/rife_414.pkl"
        wget.download(url, out=os.path.join(self.modelDir, "flownet.pkl"))

    def make_inference(self, I0, I1, n):
        res = []
        for i in range(n):
            res.append(self.model.inference(
                I0, I1, (i + 1) * 1. / (n + 1), self.scale))

        return res

    def pad_image(self, img):
        img = F.pad(img, self.padding)
        return img

    @torch.inference_mode()
    def run(self, I0, I1):
        buffer = []
        I0 = torch.from_numpy(np.transpose(I0, (2, 0, 1))).to(
            self.device, non_blocking=True).unsqueeze(0).float() / 255.
        I1 = torch.from_numpy(np.transpose(I1, (2, 0, 1))).to(
            self.device, non_blocking=True).unsqueeze(0).float() / 255.

        if self.cuda_available and self.half:
            I0 = I0.half()
            I1 = I1.half()

        if self.padding != (0, 0, 0, 0):
            I0 = self.pad_image(I0)
            I1 = self.pad_image(I1)

        output = self.make_inference(I0, I1, self.interpolation_factor - 1)

        for mid in output:
            mid = (((mid[0] * 255.).byte().cpu().numpy().transpose(1, 2, 0)))
            buffer.append(mid[:self.height, :self.width, :])

        return buffer
