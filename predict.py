# Prediction interface for Cog ⚙️
# https://cog.run/python

from cog import BasePredictor, Input, Path
from typing import List
import replicate
import random
import os
import tempfile


class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        # Initialize Replicate client
        # When running on Replicate infrastructure, authentication is automatic
        # When running locally, you need to set REPLICATE_API_TOKEN environment variable
        try:
            self.client = replicate.Client()
        except Exception:
            # For local testing, ensure REPLICATE_API_TOKEN is set
            api_token = os.environ.get("REPLICATE_API_TOKEN")
            if api_token:
                self.client = replicate.Client(api_token=api_token)
            else:
                self.client = None
        self.temp_dir = tempfile.mkdtemp()

    def predict(
        self,
        prompt: str = Input(description="Text prompt for image generation"),
        input_image: Path = Input(description="Optional input image for editing", default=None),
        duration: int = Input(description="Video duration in seconds", choices=[5, 10], default=5),
        resolution: str = Input(choices=["480p", "1080p"], default="1080p"),
        aspect_ratio: str = Input(choices=["1:1", "16:9", "4:3", "3:4", "9:16", "21:9"], default="16:9"),
    ) -> List[Path]:
        """Generate an image and video using the real-me pipeline"""
        
        # Check if client is initialized
        if self.client is None:
            raise Exception(
                "Replicate client not initialized. "
                "When running locally, set REPLICATE_API_TOKEN environment variable. "
                "When deployed to Replicate, authentication is automatic."
            )
        
        # Generate random number for IMG filename
        random_num = random.randint(0, 999)
        formatted_prompt = f"IMG_{random_num:03d}.JPG: {prompt}"
        
        try:
            # Step 1: Generate or edit image
            if input_image:
                print(f"Using FLUX Kontext Pro for image editing...")
                image_output = self.client.run(
                    "black-forest-labs/flux-kontext-pro",
                    input={
                        "prompt": formatted_prompt,
                        "input_image": input_image,
                        "aspect_ratio": aspect_ratio,
                    }
                )
            else:
                print(f"Using FLUX 1.1 Pro for image generation...")
                image_output = self.client.run(
                    "black-forest-labs/flux-1.1-pro",
                    input={
                        "prompt": formatted_prompt,
                        "aspect_ratio": aspect_ratio,
                    }
                )
            
            # Save the intermediate image
            image_path = os.path.join(self.temp_dir, f"image_{random_num}.png")
            with open(image_path, "wb") as f:
                f.write(image_output[0].read())
            
            # Step 2: Generate video
            print(f"Using SeeDANCE for video generation...")
            video_output = self.client.run(
                "bytedance/seedance-1-pro",
                input={
                    "image": open(image_path, "rb"),
                    "prompt": "aggressively mediocre home footage",
                    "duration": duration,
                    "resolution": resolution,
                    "aspect_ratio": aspect_ratio,
                }
            )
            
            # Save the video
            video_path = os.path.join(self.temp_dir, f"video_{random_num}.mp4")
            with open(video_path, "wb") as f:
                f.write(video_output[0].read())
            
            # Return both image and video paths
            return [Path(image_path), Path(video_path)]
            
        except Exception as e:
            raise Exception(f"Error in real-me pipeline: {str(e)}")
