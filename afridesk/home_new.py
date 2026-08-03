import streamlit as st

def show_home_page():
    """
    Modern home page for AfriDesk using Streamlit components
    """
    # Page configuration
    st.set_page_config(
        page_title="AfriDesk - Your Government Services Assistant",
        page_icon="🌍",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        font-family: 'Poppins', sans-serif;
        color: #343a40;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #4361ee, #7209b7);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 30px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        margin: 1rem 0;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: #4361ee;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        background: linear-gradient(90deg, #4361ee, #7209b7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: #4a4a4a;
        margin-bottom: 2rem;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .section-subtitle {
        font-size: 1.2rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 3rem;
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    """, unsafe_allow_html=True)
    
    # Hero Section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <h1 class="hero-title">Access Government Services Across Africa with Ease</h1>
        <p class="hero-subtitle">
            AfriDesk is your one-stop platform for all government services. 
            Find, apply, and manage services from anywhere, anytime.
        </p>
        """, unsafe_allow_html=True)
        
        if st.button('Start Now', key='start_now_btn'):
            st.session_state['current_page'] = 'onboarding'
            st.experimental_rerun()
    
    with col2:
        st.image("https://via.placeholder.com/600x400?text=AfriDesk", 
                use_column_width=True)
    
    # Features Section
    st.markdown("""
    <h2 class="section-title">Why Choose AfriDesk?</h2>
    <p class="section-subtitle">We're revolutionizing how you access government services with our innovative platform.</p>
    """, unsafe_allow_html=True)
    
    # Features Grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">
                <i class="fas fa-bolt"></i>
            </div>
            <h3>Fast & Easy</h3>
            <p>Access government services in just a few clicks. No more long queues or complicated processes.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">
                <i class="fas fa-shield-alt"></i>
            </div>
            <h3>Secure & Private</h3>
            <p>Your data is protected with enterprise-grade security and encryption.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">
                <i class="fas fa-headset"></i>
            </div>
            <h3>24/7 Support</h3>
            <p>Our support team is always ready to help you with any questions or issues.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to Action
    st.markdown("""
    <div style="text-align: center; margin: 4rem 0;">
        <h2>Ready to get started?</h2>
        <p>Join thousands of users who are already using AfriDesk to access government services.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button('Get Started Now', key='cta_btn', use_container_width=True):
        st.session_state['current_page'] = 'onboarding'
        st.experimental_rerun()

if __name__ == "__main__":
    show_home_page()