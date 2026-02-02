"""

import numpy as np
from PIL import Image, ImageDraw
import random

def generate_synthetic_fingerprint(width=300, height=300):
    # Create a white background
    image = Image.new('L', (width, height), color=255)
    draw = ImageDraw.Draw(image)
    
    # Generate fingerprint-like ridges
    for y in range(0, height, 3):
        # Randomize ridge curvature and spacing
        amplitude = random.randint(5, 20)
        frequency = random.uniform(0.05, 0.2)
        
        for x in range(width):
            # Create wavy lines to simulate ridge patterns
            offset = int(amplitude * np.sin(frequency * x))
            
            # Draw thin dark lines representing ridges
            if random.random() > 0.7:
                draw.line([(x, y + offset), (x, y + offset + 2)], fill=50)
    
    return image

# Generate sample fingerprints
def create_sample_fingerprints():
    # Create fingerprints for user IDs
    user_ids = ['1001', '1002', '1003', '1004','1005']
    
    for user_id in user_ids:
        fingerprint = generate_synthetic_fingerprint()
        filename = f'fingerprints/{user_id}.BMP'
        
        # Ensure fingerprints directory exists
        import os
        os.makedirs('fingerprints', exist_ok=True)
        
        # Save image
        fingerprint.save(filename)
        print(f"Generated {filename}")

# Run the generation
if __name__ == '__main__':
    create_sample_fingerprints()
    
"""