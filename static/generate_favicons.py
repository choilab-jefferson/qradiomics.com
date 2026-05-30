import os
from PIL import Image

def main():
    square_logo_path = 'static/qualia-logo-square.png'
    if not os.path.exists(square_logo_path):
        print(f"Error: {square_logo_path} not found.")
        return

    square_logo = Image.open(square_logo_path)

    # Determine Resampling filter (compatibility across PIL versions)
    try:
        resample_filter = Image.Resampling.LANCZOS
    except AttributeError:
        resample_filter = Image.LANCZOS

    # Generate and save the favicons from the clean transparent master square logo
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
