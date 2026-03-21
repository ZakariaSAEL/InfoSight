from address_utils import extract_addresses
text = "Aapex Digital INVOICE Solutions Invoice #: AD-2024-0015 145 Main Street Suite 300 Invoice Date: October 26, 2024 San Francisco; CA 94105 Due Date: November 10, 2024 Cllent: Billed To: Greenlignt Innovations Sarah Chen 888 Silicon Valley Blvd Palo Ato, CA 94304 description Unit Price"
print("Extracted:")
for a in extract_addresses(text):
    print("- " + a)
