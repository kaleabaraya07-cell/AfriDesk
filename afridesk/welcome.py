import streamlit as st
import os

def show_welcome_page():
    """
    Show the welcome page with the main interface
    """
    # Set page to use full width and configure page
    st.set_page_config(
        page_title="AfriDesk - Kenya Government Services",
        page_icon="🇰🇪",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state for page navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'welcome'

    
    # Remove default padding and margins
    st.markdown("""
    <style>
        .main > div {
            max-width: 100%;
            padding: 0;
        }
        .stApp {
            padding: 0 !important;
        }
        .welcome-button {
            width: 200px !important;
            margin: 20px auto !important;
            display: block !important;
            background-color: #0d6efd !important;
            color: white !important;
            font-weight: bold !important;
            padding: 0.75rem 1.5rem !important;
            border-radius: 50px !important;
            border: none !important;
            font-size: 1.1rem !important;
            transition: all 0.3s ease !important;
        }
        .welcome-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
        }
        .welcome-container {
            position: relative;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #0d6efd 0%, #0dcaf0 100%);
            color: white;
        }
        .welcome-content {
            max-width: 800px;
            z-index: 2;
        }
        .welcome-title {
            font-size: 3.5rem;
            font-weight: 800;
            margin-bottom: 1rem;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .welcome-subtitle {
            font-size: 1.5rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }
        @media (max-width: 768px) {
            .welcome-title {
                font-size: 2.5rem;
            }
            .welcome-subtitle {
                font-size: 1.2rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    try:
        # Check if we're in development mode (no HTML file)
        html_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'index.html')
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Hide the HTML button since we'll use Streamlit's button
            html_content = html_content.replace('id="startButton"', 'style="display: none;"')
            
            # Display the HTML content in full width
            st.components.v1.html(html_content, height=800, scrolling=False)
            
            # Add a single centered button below the HTML content
            if st.button("Get Started", key="get_started_btn", help="Start exploring government services"):
                st.session_state['current_page'] = 'home'
                st.rerun()
        else:
            # Fallback welcome page if HTML file is not found
            st.markdown("""
            <div class="welcome-container">
                <div class="welcome-content">
                    <h1 class="welcome-title">Welcome to AfriDesk Kenya</h1>
                    <p class="welcome-subtitle">Your one-stop platform for accessing government services across Kenya</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Get Started", key="get_started_btn_fallback", help="Start exploring government services"):
                st.session_state['current_page'] = 'home'
                st.rerun()
                
    except Exception as e:
        st.error(f"Error loading welcome page: {str(e)}")
        st.markdown("""
        <div style='text-align: center; padding: 40px;'>
            <h1>Welcome to AfriDesk Kenya</h1>
            <p>Your one-stop platform for accessing government services across Kenya</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Get Started", key="get_started_btn_error"):
            st.session_state['current_page'] = 'home'
            st.rerun()
