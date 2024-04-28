from diffusers import StableDiffusionPipeline
import torch
import numpy as np

class StableDiffusion():
    def __init__(self, prompt):
        self.prompt = prompt + "4k, award-winning"
        self.negative_prompt = "blurry, grainy, text, lowres, low quality, ugly, morbid, mutilated, poorly drawn hands, poorly drawn face, watermark, username, signature"
        self.model_id = "runwayml/stable-diffusion-v1-5"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    
    def get_image(self):

        self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, torch_dtype=torch.float16, variant="fp16")
        self.pipe = self.pipe.to("cuda")

        self.gen_image = self.pipe(self.prompt, negative_prompt=self.negative_prompt).images[0]
        self.gen_image.save(f"assets/genai/{self.prompt}.png")
        
        return self.gen_image