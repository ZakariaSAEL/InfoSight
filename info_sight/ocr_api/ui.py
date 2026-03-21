import streamlit as st
import os
from ocr_model import run_ocr
from PIL import Image
import tempfile

# Set page config for a premium look
st.set_page_config(
    page_title="InfoSight - Smart OCR",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .address-card {
        padding: 15px;
        border-radius: 10px;
        background-color: white;
        border-left: 5px solid #007bff;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .maps-link {
        color: #007bff;
        text-decoration: none;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔍 InfoSight - Local Smart OCR")
st.markdown("---")

# Sidebar for controls
with st.sidebar:
    st.header("Settings")
    st.info("This app runs 100% locally on your machine.")
    st.markdown("---")
    st.markdown("### Supported Formats")
    st.write("- Images (PNG, JPG, JPEG)")
    st.write("- PDFs (Scanned/Digital)")

# File Uploader
uploaded_file = st.file_uploader("Upload an Image or PDF", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file is not None:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Preview")
        if uploaded_file.type == "application/pdf":
            st.warning("PDF Preview not fully enabled in simple mode, but extraction will work!")
        else:
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)

    with col2:
        st.subheader("Actions")
        if st.button("Extract Data"):
            with st.spinner("Processing... This may take a few seconds on CPU."):
                # Save to a temporary file for ocr_model to read
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                try:
                    # Run OCR
                    results = run_ocr(tmp_path)
                    
                    if "error" in results:
                        st.error(f"Error: {results['error']}")
                    else:
                        st.success("Extraction Complete!")
                        
                        # Tabs for different data views
                        tab1, tab2, tab3 = st.tabs(["📊 Invoice Data", "📍 Address Intelligence", "📄 Extracted Text"])
                        
                        with tab1:
                            if "invoice_data" in results and results["invoice_data"]:
                                data = results["invoice_data"]
                                colA, colB = st.columns(2)
                                with colA:
                                    st.metric("Invoice Number", data.get("invoice_number", "N/A"))
                                    st.metric("Vendor", data.get("vendor_name", "N/A"))
                                    st.metric("Date", data.get("date", "N/A"))
                                with colB:
                                    st.metric("Total Amount", data.get("total_amount", "N/A"))
                                    st.metric("Client", data.get("client_name", "N/A"))
                            else:
                                st.info("No structured invoice data found.")
                                
                        with tab3:
                            st.text_area("Raw Text", results.get("text", "No text found."), height=300)
                            
                        with tab2:
                            if results["addresses"]:
                                st.write(f"Found {len(results['addresses'])} address(es):")
                                for addr in results["addresses"]:
                                    st.markdown(f"""
                                    <div class="address-card">
                                        <p><b>Original:</b> {addr['original']}</p>
                                        <p><b>Normalized:</b> {addr['normalized']}</p>
                                        <a href="{addr['maps_link']}" target="_blank" class="maps-link">📍 Open in Google Maps</a>
                                    </div>
                                    """, unsafe_allow_html=True)
                            else:
                                st.info("No addresses detected in this document.")
                
                except Exception as e:
                    st.error(f"Caught an exception: {e}")
                
                finally:
                    # Cleanup
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)

else:
    st.info("Please upload a file to begin.")

st.markdown("---")
st.caption("Powered by Google Gemini & Streamlit | Smart OCR Inference")
