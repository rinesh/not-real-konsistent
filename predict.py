# Prediction interface for Cog ⚙️
# https://cog.run/python

from cog import BasePredictor, Input, Path
from typing import List
import replicate
import random
import os
import tempfile

# Initialize Replicate models using the new pipeline model pattern
# Authentication is automatic when running on Replicate infrastructure
flux_kontext_pro = replicate.use("black-forest-labs/flux-kontext-pro")
flux_pro = replicate.use("black-forest-labs/flux-1.1-pro")
seedance = replicate.use("bytedance/seedance-1-pro")


class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        self.temp_dir = tempfile.mkdtemp()

    def predict(
        self,
        input_image: Path | None = Input(description="Optional: Upload a reference image to guide the image generation/editing process", default=None),
        prompt: str = Input(description="Describe the image you want to create or how to modify your reference image (this creates the base image that will be animated into video)"),
        duration: int = Input(description="Length of the generated video", choices=[5, 10], default=5),
        resolution: str = Input(description="Video quality - choose higher for better detail", choices=["480p", "1080p"], default="1080p"),
        aspect_ratio: str = Input(description="Video format - use 16:9 for landscape, 9:16 for mobile/portrait", choices=["1:1", "16:9", "4:3", "3:4", "9:16", "21:9"], default="16:9"),
    ) -> List[Path]:
        """Create realistic videos by first generating/editing an image from your description, then animating it into video"""
        
        # Generate random number for IMG filename
        random_num = random.randint(0, 999)
        formatted_prompt = f"IMG_{random_num:03d}.JPG: {prompt}"
        
        try:
            # Step 1: Generate or edit image
            if input_image:
                print(f"Using FLUX Kontext Pro for image editing...")
                image_output = flux_kontext_pro(
                    prompt=formatted_prompt,
                    input_image=input_image,
                    aspect_ratio=aspect_ratio,
                )
            else:
                print(f"Using FLUX 1.1 Pro for image generation...")
                image_output = flux_pro(
                    prompt=formatted_prompt,
                    aspect_ratio=aspect_ratio,
                )
            
            # Save the intermediate image
            image_path = os.path.join(self.temp_dir, f"image_{random_num}.png")
            with open(image_path, "wb") as f:
                # Handle both list and single URLPath outputs
                if isinstance(image_output, list):
                    with open(image_output[0], "rb") as img_file:
                        f.write(img_file.read())
                else:
                    with open(image_output, "rb") as img_file:
                        f.write(img_file.read())
            
            # Step 2: Generate video
            print(f"Using SeeDANCE for video generation...")
            video_output = seedance(
                image=open(image_path, "rb"),
                prompt="aggressively mediocre home footage",
                duration=duration,
                resolution=resolution,
                aspect_ratio=aspect_ratio,
            )
            
            # Save the video
            video_path = os.path.join(self.temp_dir, f"video_{random_num}.mp4")
            with open(video_path, "wb") as f:
                # Handle both list and single URLPath outputs
                if isinstance(video_output, list):
                    with open(video_output[0], "rb") as vid_file:
                        f.write(vid_file.read())
                else:
                    with open(video_output, "rb") as vid_file:
                        f.write(vid_file.read())
            
            # Return both image and video paths
            return [Path(image_path), Path(video_path)]
            
        except Exception as e:
            raise Exception(f"Error in real-me pipeline: {str(e)}")
