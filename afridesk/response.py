import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime

def get_user_context():
    """Get the user's profile data from session state"""
    if 'user_data' not in st.session_state:
        return "No user profile data available. Please complete the onboarding process first."
    
    user_data = st.session_state.user_data
    context = """User Profile Information:
    - Country: {country}
    - Age: {age}
    - Gender: {gender}
    - Marital Status: {marital_status}
    - Education Level: {education_level}
    - Employment Status: {employment_status}
    - Services Interested In: {services_needed}
    - Purpose: {purpose}
    """.format(
        country=user_data.get('country', 'Not specified'),
        age=user_data.get('age', 'Not specified'),
        gender=user_data.get('gender', 'Not specified'),
        marital_status=user_data.get('marital_status', 'Not specified'),
        education_level=user_data.get('education_level', 'Not specified'),
        employment_status=user_data.get('employment_status', 'Not specified'),
        services_needed=", ".join(user_data.get('services_needed', [])),
        purpose=user_data.get('purpose', 'Not specified')
    )
    return context

def get_system_prompt():
    """Generate a system prompt with user context"""
    user_context = get_user_context()
    
    return f"""
    You are AfriDesk, an AI assistant that helps citizens navigate government services in Africa. 
    
    User's Profile:
    {user_context}
    
    Your role is to provide personalized information based on the user's profile, including:
    - Government services and procedures relevant to their needs
    - Required documents and eligibility criteria
    - Office locations and working hours in their country
    - Application processes and fees
    - Any benefits or assistance programs they might qualify for
    
    Guidelines:
    1. Always consider the user's profile information when responding
    2. Be specific about requirements based on their country and personal circumstances
    3. Provide step-by-step guidance when explaining processes
    4. If a question is outside your knowledge, direct them to the appropriate government office
    5. Be clear about any deadlines, fees, or timeframes
    6. Use simple, easy-to-understand language
    7. Be patient and understanding of the user's situation
    8. If the user needs to visit an office, provide the nearest location if possible
    
    Current Date: {datetime.now().strftime('%Y-%m-%d')}
    """

# Common government services knowledge base
GOV_SERVICES_KNOWLEDGE = {
    "passport application": {
        "description": "Process for applying for a new passport or renewing an existing one",
        "required_documents": [
            "Completed application form",
            "Original and copy of national ID/birth certificate",
            "Passport photos (usually 2-4 copies)",
            "Payment receipt"
        ],
        "processing_time": "2-4 weeks (may vary by country)",
        "fees": "Varies by country and passport type"
    },
    "business registration": {
        "description": "Steps to register a new business",
        "required_documents": [
            "Business name reservation certificate",
            "Articles of Association",
            "ID copies of directors/shareholders",
            "Proof of business address"
        ],
        "processing_time": "1-3 weeks",
        "fees": "Varies by business type and country"
    },
    "national_id": {
        "description": "Application for national identity card",
        "required_documents": [
            "Birth certificate",
            "Proof of citizenship",
            "Passport photos",
            "Completed application form"
        ],
        "processing_time": "2-6 weeks",
        "fees": "Usually minimal or free for first-time applicants"
    }
}

def get_ai_response(prompt, api_key):
    """Get response from Gemini API with local fallback"""
    # Check if we should use local responses (if API key is invalid or quota exceeded)
    if not api_key or api_key == 'your_gemini_api_key_here':
        return get_local_response(prompt)
    
    try:
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Initialize the model with the latest version
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
        # Create chat history if it doesn't exist
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Add system prompt to the chat history if it's the first message
        if not st.session_state.chat_history:
            system_prompt = get_system_prompt()
            st.session_state.chat_history.append({"role": "user", "parts": [system_prompt]})
            st.session_state.chat_history.append({"role": "model", "parts": ["I understand your profile and am ready to help you with government services. How can I assist you today?"]})
        
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "parts": [prompt]})
        
        # Generate response with safety settings
        response = model.generate_content(
            st.session_state.chat_history,
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 2048,
            },
            safety_settings=[
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
            ]
        )
        
        # Get the response text safely
        try:
            response_text = response.text
        except Exception as e:
            st.error(f"Error getting response: {str(e)}")
            return get_local_response(prompt)
        
        # Add model response to chat history
        st.session_state.chat_history.append({"role": "model", "parts": [response_text]})
        
        return response_text
        
    except Exception as e:
        # If we hit a quota error or other API error, fall back to local responses
        return get_local_response(prompt)

def display_response(api_key=None):
    """Main function to handle the chat interface"""
    # Add custom CSS for chat interface
    st.markdown("""
    <style>
        /* Chat message containers */
        .stChatMessage {
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            max-width: 85%;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        /* User messages */
        [data-testid="stChatMessage"][data-message-author="user"] {
            background-color: #4f46e5;
            color: white;
            margin-left: auto;
            margin-right: 0;
            border-bottom-right-radius: 4px;
        }
        
        /* Assistant messages */
        [data-testid="stChatMessage"][data-message-author="assistant"] {
            background-color: #f8f9fa;
            color: #1e293b;
            border: 1px solid #dee2e6;
            margin-right: auto;
            margin-left: 0;
            border-bottom-left-radius: 4px;
        }
        
        /* Chat input */
        .stChatInputContainer {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid #dee2e6;
            margin-top: 1rem;
        }
        
        /* Clear chat button */
        .stButton > button {
            width: 100%;
            background-color: #e9ecef;
            color: #4f46e5;
            border: 1px solid #dee2e6;
        }
        
        .stButton > button:hover {
            background-color: #f1f5f9;
            border-color: #cbd5e1;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Display welcome message
    st.title("💬 Ask AfriDesk")
    st.caption("🚀 Your government services assistant")
    
    # Check if user has completed onboarding
    if 'user_data' not in st.session_state:
        st.warning("Please complete the onboarding process first to get personalized assistance.")
        if st.button("Go to Onboarding"):
            st.session_state['current_page'] = 'onboarding'
            st.rerun()
        return
    
    # Initialize chat history if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm AfriDesk, your government services assistant. I see you're from " + 
             st.session_state.user_data.get('country', 'your country') + 
             ". How can I help you with government services today?"}
        ]
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Accept user input with a unique key
    if prompt := st.chat_input("What would you like to know about government services?", key="main_chat_input"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = get_ai_response(prompt, api_key)
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Add a clear chat button with custom styling
    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)  # Add some space
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm AfriDesk, your government services assistant. How can I help you with government services today?"}
        ]
        st.experimental_rerun()

    # Add feedback section
    st.markdown("---")
    st.markdown("### Was this information helpful?")
    col1, col2 = st.columns(2)
    
    if 'feedback_submitted' not in st.session_state:
        st.session_state.feedback_submitted = False
    
    if not st.session_state.feedback_submitted:
        with col1:
            if st.button("👍 Yes", key="feedback_yes"):
                st.session_state.feedback_submitted = True
                st.success("Thank you for your feedback!")
        
        with col2:
            if st.button("👎 No", key="feedback_no"):
                st.session_state.show_feedback_form = True
                
        if st.session_state.get('show_feedback_form', False):
            feedback = st.text_area("We're sorry to hear that. Could you tell us how we can improve? (optional)", 
                                 key="feedback_text")
            if st.button("Submit Feedback", key="submit_feedback"):
                st.session_state.feedback_submitted = True
                if feedback:
                    # Here you would typically log the feedback
                    print(f"User feedback: {feedback}")
                    # In a real app, you would save this to a database
                st.success("Thank you for helping us improve our service!")
            # Save feedback if provided
            if 'user_data' in st.session_state and feedback:
                save_feedback(st.session_state.user_data, feedback)

def get_local_response(prompt):
    """Generate a response using local knowledge base"""
    # Convert prompt to lowercase for case-insensitive matching
    prompt_lower = prompt.lower()
    
    # Check for common government service queries
    if any(term in prompt_lower for term in ['passport', 'id', 'identification']):
        return """I can help with passport and ID services. Here's what you need to know:
        
        - **Passport Application**: 
          - Required documents: Birth certificate, Proof of citizenship, Passport photos, Completed application form
          - Processing time: 2-6 weeks
          - Fees: Varies by country
          
        - **National ID Card**:
          - Required documents: Birth certificate, Proof of residence, Passport photo
          - Processing time: 2-4 weeks
          - Fees: Usually free for first-time applicants
          
        Would you like more specific information about any of these services?"""
    
    elif any(term in prompt_lower for term in ['health', 'hospital', 'clinic', 'nhis']):
        return """I can provide information about health services:
        
        - **Clinic Registration**:
          - Required documents: ID document, Proof of residence
          - Processing time: Same day
          - Fees: Free for citizens
          
        - **Health Insurance (NHIS)**:
          - Required documents: ID document, Proof of residence, Passport photo
          - Processing time: 1-2 weeks
          - Fees: From GHS 30 annually (Ghana example)
          
        - **Chronic Medication**:
          - Required documents: ID document, Prescription
          - Processing time: Same day
          - Fees: Covered by insurance or free for citizens"""
    
    elif any(term in prompt_lower for term in ['education', 'school', 'university', 'student']):
        return """Here's information about education services:
        
        - **School Registration**:
          - Required documents: Birth certificate, Previous school reports, Passport photos
          - Processing time: 1-2 weeks
          
        - **University Applications**:
          - Required documents: High school certificate, ID document, Application form
          - Processing time: 4-8 weeks
          - Fees: Varies by institution
          
        - **Scholarships/Bursaries**:
          - Required documents: Academic records, ID document, Proof of income
          - Processing time: 2-3 months"""
    
    elif any(term in prompt_lower for term in ['business', 'company', 'register business', 'tax']):
        return """Here's information about business registration and tax services:
        
        - **Business Registration**:
          - Required documents: ID copies, Proof of address, Company name reservation
          - Processing time: 1-2 weeks
          - Fees: Varies by country and business type
          
        - **Tax Registration**:
          - Required documents: ID document, Business registration documents
          - Processing time: 2-3 weeks
          - Fees: Usually free
          
        - **Tax Filing**:
          - Required documents: Financial records, Previous tax returns
          - Processing time: 1-2 weeks
          - Fees: Free for e-filing"""
    
    # Default response if no specific match found
    return """I'm currently operating with limited functionality. Here are some topics I can help with:
    
    - Passport and ID services
    - Health services and insurance
    - Education and student services
    - Business registration and tax services
    
    Please ask about any of these topics, and I'll provide the information I have available."""

def save_feedback(user_data, feedback):
    """Save user feedback"""
    # This would typically save to a database
    pass
