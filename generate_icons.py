#!/usr/bin/env python3
"""
Generate PWA icons from SVG source
Requires: cairosvg (pip install cairosvg)
"""

import os
import sys
try:
    import cairosvg
except ImportError:
    print("Error: cairosvg not installed. Please install with: pip install cairosvg")
    print("Or use another tool to convert the SVG to PNG in the required sizes.")
    sys.exit(1)

# Icon sizes needed for PWA
ICON_SIZES = [72, 96, 128, 144, 152, 192, 384, 512]

def generate_icons():
    """Generate PNG icons from SVG source"""
    # Ensure the icons directory exists
    os.makedirs("static/icons", exist_ok=True)
    
    # Check if the source SVG exists
    svg_path = "static/icons/icon-192x192.svg"
    if not os.path.exists(svg_path):
        print(f"Error: Source SVG not found at {svg_path}")
        return
    
    # Generate icons for each size
    for size in ICON_SIZES:
        output_path = f"static/icons/icon-{size}x{size}.png"
        try:
            cairosvg.svg2png(url=svg_path, write_to=output_path, output_width=size, output_height=size)
            print(f"Generated: {output_path}")
        except Exception as e:
            print(f"Error generating {output_path}: {e}")

if __name__ == "__main__":
    print("Generating PWA icons...")
    generate_icons()
    print("Done!")