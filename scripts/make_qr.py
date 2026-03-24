import qrcode
from PIL import Image, ImageDraw, ImageFont

def generate_qr(
    data,
    logo_path,
    output_path='qr_with_solid_halo.png',
    qr_box_size=15,
    qr_border=4,
    qr_fill_color='black',
    logo_scale=0.25,
    halo_thickness=1,
    halo_color=(255, 255, 255, 255),  # Solid white
    font_path='',
    font_size=28,
    bottom_text='',
    padding=10
):
    # Step 1: Create QR code
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=qr_box_size,
        border=qr_border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=qr_fill_color, back_color='white').convert('RGBA')

    # Step 2: Load and resize logo
    logo = Image.open(logo_path).convert("RGBA")
    qr_width, qr_height = qr_img.size
    logo_size = int(min(qr_width, qr_height) * logo_scale)
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    # Step 3: Create solid halo (circle)
    halo_size = logo_size + 2 * halo_thickness
    halo_img = Image.new("RGBA", (halo_size, halo_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(halo_img)
    draw.ellipse((0, 0, halo_size, halo_size), fill=halo_color)

    # Step 4: Composite halo + logo
    combined = Image.new("RGBA", (halo_size, halo_size), (0, 0, 0, 0))
    combined.paste(halo_img, (0, 0), halo_img)
    combined.paste(logo, (halo_thickness, halo_thickness), logo)

    # Step 5: Paste onto QR code
    pos = ((qr_width - halo_size) // 2, (qr_height - halo_size) // 2)
    qr_img.paste(combined, pos, combined)

    # Step 6: Prepare text layer
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
        print("⚠️ Could not load specified font. Using default.")

    # Use a temporary draw object to measure text
    temp_img = Image.new("RGB", (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    bbox = temp_draw.textbbox((0, 0), bottom_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Now create image for the text
    text_img = Image.new("RGBA", (qr_width, text_height + padding * 2), (255, 255, 255, 255))
    text_draw = ImageDraw.Draw(text_img)
    text_draw.text(
        ((qr_width - text_width) // 2, padding - text_height),
        bottom_text,
        fill=(0, 0, 0, 255),
        font=font
    )

    # Step 7: Combine QR + text
    total_height = qr_height + text_img.height
    final_img = Image.new("RGBA", (qr_width, total_height), (255, 255, 255, 255))
    final_img.paste(qr_img, (0, 0))
    final_img.paste(text_img, (0, qr_height))

    # Step 8: Save result
    final_img.save(output_path)
    print(f"QR code with halo and text saved to: {output_path}")

# Example usage
font_path = '../www/assets/fonts/PermanentMarker-Regular.ttf'
generate_qr(
    data='gnarnana.com/assets/gnarnana.json',
    logo_path="../www/assets/imgs/gnarnana_logo_800x800.png",
    output_path="qr_json.png",
    qr_fill_color='#df1072',
    bottom_text='Race Info JSON',
    font_path=font_path
)
generate_qr(
    data='gnarnana.com/assets/gnarnana.kml',
    logo_path="../www/assets/imgs/gnarnana_logo_800x800.png",
    output_path="qr_kml.png",
    bottom_text='Race Info KML',
    font_path=font_path,
    qr_fill_color='#00b0db'
)
