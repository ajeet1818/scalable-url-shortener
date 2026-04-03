import streamlit as st
import requests
import qrcode
from io import BytesIO
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="URL Shortener",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 0rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# API Base URL
API_URL = "https://scalable-url-shortener-i6rt.onrender.com/"

st.title("🔗 URL Shortener")
st.markdown("Transform long URLs into short, shareable links with click tracking")

# Create tabs
tab1, tab2, tab3 = st.tabs(["📝 Create Short URL", "📊 View Stats", "🗑️ Delete URL"])

# Tab 1: Create Short URL
with tab1:
    st.header("Create a Shortened URL")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        original_url = st.text_input(
            "Enter the URL you want to shorten:",
            placeholder="https://www.example.com/very/long/url",
            label_visibility="collapsed"
        )
    
    with col2:
        create_button = st.button("🔗 Shorten", use_container_width=True)
    
    if create_button:
        if not original_url:
            st.error("Please enter a URL")
        elif not original_url.startswith(("http://", "https://")):
            st.error("Please enter a valid URL starting with http:// or https://")
        else:
            try:
                response = requests.post(
                    f"{API_URL}/shorten",
                    json={"original_url": original_url},
                    timeout=30
                )
                
                if response.status_code == 201:
                    data = response.json()
                    short_code = data["short_code"]
                    short_url = f"http://localhost:8000/api/{short_code}"
                    
                    st.success("✅ URL shortened successfully!")
                    
                    # Display results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### Short URL")
                        st.code(short_url, language="text")
                        st.button("📋 Copy to Clipboard", key="copy_short")
                    
                    with col2:
                        st.markdown("### QR Code")
                        qr = qrcode.QRCode(version=1, box_size=10, border=4)
                        qr.add_data(short_url)
                        qr.make(fit=True)
                        img = qr.make_image(fill_color="black", back_color="white")
                        img_bytes = BytesIO()
                        img.save(img_bytes, format='PNG')
                        img_bytes.seek(0)
                        st.image(img_bytes, width=200)
                    
                    # Show details
                    st.markdown("### Details")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Short Code", short_code)
                    with col2:
                        st.metric("Clicks", "0")
                    with col3:
                        st.metric("Created", datetime.fromisoformat(data["created_at"]).strftime("%Y-%m-%d"))
                    with col4:
                        st.metric("ID", data["id"])
                    
                    # Store in session for quick access
                    st.session_state.last_short_code = short_code
                    
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to API. Make sure the FastAPI server is running on http://localhost:8000")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Tab 2: View Stats
with tab2:
    st.header("View Statistics")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        short_code = st.text_input(
            "Enter short code to view stats:",
            placeholder="e.g., abc123",
            label_visibility="collapsed"
        )
    
    with col2:
        stats_button = st.button("📊 Get Stats", use_container_width=True)
    
    if stats_button:
        if not short_code:
            st.error("Please enter a short code")
        else:
            try:
                response = requests.get(
                    f"{API_URL}/stats/{short_code}",
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.success("✅ Statistics found")
                    
                    # Display metrics
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Total Clicks", data["clicks"])
                    with col2:
                        st.metric("Created Date", datetime.fromisoformat(data["created_at"]).strftime("%Y-%m-%d %H:%M"))
                    with col3:
                        st.metric("Short Code", data["short_code"])
                    
                    # Display URLs
                    st.markdown("### Original URL")
                    st.code(data["original_url"], language="text")
                    
                    # QR Code for stats
                    st.markdown("### QR Code")
                    short_url = f"http://localhost:8000/api/{data['short_code']}"
                    qr = qrcode.QRCode(version=1, box_size=10, border=4)
                    qr.add_data(short_url)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    img_bytes = BytesIO()
                    img.save(img_bytes, format='PNG')
                    img_bytes.seek(0)
                    st.image(img_bytes, width=200)
                    
                else:
                    st.error(f"Short code '{short_code}' not found")
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to API. Make sure the FastAPI server is running")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Tab 3: Delete URL
with tab3:
    st.header("Delete a Shortened URL")
    
    st.warning("⚠️ This action cannot be undone. Deleting a URL will permanently remove its record.")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        delete_code = st.text_input(
            "Enter short code to delete:",
            placeholder="e.g., abc123",
            label_visibility="collapsed",
            key="delete_input"
        )
    
    with col2:
        delete_button = st.button("🗑️ Delete", use_container_width=True, key="delete_btn")
    
    if delete_button:
        if not delete_code:
            st.error("Please enter a short code")
        else:
            try:
                # Show confirmation dialog
                if "delete_confirmed" not in st.session_state:
                    st.session_state.delete_confirmed = False
                
                if not st.session_state.delete_confirmed:
                    st.info(f"Are you sure you want to delete '{delete_code}'?")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Yes, delete it"):
                            st.session_state.delete_confirmed = True
                            st.rerun()
                    with col2:
                        if st.button("❌ Cancel"):
                            st.session_state.delete_confirmed = False
                else:
                    response = requests.delete(
                        f"{API_URL}/{delete_code}",
                        timeout=5
                    )
                    
                    if response.status_code == 204:
                        st.success(f"✅ Short code '{delete_code}' has been deleted successfully")
                        st.session_state.delete_confirmed = False
                    else:
                        st.error(f"Short code '{delete_code}' not found or error occurred")
                        st.session_state.delete_confirmed = False
                        
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to API. Make sure the FastAPI server is running")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🚀 <strong>URL Shortener</strong> | Built with Streamlit & FastAPI</p>
    <p style='font-size: 0.8em; color: gray;'>Make sure FastAPI server is running: <code>uvicorn app.main:app --reload</code></p>
</div>
""", unsafe_allow_html=True)
