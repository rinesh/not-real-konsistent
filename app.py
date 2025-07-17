#!/usr/bin/env python3
"""
Local Flask app to test the real-me model pipeline
"""
from flask import Flask, render_template, request, jsonify, send_file
import replicate
import random
import os
import tempfile
import json
from datetime import datetime

app = Flask(__name__)

# Configure Flask
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

class RealMePredictor:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        
    def predict(self, prompt, input_image=None, duration=5, resolution="1080p", aspect_ratio="16:9", api_token=None):
        """
        Recreate the real-me model logic locally
        """
        if not api_token:
            raise Exception("API token is required")
            
        client = replicate.Client(api_token=api_token)
        
        # Generate random number for IMG filename
        random_num = random.randint(0, 999)
        formatted_prompt = f"IMG_{random_num:03d}.JPG: {prompt}"
        
        try:
            # Step 1: Generate or edit image
            if input_image:
                print(f"Using FLUX Kontext Pro for image editing...")
                image_output = client.run(
                    "black-forest-labs/flux-kontext-pro",
                    input={
                        "prompt": formatted_prompt,
                        "input_image": input_image,
                        "aspect_ratio": aspect_ratio,
                    }
                )
            else:
                print(f"Using FLUX 1.1 Pro for image generation...")
                image_output = client.run(
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
            video_output = client.run(
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
            
            return {
                "success": True,
                "image_path": image_path,
                "video_path": video_path,
                "formatted_prompt": formatted_prompt,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

# Initialize predictor
predictor = RealMePredictor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        prompt = data.get('prompt', '')
        duration = int(data.get('duration', 5))
        resolution = data.get('resolution', '1080p')
        aspect_ratio = data.get('aspect_ratio', '16:9')
        api_token = data.get('api_token', '')
        
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
            
        if not api_token:
            return jsonify({"error": "API token is required"}), 400
        
        # Run prediction
        result = predictor.predict(
            prompt=prompt,
            duration=duration,
            resolution=resolution,
            aspect_ratio=aspect_ratio,
            api_token=api_token
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict_with_image', methods=['POST'])
def predict_with_image():
    try:
        prompt = request.form.get('prompt', '')
        duration = int(request.form.get('duration', 5))
        resolution = request.form.get('resolution', '1080p')
        aspect_ratio = request.form.get('aspect_ratio', '16:9')
        api_token = request.form.get('api_token', '')
        
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
            
        if not api_token:
            return jsonify({"error": "API token is required"}), 400
        
        input_image = None
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                # Save uploaded image
                image_path = os.path.join(predictor.temp_dir, f"upload_{random.randint(0,999)}.png")
                file.save(image_path)
                input_image = open(image_path, "rb")
        
        # Run prediction
        result = predictor.predict(
            prompt=prompt,
            input_image=input_image,
            duration=duration,
            resolution=resolution,
            aspect_ratio=aspect_ratio,
            api_token=api_token
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    # Validate filename to prevent path traversal
    if '..' in filename or '/' in filename or '\\' in filename:
        return "Invalid filename", 400
    
    # Only allow specific file extensions
    allowed_extensions = {'.png', '.jpg', '.jpeg', '.mp4', '.webp'}
    if not any(filename.lower().endswith(ext) for ext in allowed_extensions):
        return "Invalid file type", 400
    
    file_path = os.path.join(predictor.temp_dir, filename)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found", 404

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    print("Starting Real-Me Model Test Server...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)