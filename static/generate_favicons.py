import os
from PIL import Image

def main():
    logo_path = 'static/qualia-logo.png'
    if not os.path.exists(logo_path):
        print(f"Error: {logo_path} not found.")
        return

    logo = Image.open(logo_path)
    
    # 1. Get active bounding box of the original logo to crop any empty margins
    bbox = logo.getbbox()
    if not bbox:
        print("Error: Bounding box not found.")
        return
    cropped = logo.crop(bbox)
    cw, ch = cropped.size

    # 2. Frame in a perfect high-resolution square canvas (512x512)
    C = 512
    # First, scale the cropped image so that its width fits the C canvas
    scale_factor = C / cw
    new_w = C
    new_h = int(ch * scale_factor)
    
    # Determine Resampling filter (compatibility across PIL versions)
    try:
        resample_filter = Image.Resampling.LANCZOS
    except AttributeError:
        resample_filter = Image.LANCZOS

    logo_scaled = cropped.resize((new_w, new_h), resample_filter)

    # Place in the center of the 512x512 square canvas
    square_logo = Image.new('RGBA', (C, C), (0, 0, 0, 0))
    offset_y = (C - new_h) // 2
    square_logo.paste(logo_scaled, (0, offset_y))

    # Save the master square logo
    square_logo_path = 'static/qualia-logo-square.png'
    square_logo.save(square_logo_path, 'PNG')
    print(f"Generated and saved {square_logo_path} successfully!")

    # 3. Generate and save the favicons from this perfect original master square logo
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
