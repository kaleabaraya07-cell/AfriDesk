import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def onboarding_questionnaire():
    st.set_page_config(
        page_title="Let's Get Started",
        page_icon="📝",
        layout="centered"
    )
    
    # Initialize session state for form progress
    if 'form_step' not in st.session_state:
        st.session_state['form_step'] = 0
        st.session_state['user_data'] = {}
    
    # Progress bar
    progress = st.progress(0)
    
    # Form steps
    steps = [
        "Personal Information",
        "Location Details",
        "Service Preferences",
        "Review & Submit"
    ]
    
    # Update progress
    progress.progress((st.session_state['form_step'] + 1) / len(steps))
    
    # Current step display
    st.caption(f"Step {st.session_state['form_step'] + 1} of {len(steps)}")
    st.subheader(steps[st.session_state['form_step']])
    
    # Add custom CSS for better form styling
    st.markdown("""
    <style>
        /* Form labels */
        .stTextInput > label, .stSelectbox > label, .stMultiselect > label, .stCheckbox > label {
            color: #1e293b !important;
            font-weight: 600 !important;
            font-size: 1.05rem !important;
        }
        
        /* Section headers */
        h3 {
            color: #0f172a !important;
            border-bottom: 2px solid #4f46e5;
            padding-bottom: 8px;
            margin-bottom: 1.5rem !important;
        }
        
        /* Form container */
        .stForm {
            background: #f8f9fa;  /* Light gray background */
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid #dee2e6;
            margin: 1rem 0;
        }
        
        /* Input fields */
        .stTextInput > div > div > input, 
        .stSelectbox > div > div > div {
            background-color: #f8f9fa !important;
            border: 1px solid #ced4da !important;
            border-radius: 8px !important;
            padding: 0.5rem 0.75rem !important;
        }
        
        /* Focus state */
        .stTextInput > div > div > input:focus, 
        .stSelectbox > div > div > div:focus-within {
            border-color: #4f46e5 !important;
            box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2) !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Form content based on current step
    with st.form(key='onboarding_form'):
        if st.session_state['form_step'] == 0:  # Personal Information
            st.markdown("### Personal Information")
            st.session_state['user_data']['first_name'] = st.text_input("First Name")
            st.session_state['user_data']['last_name'] = st.text_input("Last Name")
            st.session_state['user_data']['email'] = st.text_input("Email Address")
            st.session_state['user_data']['phone'] = st.text_input("Phone Number")
            
        elif st.session_state['form_step'] == 1:  # Location Details
            st.markdown("### Location Details")
            st.session_state['user_data']['country'] = st.selectbox(
                "Country",
                ["Nigeria", "Kenya", "South Africa", "Ghana", "Rwanda", "Other"]
            )
            st.session_state['user_data']['state'] = st.text_input("State/Province")
            st.session_state['user_data']['city'] = st.text_input("City/Town")
            
        elif st.session_state['form_step'] == 2:  # Service Preferences
            st.markdown("### Service Preferences")
            st.session_state['user_data']['services_needed'] = st.multiselect(
                "What services are you interested in? (Select all that apply)",
                ["Passport/Visa", "National ID", "Business Registration", 
                 "Tax Services", "Health Services", "Education Services"]
            )
            st.session_state['user_data']['language'] = st.selectbox(
                "Preferred Language",
                ["English", "French", "Swahili", "Arabic", "Portuguese"]
            )
            
        else:  # Review & Submit
            st.subheader("Please review your information")
            st.json(st.session_state['user_data'])
            st.checkbox("I agree to the terms of service and privacy policy", key="terms_agreed")
        
        # Navigation buttons
        col1, col2 = st.columns([1, 1])
        
        submitted = False
        
        with col1:
            if st.session_state['form_step'] > 0:
                if st.form_submit_button("Previous"):
                    st.session_state['form_step'] -= 1
                    st.rerun()
        
        with col2:
            if st.session_state['form_step'] < len(steps) - 1:
                if st.form_submit_button("Next"):
                    st.session_state['form_step'] += 1
                    st.rerun()
            else:
                submitted = st.form_submit_button("Complete Registration", type="primary")
    
    # Show success message after form submission
    if submitted and st.session_state.get('terms_agreed', False):
        # Save all the important data to session state
        st.session_state['onboarding_complete'] = True
        st.session_state['current_page'] = 'services'  # Set the next page
        
        # Make sure user_data is properly set
        if 'user_data' not in st.session_state:
            st.session_state['user_data'] = {}
            
        # Force a rerun to ensure session state is saved
        st.rerun()
        
    # This will be shown after the rerun
    if st.session_state.get('onboarding_complete', False):
        st.balloons()
        st.success("🎉 Registration Successful!")
        st.subheader("Your Information")
        
        # Display user data in a nice format
        user_data = st.session_state.get('user_data', {})
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Personal Information**")
            st.write(f"👤 **Name:** {user_data.get('first_name', '')} {user_data.get('last_name', '')}")
            st.write(f"📧 **Email:** {user_data.get('email', '')}")
            st.write(f"📱 **Phone:** {user_data.get('phone', '')}")
            
        with col2:
            st.write("**Location**")
            st.write(f"🌍 **Country:** {user_data.get('country', '')}")
            st.write(f"🏙️ **State/Province:** {user_data.get('state', '')}")
            st.write(f"🏡 **City/Town:** {user_data.get('city', '')}")
        
        st.write("**Services Needed:**", ", ".join(user_data.get('services_needed', [])))
        
        # Add a button to continue to services
        if st.button("Continue to Services"):
            st.session_state['current_page'] = 'services'
            st.rerun()
    elif submitted and not st.session_state.get('terms_agreed', False):
        st.error("Please agree to the terms and conditions to continue.")

if __name__ == "__main__":
    onboarding_questionnaire()
