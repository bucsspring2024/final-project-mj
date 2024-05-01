from diffusers import StableDiffusionPipeline, AutoencoderKL
import torch
import numpy as np
import platform

class StableDiffusion():
    def __init__(self, prompt):
        self.prompt = prompt + " 4k, award-winning"
        self.negative_prompt = "blurry, grainy, text, lowres, low quality, ugly, morbid, mutilated, poorly drawn hands, poorly drawn face, watermark, username, signature"
        self.model_id = "runwayml/stable-diffusion-v1-5"
        self.device = "mps" if platform.system() == "Darwin" else "cuda" if torch.cuda.is_available() else "cpu"
    
    
    def get_image(self):
        self.vae = AutoencoderKL.from_pretrained("madebyollin/sdxl-vae-fp16-fix", torch_dtype=torch.float16)
        self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, vae=self.vae, torch_dtype=torch.float16, safety_checker=None, requires_safety_checker=False)
        self.pipe = self.pipe.to(self.device)
        self.pipe.enable_attention_slicing()
        
        # Macs are slower, so reducing inference steps / dimensions to speed up the process at cost of quality
        if platform.system() == "Darwin":
            self.gen_image = self.pipe(self.prompt, negative_prompt=self.negative_prompt, height=256, width=256, num_inference_steps=25).images[0]
        else:
            self.gen_image = self.pipe(self.prompt, negative_prompt=self.negative_prompt).images[0]
        
        # self.gen_image.save(f"assets/genai/{self.prompt}.png")
        
        return self.gen_image