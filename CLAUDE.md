# Real-Me Model Development Notes

## Project Overview
This is a Replicate pipeline model that creates realistic videos by combining image generation/editing with video animation. The model uses a three-stage pipeline to transform text descriptions (and optionally reference images) into authentic-looking videos.

## Architecture

### Pipeline Components
1. **Image Generation/Editing Stage**
   - **FLUX 1.1 Pro**: Generates new images from text prompts when no reference image is provided
   - **FLUX Kontext Pro**: Edits/transforms existing images based on text prompts when a reference image is uploaded
   
2. **Video Generation Stage**
   - **SeeDANCE 1 Pro**: Animates the generated/edited image into a video with "aggressively mediocre home footage" aesthetic

3. **Output Format**
   - Returns both the intermediate image and final video for download
   - Image output is useful for debugging and as a preview

### Technical Implementation
- Built as a Replicate pipeline model using `replicate.use()` pattern
- Runs on CPU infrastructure (pipeline models requirement)
- Uses Python 3.13 with minimal dependencies
- Automatic authentication when deployed to Replicate

## Key Design Decisions

### Input Ordering
- `input_image` comes first to emphasize its importance as an optional reference
- `prompt` describes what image to create or how to modify the reference
- Video parameters (duration, resolution, aspect_ratio) come after content inputs

### Prompt Formatting
- User prompts are prefixed with `IMG_XXX.JPG:` to simulate camera photo filenames
- This helps create more authentic-looking results
- Random 3-digit numbers (000-999) for variety

### Fixed Video Style
- The SeeDANCE prompt is hardcoded as "aggressively mediocre home footage"
- This maintains consistent video aesthetic regardless of user input
- User prompt only affects image generation, not video style

## Deployment Configuration

### Pipeline Model Requirements
- Must use `replicate.use()` at global scope (not inside class methods)
- CPU-only execution (`gpu: false` in cog.yaml)
- Specific replicate version: `replicate>=1.1.0b1,<2.0.0a1`
- No custom base image support for Python 3.13

### Authentication
- Automatic authentication when running on Replicate infrastructure
- No need for users to provide API tokens
- Uses Replicate's internal authentication for calling other models

## Common Issues and Solutions

### URLPath Handling
- Pipeline models return `URLPath` objects, not raw file data
- Must use `open(url_path, "rb")` to read file contents
- Handle both single objects and lists for compatibility

### Optional Inputs
- Use `Path | None` type annotation for optional file inputs
- Must include `default=None` in Input() declaration
- Replicate UI will correctly show as optional

### Model Naming
- Pipeline models cannot replace existing regular models
- Must create new model or delete existing one first
- Use descriptive names that indicate pipeline nature

## Testing and Development

### Local Testing
```bash
# Install dependencies
pip install -r requirements-local.txt

# Run Flask test server
python app.py

# Test with cog (requires REPLICATE_API_TOKEN)
cog predict --use-replicate-token -i prompt="test"
```

### Deployment Commands
```bash
# Login to Replicate
cog login

# Deploy as pipeline model
cog push --x-pipeline r8.im/username/model-name
```

## Future Improvements
- Add style parameter to control video aesthetic
- Support batch processing for multiple videos
- Add more sophisticated prompt engineering
- Consider adding watermark removal/addition options
- Implement progress callbacks for long operations