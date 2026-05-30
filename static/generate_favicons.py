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

    # 3. Calculate the centroid of the main circle of the Q (defined as original x < 36)
    # The crop starts at bbox[0], so the circle limit in cropped coordinates is 36 - bbox[0]
    circle_limit = 36 - bbox[0]
    cropped_pixels = q_cropped.load()

    sum_x, sum_y, count = 0, 0, 0
    for y_c in range(h):
        for x_c in range(w):
            r_c, g_c, b_c, a_c = cropped_pixels[x_c, y_c]
            # Consider pixels with significant opacity for centroid calculation
            if a_c > 50 and x_c < circle_limit:
                sum_x += x_c
                sum_y += y_c
                count += 1

    if count > 0:
        centroid_x = sum_x / count
        centroid_y = sum_y / count
    else:
        # Fallback to visual center if circle not segmented
        centroid_x = w / 2.0
        centroid_y = h / 2.0

    # 4. Create a square canvas where the Q's circle centroid is perfectly in the center.
    # To prevent any part of the image from being clipped, the radius of the canvas
    # must be at least the maximum distance from the centroid to any of the image boundaries.
    max_dist = max(
        centroid_x,
        w - centroid_x,
        centroid_y,
        h - centroid_y
    )
    C = int(max_dist * 2) + 4  # Perfect square canvas dimension

    centered_canvas = Image.new('RGBA', (C, C), (0, 0, 0, 0))
    offset_x = int(C / 2 - centroid_x)
    offset_y = int(C / 2 - centroid_y)
    centered_canvas.paste(q_cropped, (offset_x, offset_y))

    # 5. Add 12% padding for visual breathing room and professional floating appearance
    padding = int(C * 0.12)
    padded_dim = C + padding * 2
    q_final = Image.new('RGBA', (padded_dim, padded_dim), (0, 0, 0, 0))
    q_final.paste(centered_canvas, (padding, padding))

    # Determine Resampling filter (compatibility across PIL versions)
    try:
        resample_filter = Image.Resampling.LANCZOS
    except AttributeError:
        resample_filter = Image.LANCZOS

    # 6. Generate and save the icons
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
