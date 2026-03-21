from PIL import Image, ImageDraw, ImageFont
import os

def create_multilingual_test_invoice():
    # Create a white canvas
    img = Image.new('RGB', (1000, 1200), color='white')
    d = ImageDraw.Draw(img)
    
    # Text with French, Arabic, and English
    # Note: Traditional PIL has trouble with Arabic RTL/shaping without complex libraries, 
    # but for a synthetic OCR test, we can just put the characters.
    # We will use common Moroccan terms.
    
    text = """
    *** INVOICE / FACTURE / فاتورة ***
    No: #MULTI-2026
    Date: 21-03-2026
    
    Vendeur:
    AL AMAL TECH (شركة الأمل للتقنية)
    15 Rue de la Liberté (شارع الحرية)
    Quartier Maârif, Casablanca
    
    Billed To:
    John Doe Services
    45 Av el harrouchi
    Z.I. Ain Sebaa
    Casablanca, Morocco
    
    Details:
    1x Digital Consulting - 3000 DH
    1x الدعم الفني (Technical Support) - 1000 DH
    
    Total: 4000 MAD
    """
    
    try:
        # Use a font that supports Arabic if possible, or fallback
        # On Windows, 'Arial' or 'Times New Roman' usually support Arabic
        font_path = "C:\\Windows\\Fonts\\arial.ttf"
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, 32)
        else:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()
        
    d.text((60, 60), text, fill="black", font=font)
    
    save_path = 'multilingual_test_invoice.png'
    img.save(save_path)
    print(f"Created {save_path}")
    return os.path.abspath(save_path)

if __name__ == "__main__":
    create_multilingual_test_invoice()
