import os
from PIL import Image

def main():
    logo_path = 'static/qualia-logo.png'
    if not os.path.exists(logo_path):
        print(f"Error: {logo_path} not found.")
        return

    logo = Image.open(logo_path)
    width, height = logo.size
    pixels = logo.load()

    # 1. Segment orange pixels for the Q and its tail (limit to x < 52)
    max_x = 52
    fade_start = 42
    q_canvas = Image.new('RGBA', (max_x, height), (0, 0, 0, 0))
    q_pixels = q_canvas.load()

    for y in range(height):
        for x in range(max_x):
            if x < width:
                r, g, b, a = pixels[x, y]
                # Segment orange vs gray
                dist_orange = (r - 243)**2 + (g - 152)**2 + (b - 0)**2
                dist_gray = (r - 123)**2 + (g - 122)**2 + (b - 119)**2
                if a > 0 and dist_orange < dist_gray:
                    # Apply a smooth horizontal fade-out for x >= fade_start to taper the tail
                    if x >= fade_start:
                        factor = 1.0 - (x - fade_start) / (max_x - fade_start)
                        new_a = int(a * factor)
                    else:
                        new_a = a
                    
                    if new_a > 0:
                        q_pixels[x, y] = (r, g, b, new_a)

    # 2. Crop to the active bounding box
    bbox = q_canvas.getbbox()
    if not bbox:
        print("Error: Failed to find Q shape in segmentation.")
        return
    q_cropped = q_canvas.crop(bbox)
    w, h = q_cropped.size

    # 3. Calculate circle dimensions inside q_cropped
    # The circle's bounding box in original logo is x: [0, 36], y: [11, 72].
    # bbox[0] and bbox[1] are the top-left of q_cropped.
    circle_w = 36 - bbox[0]
    circle_h = 72 - bbox[1]

    # 4. Create a square canvas where the Q's circle body is maximized and perfectly centered.
    # We choose C = 64 to ensure the circle body occupies ~95% of the canvas height (very large and prominent).
    C = 64
    q_final = Image.new('RGBA', (C, C), (0, 0, 0, 0))

    # Center the circle in the canvas
    offset_x = (C - circle_w) // 2
    offset_y = (C - circle_h) // 2

    # Paste the cropped image at the offset (allowing the tail to extend and fade beautifully at the boundaries)
    q_final.paste(q_cropped, (offset_x, offset_y))

    # Determine Resampling filter (compatibility across PIL versions)
    try:
        resample_filter = Image.Resampling.LANCZOS
    except AttributeError:
        resample_filter = Image.LANCZOS

    # 5. Generate and save the icons
    # 16x16 PNG
    fav_16 = q_final.resize((16, 16), resample_filter)
    fav_16.save('static/favicon-16x16.png', 'PNG')
    print("Saved static/favicon-16x16.png")

    # 32x32 PNG
    fav_32 = q_final.resize((32, 32), resample_filter)
    fav_32.save('static/favicon-32x32.png', 'PNG')
    print("Saved static/favicon-32x32.png")

    # Apple Touch Icon (180x180 PNG)
    apple_icon = q_final.resize((180, 180), resample_filter)
    apple_icon.save('static/apple-touch-icon.png', 'PNG')
    print("Saved static/apple-touch-icon.png")

    # Multi-size ICO (16x16, 32x32, 48x48)
    fav_padded_for_ico = q_final.resize((256, 256), resample_filter)
    fav_padded_for_ico.save(
        'static/favicon.ico',
        format='ICO',
        sizes=[(16, 16), (32, 32), (48, 48)]
    )
    print("Saved static/favicon.ico")

if __name__ == '__main__':
    main()
