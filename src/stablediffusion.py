from diffusers import StableDiffusionPipeline
import torch
import platform

class StableDiffusion():
    def __init__(self, prompt):
        '''
        Initializes the object and Stable Diffusion model, does a little prompt engineering
        '''
        self.prompt = prompt + " 4k, award-winning"
        self.negative_prompt = "blurry, grainy, text, lowres, low quality, ugly, morbid, mutilated, poorly drawn hands, poorly drawn face, watermark, username, signature"
        self.model_id = "runwayml/stable-diffusion-v1-5"
        self.device = "mps" if platform.system() == "Darwin" else "cuda" if torch.cuda.is_available() else "cpu" # "Darwin" is Mac OS
    
    
    def get_image(self):
        '''
        Calls the Stable Diffusion model to generate an image based on the prompt
        
        Returns:
            gen_image PIL.Image: the generated image
        '''

        # Load the pipeline

        # I've been trying my hardest to get this to work on my Macbook M! 2020, but it doesn't. When I render the image, a floating point precision error occurs and the image returns as black. This doesn't happen on my Windows PC.
        # The alternative solution is to set torch_dtype=torch.float32, but this is way too slow even after reducing the inference steps and dimensions.
        self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, torch_dtype=torch.float16)
        self.pipe = self.pipe.to(self.device)
        self.pipe.enable_attention_slicing() # Performance optimization for low VRAM
        
        # Macs are slower, so reducing inference steps / dimensions to speed up the process at the cost of quality. These images look meh
        if platform.system() == "Darwin":
            self.gen_image = self.pipe(self.prompt, negative_prompt=self.negative_prompt, height=256, width=256, num_inference_steps=25).images[0]
        else:
            self.gen_image = self.pipe(self.prompt, negative_prompt=self.negative_prompt).images[0]
        
        # self.gen_image.save(f"assets/genai/{self.prompt}.png")
        
        return self.gen_image