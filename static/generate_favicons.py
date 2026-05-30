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

    # Determine Resampling filter (compatibility across PIL versions)
    try:
        resample_filter = Image.Resampling.LANCZOS
    except AttributeError:
        resample_filter = Image.LANCZOS

    # 1. Crop and segment the orange Q (x < 44, short tail with fade-out from x=36)
    q_canvas = Image.new('RGBA', (44, height), (0, 0, 0, 0))
    q_pixels = q_canvas.load()
    for y in range(height):
        for x in range(44):
            if x < width:
                r, g, b, a = pixels[x, y]
                # Segment orange vs gray
                dist_orange = (r - 243)**2 + (g - 152)**2 + (b - 0)**2
                dist_gray = (r - 123)**2 + (g - 122)**2 + (b - 119)**2
                if a > 0 and dist_orange < dist_gray:
                    if x >= 36:
                        factor = 1.0 - (x - 36) / (44 - 36)
                        new_a = int(a * factor)
                    else:
                        new_a = a
                    if new_a > 0:
                        q_pixels[x, y] = (r, g, b, new_a)

    bbox_q = q_canvas.getbbox()
    if not bbox_q:
        print("Error: Q bounding box not found.")
        return
    q_cropped = q_canvas.crop(bbox_q)

    # 2. Crop and segment the right half (x >= 36: gray 'ualia' text + orange swoosh/dots)
    right_canvas = Image.new('RGBA', (width - 36, height), (0, 0, 0, 0))
    right_pixels = right_canvas.load()
    for y in range(height):
        for x in range(36, width):
            r, g, b, a = pixels[x, y]
            if a > 0:
                right_pixels[x - 36, y] = (r, g, b, a)

    bbox_r = right_canvas.getbbox()
    if not bbox_r:
        print("Error: Right half bounding box not found.")
        return
    right_cropped = right_canvas.crop(bbox_r)

    # 3. Construct a high-resolution 256x256 square logo
    C = 256
    square_logo = Image.new('RGBA', (C, C), (0, 0, 0, 0))

    # Scale components for perfect visual balance in a square layout
    # - Q body is massive (101x140) to dominate as the hero emblem
    q_scaled = q_cropped.resize((101, 140), resample_filter)
    # - Right half (ualia + swoosh + dots) is compact (120x87) at the bottom
    r_scaled = right_cropped.resize((120, 87), resample_filter)

    # Paste components onto the square canvas
    q_x = (C - q_scaled.width) // 2
    q_y = 10
    square_logo.paste(q_scaled, (q_x, q_y))

    r_x = (C - r_scaled.width) // 2
    r_y = 10 + 140 + 8
    square_logo.paste(r_scaled, (r_x, r_y))

    # Save the master square logo
    square_logo_path = 'static/qualia-logo-square.png'
    square_logo.save(square_logo_path, 'PNG')
    print(f"Generated and saved {square_logo_path}")

    # 4. Generate and save the favicons from the master square logo
    # 16x16 PNG
    fav_16 = square_logo.resize((16, 16), resample_filter)
    fav_16.save('static/favicon-16x16.png', 'PNG')
    print("Saved static/favicon-16x16.png")

    # 32x32 PNG
    fav_32 = square_logo.resize((32, 32), resample_filter)
    fav_32.save('static/favicon-32x32.png', 'PNG')
    print("Saved static/favicon-32x32.png")

    # Apple Touch Icon (180x180 PNG)
    apple_icon = square_logo.resize((180, 180), resample_filter)
    apple_icon.save('static/apple-touch-icon.png', 'PNG')
    print("Saved static/apple-touch-icon.png")

    # Multi-size ICO (16x16, 32x32, 48x48)
    fav_padded_for_ico = square_logo.resize((256, 256), resample_filter)
    fav_padded_for_ico.save(
        'static/favicon.ico',
        format='ICO',
        sizes=[(16, 16), (32, 32), (48, 48)]
    )
    print("Saved static/favicon.ico")

if __name__ == '__main__':
    main()
