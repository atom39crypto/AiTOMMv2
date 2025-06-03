import os
import sys
from PIL import Image
from Mainframe.uploder import uploder

def generate_image(prompt, model_id="CompVis/stable-diffusion-v1-4", device="cpu"):
    print("Text _ to _ Image ", prompt)
    from diffusers import StableDiffusionPipeline
    os.environ["HF_HOME"] = "E:/image/huggingface_cache"
    os.environ["TORCH_HOME"] = "E:/image/torch_cache"
    
    pipe = StableDiffusionPipeline.from_pretrained(model_id).to(device)
    image = pipe(prompt).images[0]
    image.show()


def generate_image_from_image(input_image_path,prompt, model_id="CompVis/stable-diffusion-v1-4", device="cpu", strength=0.6):
    print("Image _ to _ Image ", prompt)
    from diffusers import StableDiffusionImg2ImgPipeline
    # Set cache paths if needed
    os.environ["HF_HOME"] = "E:/image/huggingface_cache"
    os.environ["TORCH_HOME"] = "E:/image/torch_cache"
    
    # Load the image-to-image pipeline
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id).to(device)
    pipe.enable_attention_slicing()  # Enable to reduce memory usage
    
    # Open, convert, and resize the input image
    init_image = Image.open(input_image_path).convert("RGB")
    init_image = init_image.resize((512, 512))
    
    # Generate the new image based on the input image and text prompt
    result = pipe(prompt=prompt, image=init_image, strength=strength)
    image = result.images[0]
    
    # Show the generated image
    image.show()



if __name__ == "__main__":
    prompt = sys.argv[1]
    prompt = prompt.replace("_", " ")

    print(f"--------------------------------- prompt :{prompt} -----------------------------------",)

    if "image" in prompt.lower() and any(keyword in prompt.lower() for keyword in ["alter", "modify", "change"]):
        path = uploder()
        generate_image_from_image(path, prompt)
        print(path, "image to Image")

    else:
        generate_image(prompt)
        print("Text to Image")
