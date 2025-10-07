# pip install qrcode[pil] pillow

import os
import qrcode
from urllib.parse import urlsplit, urlunsplit
import qrcode.image.svg as qsvg

def normalize_url(url: str) -> str:
    """Dodaj https:// ako nedostaje i vrati očišćen URL."""
    url = url.strip()
    parts = urlsplit(url)
    if not parts.scheme:
        parts = parts._replace(scheme="https")
    return urlunsplit(parts)

def make_qr(url: str, out_dir: str = "outputs"):
    """Generira QR kod za zadani URL i sprema PNG i SVG verzije."""
    url = normalize_url(url)

    # napravi folder ako ne postoji
    os.makedirs(out_dir, exist_ok=True)

    # kreiraj imena datoteka prema URL-u (sigurna imena)
    safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_")
    png_path = os.path.join(out_dir, f"{safe_name}.png")
    svg_path = os.path.join(out_dir, f"{safe_name}.svg")

    # --- PNG verzija ---
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img.save(png_path)

    # --- SVG verzija ---
    factory = qsvg.SvgImage
    svg_img = qrcode.make(url, image_factory=factory)
    svg_img.save(svg_path)

    print(f"\n✅ QR kod generiran!")
    print(f"   URL: {url}")
    print(f"   PNG: {png_path}")
    print(f"   SVG: {svg_path}\n")

if __name__ == "__main__":
    user_url = input("Unesi link koji želiš pretvoriti u QR kod: ").strip()
    if user_url:
        make_qr(user_url)
    else:
        print("⚠️ Nije unesen link.")
