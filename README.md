# real-me

A composite AI model that generates realistic "home footage" style videos by combining image generation and video synthesis.

## What it does

This model creates authentic-looking amateur video footage by:
1. Generating or editing images using FLUX models
2. Converting them to videos with a distinctive "aggressively mediocre home footage" aesthetic

## Features

- **Conditional Image Processing**: 
  - Without input image: Uses FLUX 1.1 Pro for generation
  - With input image: Uses FLUX Kontext Pro for editing
- **Customizable Duration**: Choose between 5 or 10 second videos
- **Resolution Options**: 480p or 1080p output
- **Aspect Ratios**: 16:9 or 9:16 format
- **Unique Naming**: Each image gets a random "IMG_0XXX.JPG" prefix

## Example Usage

```bash
# Generate a 5-second video from scratch
cog predict -i prompt="sunset"

# Create a 10-second video with custom settings
cog predict -i prompt="ocean waves" -i duration=10 -i resolution="1080p"

# Edit an existing image into video
cog predict -i prompt="retro filter" -i input_image=@photo.jpg -i duration=10
```

## Models Used

- **FLUX 1.1 Pro**: For image generation from scratch
- **FLUX Kontext Pro**: For image editing when input image provided
- **SeeDANCE 1 Pro**: For video generation with home footage aesthetic
