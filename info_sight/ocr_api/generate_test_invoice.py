from PIL import Image, ImageDraw, ImageFont

def create_invoice():
    # Create a white canvas
    img = Image.new('RGB', (800, 1000), color='white')
    d = ImageDraw.Draw(img)
    
    # Text with intentional abbreviation and capitalization errors
    text = """
FACTURE N°: 2026-0042
Date: 19 Mars 2026
    
VENDOR: 
Tech Solutions SARL
Adresse: 14 bd anfa, 
res. les jasmins, appt 3 
casablanca, maroc
    
BILLED TO:
Client Alpha
adresse: 100 Rte de la plage, lot. al nassim
Z.I. tanger
    
ITEMS:
1x Software License - 5000 DH
1x Server Setup - 2500 DH
    
TOTAL AMOUNT: 7500 DH
"""
    
    try:
        # Try to use Arial if available on windows
        font = ImageFont.truetype("arial.ttf", 36)
    except IOError:
        font = ImageFont.load_default()
        
    d.text((50, 50), text, fill="black", font=font)
    img.save('test_invoice_real.png')
    print("Created test_invoice_real.png")

if __name__ == "__main__":
    create_invoice()
