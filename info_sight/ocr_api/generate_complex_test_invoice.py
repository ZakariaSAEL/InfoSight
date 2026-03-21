from PIL import Image, ImageDraw, ImageFont
import os

def create_complex_test_invoice():
    # Create a white canvas
    img = Image.new('RGB', (1000, 1200), color='white')
    d = ImageDraw.Draw(img)
    
    # Text with intentional abbreviation and capitalization errors to test Gemini normalization
    text = """
    *** INVOICE / FACTURE ***
    Reference: #ERR-999
    Date de facturation: 21-03-2026
    
    EXPEDITEUR (VENDOR):
    maroc global tech s.a.r.l
    125, AV des F.A.R, IMM. ATLAS
    4eme etage, APP 42
    20000 CASABLANCA
    MA
    
    DESTINATAIRE (CLIENT):
    STE NOVA SERVICES
    45 Bvd de la resistance
    RES les fleurs, Bloc C
    qrt industriel
    TANGER, MAROC
    
    DESCRIPTION                          TOTAL
    ------------------------------------------
    Maintenance Serveur Cloud            1500 MAD
    Licence Annuelle (Promo)              800 MAD
    
    TOTAL TTC: 2300 MAD
    
    Notes: 
    Paiement par virement à la Rte de Rabat.
    Z.I. Gzenaya
    """
    
    try:
        # Try to use a clean font if available on windows
        font_path = "C:\\Windows\\Fonts\\arial.ttf"
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, 32)
        else:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()
        
    d.text((60, 60), text, fill="black", font=font)
    
    save_path = 'complex_test_invoice.png'
    img.save(save_path)
    print(f"Created {save_path}")
    return os.path.abspath(save_path)

if __name__ == "__main__":
    create_complex_test_invoice()
