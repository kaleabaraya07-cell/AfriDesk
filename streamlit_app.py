import streamlit as st
import os
import json
import base64
import google.generativeai as genai
from pathlib import Path
from streamlit_option_menu import option_menu

# Initialize Gemini API
def init_gemini():
    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        return genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"Error initializing Gemini: {e}")
        return None

# Set page config
st.set_page_config(
    page_title="AfriDesk - Your Guide to African Government Services",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
def load_css():
    st.markdown("""
    <style>
        /* Main container */
        .main {
            padding: 1rem 2rem;
        }
        
        /* Header */
        .header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        
        /* Service cards */
        .service-card {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            border: 1px solid #e0e0e0;
            transition: all 0.3s ease;
        }
        
        .service-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        }
        
        .service-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: #2a5298;
        }
        
        /* Sidebar */
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
            border-right: 1px solid #0f3460;
            box-shadow: 2px 0 15px rgba(0,0,0,0.2);
            color: #e6e6e6;
        }
        
        /* Sidebar header */
        .sidebar .sidebar-content h1 {
            color: #e6e6e6;
            border-bottom: 2px solid #0f3460;
            padding-bottom: 0.5rem;
        }
        
        /* Sidebar text color */
        .sidebar .stTextInput label, .sidebar .stMarkdown, .sidebar .stMarkdown p {
            color: #e6e6e6 !important;
        }
        
        /* Search input */
        .sidebar .stTextInput>div>div>input {
            background-color: rgba(255, 255, 255, 0.1);
            color: #ffffff;
            border: 1px solid #0f3460;
            transition: all 0.3s ease;
        }
        
        /* Hover effects */
        .sidebar .stTextInput>div>div>input:hover, 
        .sidebar .stTextInput>div>div>input:focus {
            border-color: #64b4ff;
            box-shadow: 0 0 0 2px rgba(100, 180, 255, 0.2);
        }
        
        /* Menu item hover */
        .sidebar [data-testid='stSidebarNav'] a:hover {
            background-color: rgba(100, 180, 255, 0.2) !important;
        }
        
        /* Buttons */
        .stButton>button {
            border-radius: 8px;
            background: #2a5298;
            color: white;
            font-weight: 500;
            border: none;
            padding: 0.6rem 1.2rem;
            margin: 0.3rem 0;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background: #1e3c72;
            transform: translateY(-1px);
        }
    </style>
    """, unsafe_allow_html=True)

def show_welcome():
    st.markdown("""
    <div class="header">
        <h1>Welcome to AfriDesk 🌍</h1>
        <h3>Your Personalized Guide to Government Services in Africa</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem;">
            Access government services, find clinics, and get assistance with official processes across Africa.
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_features():
    st.markdown("## Government Information Services")
    
    st.markdown("""
    <style>
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .feature-card:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    }
    .feature-card h3 {
        color: #ffffff;
        margin-bottom: 0.8rem;
        font-weight: 600;
    }
    .feature-card p {
        color: #e2e8f0;
        line-height: 1.6;
        opacity: 0.9;
        margin-bottom: 0;
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🏛️</div>
            <h3>Government Portals</h3>
            <p>Access official government websites and digital services across different ministries and departments.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📑</div>
            <h3>Public Records</h3>
            <p>Find and request official documents, certificates, and public records from government agencies.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📢</div>
            <h3>Announcements</h3>
            <p>Stay updated with the latest government announcements, policies, and public notices.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # New row of feature cards
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🏥</div>
            <h3>Healthcare</h3>
            <p>Access healthcare services, find hospitals, and schedule medical appointments.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🏠</div>
            <h3>Housing</h3>
            <p>Find housing assistance programs and apply for public housing services.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎓</div>
            <h3>Education</h3>
            <p>Access educational resources, scholarships, and school registration services.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    st.markdown("---")

def get_services():
    return [
        {
            "name": "Healthcare Services",
            "icon": "🏥",
            "description": "Access to public healthcare facilities, clinics, and medical services.",
            "details": {
                "Eligibility": "All citizens and legal residents",
                "Requirements": ["National ID", "Health Insurance Card (if applicable)", "Referral letter (for specialists)"],
                "Processing Time": "Varies by facility",
                "Cost": "Free for basic services, fees may apply for specialized care"
            }
        },
        {
            "name": "Passport & Visa",
            "icon": "🛂",
            "description": "Passport applications, renewals, and visa processing services.",
            "details": {
                "Eligibility": "Citizens and eligible foreign nationals",
                "Requirements": ["Birth certificate", "National ID", "Passport photos", "Proof of travel"],
                "Processing Time": "10-15 business days",
                "Cost": "Varies by passport type and processing speed"
            }
        },
        {
            "name": "Business Registration",
            "icon": "💼",
            "description": "Register and license new businesses and companies.",
            "details": {
                "Eligibility": "Citizens, residents, and foreign investors",
                "Requirements": ["Business name reservation", "Articles of Association", "Tax identification", "Business plan"],
                "Processing Time": "5-10 business days",
                "Cost": "Varies by business type and capital"
            }
        },
        {
            "name": "Tax Information",
            "icon": "💰",
            "description": "Tax registration, filing, and payment services.",
            "details": {
                "Eligibility": "All taxpayers",
                "Requirements": ["Tax ID number", "Financial records", "Previous tax returns"],
                "Processing Time": "Varies by service",
                "Cost": "Fees may apply for certain services"
            }
        },
        {
            "name": "Education Services",
            "icon": "🎓",
            "description": "School registration, certification, and academic services.",
            "details": {
                "Eligibility": "Students and educational institutions",
                "Requirements": ["Academic records", "Birth certificate", "Previous school reports"],
                "Processing Time": "Varies by institution",
                "Cost": "Varies by level of education and institution"
            }
        },
        {
            "name": "Housing & Utilities",
            "icon": "🏠",
            "description": "Housing applications and utility connections.",
            "details": {
                "Eligibility": "Varies by program",
                "Requirements": ["Proof of income", "Identification", "Proof of residence"],
                "Processing Time": "14-30 business days",
                "Cost": "Varies by service and location"
            }
        }
    ]

def show_service_details(service):
    st.markdown(f"# {service['icon']} {service['name']}")
    st.markdown(f"{service['description']}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Service Details")
        st.markdown("#### Eligibility")
        st.info(service['details']['Eligibility'])
        
        st.markdown("#### Processing Time")
        st.info(service['details']['Processing Time'])
    
    with col2:
        st.markdown("#### Requirements")
        for req in service['details']['Requirements']:
            st.markdown(f"- {req}")
        
        st.markdown("#### Cost")
        st.info(service['details']['Cost'])
    
    st.markdown("---")
    
    if st.button("← Back to Services"):
        st.session_state['current_page'] = 'services'
        st.rerun()

def show_personalized_service_details(service):
    """Display service details personalized for the user's profile"""
    user_profile = st.session_state.user_profile_data
    
    # Display service header with icon and name
    st.markdown(f"# {service['icon']} {service['name']}")
    st.markdown(f"{service['description']}")
    
    # Add a note that this is personalized
    st.success("ℹ️ These service details are personalized based on your profile.")
    
    st.markdown("---")
    
    # Two-column layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Service Details")
        
        # Personalized eligibility based on user profile
        st.markdown("#### Eligibility")
        if 'age' in user_profile and user_profile.get('age', 0) < 18 and '18+' in service['details']['Eligibility']:
            st.warning("⚠️ Age Restriction: This service is only available for individuals 18 years and older.")
        else:
            st.info(service['details']['Eligibility'])
        
        # Processing time with personalized estimate if possible
        st.markdown("#### Estimated Processing Time")
        processing_time = service['details']['Processing Time']
        if 'country' in user_profile and 'Nigeria' in user_profile['country']:
            processing_time = f"{processing_time} (faster processing for residents in {user_profile['country']})"
        st.info(processing_time)
    
    with col2:
        st.markdown("#### Requirements")
        
        # Add personalized requirements based on user profile
        requirements = service['details']['Requirements'].copy()
        
        # Add additional requirements based on user's country if needed
        if 'country' in user_profile and 'Nigeria' in user_profile['country']:
            requirements.append("Valid Nigerian ID (e.g., NIN, Voter's Card, or International Passport)")
        
        # Show requirements in a more readable format
        for req in requirements:
            st.markdown(f"- {req}")
        
        # Cost information with personalized notes
        st.markdown("#### Cost Estimate")
        cost = service['details']['Cost']
        if 'income_level' in user_profile and 'low' in user_profile['income_level'].lower():
            cost += " (discounts may be available for low-income individuals)"
        st.info(cost)
    
    # Add a section for next steps based on the service
    st.markdown("---")
    st.markdown("### Next Steps")
    
    if st.button("📅 Schedule an Appointment", use_container_width=True):
        st.session_state['show_appointment_form'] = True
    
    if st.session_state.get('show_appointment_form', False):
        with st.form("appointment_form"):
            st.markdown("#### Schedule an Appointment")
            st.date_input("Preferred Date")
            st.text_input("Contact Number")
            if st.form_submit_button("Submit Appointment Request"):
                st.success("Appointment request submitted! We'll contact you shortly to confirm.")
                st.session_state['show_appointment_form'] = False
    
    st.markdown("---")
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1,1,2])
    with col1:
        if st.button("← Back to Services"):
            st.session_state['current_page'] = 'services'
            st.rerun()
    
    with col2:
        if st.button("🔄 Update Profile"):
            st.session_state['current_page'] = 'profile'
            st.rerun()

def show_profile_creation():
    st.markdown("# 👤 Set Up Your Profile")
    
    # Initialize step counter if not exists
    if 'profile_step' not in st.session_state:
        st.session_state.profile_step = 0
        
    # Initialize form data if not exists
    if 'profile_data' not in st.session_state:
        st.session_state.profile_data = {
            'name': '',
            'age': 25,
            'gender': 'Prefer not to say',
            'country': '',
            'email': '',
            'occupation': '',
            'income_level': 'Middle',
            'needs': [],
            'additional_info': ''
        }
    
    # Show the appropriate step
    if st.session_state.profile_step == 0:
        show_welcome_step()
    elif st.session_state.profile_step == 1:
        show_personal_info_step()
    elif st.session_state.profile_step == 2:
        show_contact_info_step()
    elif st.session_state.profile_step == 3:
        show_preferences_step()
    elif st.session_state.profile_step == 4:
        show_review_step()

def show_welcome_step():
    st.markdown("## Welcome to Your Profile Setup")
    st.markdown("Let's get started by setting up your profile. This will help us provide you with personalized service recommendations.")
    
    if st.button("Start Setup", type="primary"):
        st.session_state.profile_step = 1
        st.rerun()

def show_personal_info_step():
    st.markdown("## Personal Information")
    
    with st.form("personal_info"):
        name = st.text_input("Full Name*", 
                          value=st.session_state.profile_data['name'])
        
        age = st.number_input("Age*", 
                            min_value=1, 
                            max_value=120, 
                            step=1,
                            value=st.session_state.profile_data['age'])
                            
        gender = st.selectbox("Gender",
                            ["Prefer not to say", "Male", "Female", "Other"],
                            index=["Prefer not to say", "Male", "Female", "Other"].index(
                                st.session_state.profile_data['gender']))
        
        countries = [
            "Select a country",
            "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde", "Cameroon", "Central African Republic",
            "Chad", "Comoros", "Congo (Congo-Brazzaville)", "Côte d'Ivoire", "Democratic Republic of the Congo", "Djibouti",
            "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini (fmr. Swaziland)", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea",
            "Guinea-Bissau", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius",
            "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", "Senegal", "Seychelles",
            "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"
        ]
        
        country = st.selectbox(
            "Country of Residence*",
            options=countries,
            index=countries.index(st.session_state.profile_data['country']) if st.session_state.profile_data['country'] in countries else 0
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Back"):
                st.session_state.profile_step = 0
                st.rerun()
        with col2:
            if st.form_submit_button("Next") and name and country:
                st.session_state.profile_data.update({
                    'name': name,
                    'age': age,
                    'gender': gender,
                    'country': country
                })
                st.session_state.profile_step = 2
                st.rerun()

def show_contact_info_step():
    st.markdown("## Contact Information")
    
    with st.form("contact_info"):
        email = st.text_input("Email Address",
                            value=st.session_state.profile_data['email'])
                            
        occupation = st.text_input("Occupation",
                                 value=st.session_state.profile_data['occupation'])
        
        income_level = st.select_slider(
            "Income Level",
            options=["Low", "Lower-Middle", "Middle", "Upper-Middle", "High"],
            value=st.session_state.profile_data['income_level']
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Back"):
                st.session_state.profile_step = 1
                st.rerun()
        with col2:
            if st.form_submit_button("Next"):
                st.session_state.profile_data.update({
                    'email': email,
                    'occupation': occupation,
                    'income_level': income_level
                })
                st.session_state.profile_step = 3
                st.rerun()

def show_preferences_step():
    st.markdown("## Your Preferences")
    
    with st.form("preferences"):
        needs = st.multiselect(
            "What services are you interested in? (Select all that apply)",
            ["Healthcare", "Education", "Housing", "Business", "Legal", "Social Services"],
            default=st.session_state.profile_data['needs']
        )
        
        additional_info = st.text_area(
            "Any specific needs or requirements?",
            value=st.session_state.profile_data['additional_info']
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Back"):
                st.session_state.profile_step = 2
                st.rerun()
        with col2:
            if st.form_submit_button("Review & Submit"):
                st.session_state.profile_data.update({
                    'needs': needs,
                    'additional_info': additional_info
                })
                st.session_state.profile_step = 4
                st.rerun()

def show_review_step():
    st.markdown("## Review Your Profile")
    
    st.markdown("### Personal Information")
    st.write(f"**Name:** {st.session_state.profile_data['name']}")
    st.write(f"**Age:** {st.session_state.profile_data['age']}")
    st.write(f"**Gender:** {st.session_state.profile_data['gender']}")
    st.write(f"**Country:** {st.session_state.profile_data['country']}")
    
    st.markdown("### Contact Information")
    st.write(f"**Email:** {st.session_state.profile_data['email'] or 'Not provided'}")
    st.write(f"**Occupation:** {st.session_state.profile_data['occupation'] or 'Not provided'}")
    st.write(f"**Income Level:** {st.session_state.profile_data['income_level']}")
    
    st.markdown("### Preferences")
    st.write("**Interested Services:** " + ", ".join(st.session_state.profile_data['needs']) or 'None selected')
    if st.session_state.profile_data['additional_info']:
        st.write("**Additional Notes:**")
        st.write(st.session_state.profile_data['additional_info'])
    
    # Create three columns for the buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Back to Edit"):
            st.session_state.profile_step = 3
            st.rerun()
    
    with col2:
        if st.button("✅ Save Profile"):
            st.session_state.user_profile_data = st.session_state.profile_data
            # Ensure services will be filtered based on this profile
            if 'services_data' in st.session_state:
                del st.session_state['services_data']
            st.success("Profile saved successfully!", icon="✅")
            # st.session_state.current_page = 'recommendations'
            # st.rerun()
    
    # Form handling is done in the individual step functions

def get_service_recommendations(profile):
    """Generate service recommendations using Gemini API"""
    try:
        model = init_gemini()
        if not model:
            return "Unable to connect to recommendation service. Using default recommendations."
            
        prompt = f"""Based on the following user profile, recommend relevant government services in a clear, concise way.
        Focus on services that would be most beneficial for this person's needs.
        
        Profile:
        {json.dumps(profile, indent=2)}
        
        Recommended Services:"""
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error getting recommendations: {e}")
        return "Unable to generate recommendations at this time. Please try again later."

def show_recommendations():
    if 'user_profile_data' not in st.session_state:
        st.warning("No profile found. Please create a profile first.")
        st.session_state['current_page'] = 'profile'
        st.rerun()
    
    profile = st.session_state['user_profile_data']
    
    st.markdown(f"# 🎯 Personalized Recommendations for {profile['name']}")
    
    with st.spinner("Generating personalized recommendations..."):
        recommendations = get_service_recommendations(profile)
    
    st.markdown("## Recommended Services")
    st.markdown(recommendations)
    
    st.markdown("---")
    if st.button("← Back to Profile"):
        st.session_state['current_page'] = 'profile'
        st.rerun()

def show_services():
    user_has_profile = 'user_profile_data' in st.session_state and st.session_state.user_profile_data
    if not user_has_profile:
        st.warning("⚠️ You haven't set up your profile yet. Personalize your experience by setting up your profile to get tailored service recommendations.")
        return

    from afridesk.services import services_list
    services_list()
        



def show_about():
    st.title("About AfriDesk")
    st.write("""
    ## Your Gateway to African Government Services
    
    AfriDesk is a comprehensive platform designed to simplify access to government services across Africa. 
    Our mission is to bridge the gap between citizens and essential government services through technology.
    
    ### Key Features:
    - **Service Directory**: Browse a wide range of government services
    - **Personalized Assistance**: Get tailored service recommendations based on your profile
    - **AI Chat Support**: 24/7 virtual assistant to guide you through processes
    - **User Profiles**: Save your information for faster service access
    
    ### Our Vision
    To make government services more accessible, efficient, and user-friendly for all African citizens.
    
    ### Contact Us
    Have questions or feedback? We'd love to hear from you at support@afridesk.africa
    """)
    
    st.markdown("---")
    st.caption("© 2024 AfriDesk. All rights reserved.")

def show_chat_interface():
    st.markdown("## 💬 Government Services Assistant")
    
    # Initialize chat history if it doesn't exist

    assistant = None
    # Initialize GovernmentAssistant if not already in session state
    try:
        from afridesk.assistant import GovernmentAssistant
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            st.warning("OpenAI API key not found. Some features may be limited.")
        profile_data = st.session_state.get('user_profile_data', {})
        assistant = GovernmentAssistant(openai_api_key, profile_data)
    except Exception as e:
        st.error(f"Error initializing assistant: {str(e)}")
    

    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": """Hello! I'm your Government Services Assistant. I can help you with:
                
- Finding government offices and services
- Understanding government procedures and requirements
- Completing official forms and applications
- Getting information about public services and benefits

How can I assist you today?"""
            }
        ]
    # Display chat messages with better styling
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input with better placeholder
    if prompt := st.chat_input("Ask me anything about government services..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Searching for information..."):
                try:
                    # Get user profile data for context if available
                    user_context = st.session_state.get('user_profile_data', {}) or st.session_state.get('user_data', {})
                    
                    # Generate response using the assistant
                    # Use the chat method for conversation history
                    chat_history = [
                        assistant._create_system_message()
                    ]
                    
                    # Add previous messages to maintain context
                    for msg in st.session_state.messages[-5:]:  # Keep last 5 messages for context
                        chat_history.append({"role": msg["role"], "content": msg["content"]})
                    
                    # Get response from the assistant
                    response = assistant.chat(chat_history)
                    
                    # If the response is about finding offices, try to get structured data
                    if any(keyword in prompt.lower() for keyword in ['find', 'locate', 'where is', 'nearest', 'office']):
                        location = user_context.get('location', '')
                        if location:
                            office_type = None
                            if 'dmv' in prompt.lower() or 'driving' in prompt.lower():
                                office_type = 'DMV'
                            elif 'post' in prompt.lower() or 'mail' in prompt.lower():
                                office_type = 'Post Office'
                            elif 'city hall' in prompt.lower() or 'municipal' in prompt.lower():
                                office_type = 'City Hall'
                                
                            office_info = assistant.get_government_offices(location, office_type)
                            if office_info and 'error' not in office_info.lower():
                                try:
                                    offices = json.loads(office_info).get('offices', [])
                                    if offices:
                                        response += "\n\n**Nearby Government Offices:**\n\n"
                                        for office in offices[:3]:  # Show top 3 results
                                            response += f"**{office.get('name', 'Office')}**\n"
                                            if 'address' in office:
                                                response += f"📍 {office['address']}\n"
                                            if 'phone' in office:
                                                response += f"📞 {office['phone']}\n"
                                            if 'hours' in office:
                                                response += f"🕒 {office['hours']}\n"
                                            if 'website' in office:
                                                response += f"🌐 [Visit Website]({office['website']})\n"
                                            response += "\n"
                                except json.JSONDecodeError:
                                    response += "\n\nI found some information about local offices, but couldn't format it properly."
                
                
                    st.markdown(response, unsafe_allow_html=True)
                    
                except Exception as e:
                    error_msg = f"I'm sorry, I encountered an error while processing your request: {str(e)}"
                    st.error(error_msg)
                    response = error_msg
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    # Install required packages
    try:
        from streamlit_option_menu import option_menu
    except ImportError:
        import sys
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit-option-menu"])
        from streamlit_option_menu import option_menu
        
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    load_css()
    
    # Initialize session state for page navigation
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'welcome'
    
    # Initialize selected service if not set
    if 'selected_service' not in st.session_state:
        st.session_state['selected_service'] = get_services()[0]
    
    # Sidebar navigation
    with st.sidebar:
        # Add logo with centered alignment and proper sizing
        st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <img src='data:image/jpg;base64,{}' style='max-width: 80%; height: auto; border-radius: 10px;'>
            <h1 style='margin-top: 15px; color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);'>AfriDesk</h1>
        </div>
        """.format(base64.b64encode(open("WhatsApp Image 2025-08-23 at 16.22.34_0012d67c.jpg", "rb").read()).decode()), unsafe_allow_html=True)
        
        # Main navigation menu with improved styling and icons
        menu = option_menu(
            menu_title=None,
            options=["Home", "Services", "Chat Assistant", "Profile", "About"],
            icons=["house", "list-task", "chat-left-text", "person", "info-circle"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {
                    "padding": "0!important", 
                    "background": "linear-gradient(180deg, #1a1a2e 0%, #16213e 100%)", 
                    "border-radius": "0.5rem", 
                    "box-shadow": "2px 0 15px rgba(0,0,0,0.2)",
                    "margin-bottom": "1rem"
                },
                "icon": {"color": "#64b4ff", "font-size": "1.2rem"}, 
                "nav-link": {
                    "font-size": "0.95rem",
                    "text-align": "left",
                    "margin": "0.2rem 0",
                    "--hover-color": "rgba(100, 180, 255, 0.2)",
                    "border-radius": "0.5rem",
                    "padding": "0.7rem 1rem",
                    "transition": "all 0.3s ease",
                    "color": "#e0e0e0"
                },
                "nav-link:hover": {
                    "background-color": "rgba(100, 180, 255, 0.2)",
                    "color": "#ffffff",
                    "transform": "translateX(5px)"
                },
                "nav-link-selected": {
                    "background-color": "#2a5298", 
                    "color": "white",
                    "font-weight": "500",
                    "box-shadow": "0 4px 12px rgba(42, 82, 152, 0.3)"
                },
            }
        )
        
        if menu == "Home":
            st.session_state['current_page'] = 'welcome'
        elif menu == "Profile":
            st.session_state['current_page'] = 'profile'
        elif menu == "Services":
            st.session_state['current_page'] = 'services'
        elif menu == "Chat Assistant":
            st.session_state['current_page'] = 'chat'
        elif menu == "About":
            st.session_state['current_page'] = 'about'
    
    # Main content area
    if st.session_state['current_page'] == 'welcome':
        show_welcome()
        show_features()
    
    elif st.session_state['current_page'] == 'services':
        show_services()
    
    elif st.session_state['current_page'] == 'profile':
        show_profile_creation()
    
    elif st.session_state['current_page'] == 'recommendations':
        show_recommendations()
    
    elif st.session_state['current_page'] == 'chat':
        show_chat_interface()
        
        if st.button("← Back to Services", use_container_width=True):
            st.session_state['current_page'] = 'services'
            st.rerun()
            
    elif st.session_state['current_page'] == 'about':
        show_about()

if __name__ == "__main__":
    main()

