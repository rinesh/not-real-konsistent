# Not-Real-Konsistent: Consistent Character Video Generator

Generate realistic videos with consistent character preservation. This Replicate model specializes in maintaining character and object consistency from reference images while creating authentic-looking animated videos. Perfect for creating videos where character identity needs to remain consistent throughout.

## 🎯 What it does

This model excels at creating realistic videos while maintaining character consistency:
1. **Consistent Character Generation**: When provided with a reference image, the model preserves character identity and features throughout the video
2. **Flexible Scene Creation**: Generates new scenes and actions while keeping characters/objects consistent
3. **Realistic Animation**: Transforms images into natural-looking videos with authentic motion

## 🚀 Try it Online

**Live Model**: https://replicate.com/rinesh/not-real-konsistent

## ✨ Features

- **Character Consistency**: 
  - Maintains character/object identity from reference images
  - Preserves key features and attributes throughout the video
  - Perfect for creating consistent character animations
- **Customizable Output**:
  - Duration: 5 or 10 second videos
  - Resolution: 480p or 1080p
  - Aspect Ratios: Multiple formats (16:9, 9:16, 1:1, 4:3, etc.)
- **Dual Output**: Get both the generated image and video
- **Automatic Authentication**: No API tokens needed when using on Replicate

## 📝 Input Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `input_image` | File | Optional reference image for character/object consistency | None |
| `prompt` | String | Describe the scene/action (character consistency maintained from reference) | Required |
| `duration` | Integer | Video length in seconds (5 or 10) | 5 |
| `resolution` | String | Video quality (480p or 1080p) | 1080p |
| `aspect_ratio` | String | Video format (16:9, 9:16, 1:1, etc.) | 16:9 |

## 🎬 Example Usage

### Using Replicate Website
Visit https://replicate.com/rinesh/not-real-konsistent and use the web interface.

### Using API
```python
import replicate

output = replicate.run(
    "rinesh/not-real-konsistent:latest",
    input={
        "prompt": "a serene mountain landscape at sunset",
        "duration": 10,
        "resolution": "1080p",
        "aspect_ratio": "16:9"
    }
)
```

### Using cog CLI
```bash
# Generate video from text only
cog predict -i prompt="birthday party celebration"

# Use reference image
cog predict -i input_image=@photo.jpg -i prompt="make it look vintage"

# Custom settings
cog predict -i prompt="ocean waves" -i duration=10 -i resolution="1080p" -i aspect_ratio="9:16"
```

## 🛠️ Technical Details

### Models Used
- **FLUX 1.1 Pro**: Text-to-image generation
- **FLUX Kontext Pro**: Image editing with text guidance
- **SeeDANCE 1 Pro**: Image-to-video animation

### Architecture
- Built as a Replicate pipeline model
- Runs on CPU infrastructure
- Automatic model chaining with authentication
- Returns both intermediate image and final video

## 🏃 Local Development

### Prerequisites
- Python 3.11+
- Docker Desktop
- Replicate account and API token

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/not-real-konsistent.git
cd not-real-konsistent

# Install dependencies
pip install -r requirements-local.txt

# Set your Replicate API token
export REPLICATE_API_TOKEN="your_token_here"

# Run local test server
python app.py
```

### Testing with cog
```bash
# Test locally with cog
cog predict --use-replicate-token \
  -i prompt="test video" \
  -i duration=5
```

## 📦 Deployment

### Deploy to Replicate
```bash
# Login to Replicate
cog login

# Push as pipeline model
cog push --x-pipeline r8.im/yourusername/your-model-name
```

### Important Notes
- Must deploy as pipeline model (`--x-pipeline` flag)
- Requires `replicate>=1.1.0b1,<2.0.0a1`
- CPU-only execution
- Cannot overwrite existing non-pipeline models

## 📄 License

This project is licensed under the MIT License. See the models' individual licenses:
- FLUX models: Check Black Forest Labs licensing
- SeeDANCE: Check ByteDance licensing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues or questions:
- Create an issue on GitHub
- Contact through Replicate platform
- See CLAUDE.md for development notes
