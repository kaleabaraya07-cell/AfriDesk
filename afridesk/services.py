import os
import streamlit as st
import google.generativeai as genai
import json
from dotenv import load_dotenv

load_dotenv()

# Local service data as fallback, categorized by service type
LOCAL_SERVICES = {
    "Nigeria": {
        "services": [
            # Health Services
            {
                "name": "National Health Insurance Scheme (NHIS) Enrollment",
                "description": "Enroll in the national health insurance program for affordable healthcare services.",
                "required_documents": ["Means of identification", "Passport photograph", "Proof of address"],
                "processing_time": "1-2 weeks",
                "fees": "From N15,000 annually",
                "category": "Health Services"
            },
            {
                "name": "Primary Healthcare Center Registration",
                "description": "Register with your local primary healthcare center for basic medical services.",
                "required_documents": ["Proof of residence", "Means of identification"],
                "processing_time": "Same day",
                "fees": "Free for basic services",
                "category": "Health Services"
            },
            # Education Services
            {
                "name": "JAMB Registration",
                "description": "Register for Joint Admissions and Matriculation Board examinations for tertiary education.",
                "required_documents": ["O'Level results", "Birth certificate", "Passport photograph"],
                "processing_time": "1 day",
                "fees": "N4,700 for UTME",
                "category": "Education Services"
            },
            {
                "name": "WAEC Registration",
                "description": "Register for West African Examinations Council (WAEC) exams.",
                "required_documents": ["Birth certificate", "Passport photograph"],
                "processing_time": "1 day",
                "fees": "N18,000 - N25,000",
                "category": "Education Services"
            },
            # Business Registration
            {
                "name": "Corporate Affairs Commission (CAC) Business Registration",
                "description": "Register your business with the Corporate Affairs Commission.",
                "required_documents": ["Business name reservation", "Passport photographs", "Means of identification"],
                "processing_time": "1-2 weeks",
                "fees": "From N10,000",
                "category": "Business Registration"
            },
            {
                "name": "Business Premises Registration",
                "description": "Register your business premises with the local government.",
                "required_documents": ["CAC certificate", "Proof of address", "Tax identification number"],
                "processing_time": "1 week",
                "fees": "Varies by location",
                "category": "Business Registration"
            },
            # Tax Services
            {
                "name": "Tax Identification Number (TIN) Registration",
                "description": "Register for a Tax Identification Number with the Federal Inland Revenue Service.",
                "required_documents": ["Means of identification", "Proof of address", "Passport photograph"],
                "processing_time": "24-48 hours",
                "fees": "Free",
                "category": "Tax Services"
            },
            {
                "name": "Filing Annual Tax Returns",
                "description": "File your annual tax returns with the Federal Inland Revenue Service.",
                "required_documents": ["TIN", "Financial statements", "Previous tax returns"],
                "processing_time": "1-2 days",
                "fees": "Varies by income",
                "category": "Tax Services"
            },
            # National ID
            {
                "name": "National ID Card Registration",
                "description": "Register for or replace your National Identity Card.",
                "required_documents": ["Birth certificate/age declaration", "Proof of address", "Local government identification"],
                "processing_time": "2-6 weeks",
                "fees": "Free",
                "category": "National ID"
            }
        ]
    },
    "Kenya": {
        "services": [
            # Health Services
            {
                "name": "NHIF Registration",
                "description": "Enroll in the National Hospital Insurance Fund for healthcare coverage.",
                "required_documents": ["National ID", "Passport photo", "KRA PIN"],
                "processing_time": "1-2 weeks",
                "fees": "From KSh 500 monthly",
                "category": "Health Services"
            },
            {
                "name": "Linda Mama Maternity Program",
                "description": "Free maternity services for expectant mothers.",
                "required_documents": ["National ID", "NHIF card"],
                "processing_time": "Same day registration",
                "fees": "Free",
                "category": "Health Services"
            },
            # Education Services
            {
                "name": "KUCCPS University Application",
                "description": "Apply for university placement through the Kenya Universities and Colleges Central Placement Service.",
                "required_documents": ["KCSE results slip", "National ID", "Passport photo"],
                "processing_time": "2-4 weeks",
                "fees": "KSh 1,500",
                "category": "Education Services"
            },
            {
                "name": "KNEC KCPE/KCSE Registration",
                "description": "Register for national primary and secondary education examinations.",
                "required_documents": ["Birth certificate", "Passport photo", "Previous school records"],
                "processing_time": "1-2 weeks",
                "fees": "KSh 1,000 - KSh 1,500",
                "category": "Education Services"
            },
            # Business Registration
            {
                "name": "eCitizen Business Registration",
                "description": "Register a new business through the eCitizen portal.",
                "required_documents": ["National ID", "KRA PIN", "Passport photo", "Business name search"],
                "processing_time": "1-3 days",
                "fees": "From KSh 10,000",
                "category": "Business Registration"
            },
            {
                "name": "Single Business Permit",
                "description": "Obtain a business permit from the county government.",
                "required_documents": ["Business registration certificate", "KRA PIN certificate", "Lease agreement"],
                "processing_time": "1-2 weeks",
                "fees": "Varies by business type and size",
                "category": "Business Registration"
            },
            # Tax Services
            {
                "name": "KRA PIN Registration",
                "description": "Register for a Personal Identification Number with the Kenya Revenue Authority.",
                "required_documents": ["National ID", "Passport photo"],
                "processing_time": "24 hours",
                "fees": "Free",
                "category": "Tax Services"
            },
            {
                "name": "File Tax Returns",
                "description": "File your annual tax returns with the Kenya Revenue Authority.",
                "required_documents": ["KRA PIN", "Monthly pay slips", "P9 form"],
                "processing_time": "1-2 days",
                "fees": "Free",
                "category": "Tax Services"
            }
        ]
    },
    "Ghana": {
        "services": [
            # Health Services
            {
                "name": "National Health Insurance Scheme (NHIS) Registration",
                "description": "Enroll in Ghana's national health insurance program.",
                "required_documents": ["Ghana Card", "Proof of residence", "Passport photo"],
                "processing_time": "1-2 weeks",
                "fees": "From GHS 30 annually",
                "category": "Health Services"
            },
            {
                "name": "Community-based Health Planning and Services (CHPS)",
                "description": "Access primary healthcare services in your community.",
                "required_documents": ["NHIS card"],
                "processing_time": "Same day",
                "fees": "Free with NHIS",
                "category": "Health Services"
            },
            # Education Services
            {
                "name": "WASSCE Registration",
                "description": "Register for West African Senior School Certificate Examination.",
                "required_documents": ["BECE certificate", "Birth certificate", "Passport photo"],
                "processing_time": "2 weeks",
                "fees": "GHS 400-600",
                "category": "Education Services"
            },
            {
                "name": "University of Ghana Applications",
                "description": "Apply for undergraduate programs at the University of Ghana.",
                "required_documents": ["WASSCE results", "Birth certificate", "Passport photo"],
                "processing_time": "4-6 weeks",
                "fees": "GHS 200-400",
                "category": "Education Services"
            },
            # Business Registration
            {
                "name": "Registrar General's Department Business Registration",
                "description": "Register your business with the Registrar General's Department.",
                "required_documents": ["Business name certificate", "Form 3", "Passport photo", "ID copy"],
                "processing_time": "1-2 weeks",
                "fees": "From GHS 50",
                "category": "Business Registration"
            },
            {
                "name": "Ghana Investment Promotion Centre (GIPC) Registration",
                "description": "Register your foreign-owned business with GIPC.",
                "required_documents": ["Business registration certificate", "Business plan", "Passport copies"],
                "processing_time": "2-3 weeks",
                "fees": "From $1,000",
                "category": "Business Registration"
            },
            # Tax Services
            {
                "name": "Ghana Revenue Authority (GRA) TIN Registration",
                "description": "Register for a Tax Identification Number.",
                "required_documents": ["Ghana Card/Passport", "Proof of address"],
                "processing_time": "24-48 hours",
                "fees": "Free",
                "category": "Tax Services"
            },
            {
                "name": "File Annual Tax Returns",
                "description": "File your annual tax returns with the GRA.",
                "required_documents": ["TIN certificate", "Financial statements", "Previous tax returns"],
                "processing_time": "1-2 days",
                "fees": "Free",
                "category": "Tax Services"
            },
            # National ID
            {
                "name": "Ghana Card Registration",
                "description": "Register for the national identification card.",
                "required_documents": ["Birth certificate", "Proof of residence", "Passport photo"],
                "processing_time": "2-4 weeks",
                "fees": "Free",
                "category": "National ID"
            }
        ]
    },
    "South Africa": {
        "services": [
            # Health Services
            {
                "name": "Clinic Registration",
                "description": "Register at your local clinic for primary healthcare services.",
                "required_documents": ["ID document", "Proof of residence", "Clinic card (if applicable)"],
                "processing_time": "Same day",
                "fees": "Free for South African citizens",
                "category": "Health Services"
            },
            {
                "name": "Chronic Medication Collection",
                "description": "Access to chronic medication at designated facilities.",
                "required_documents": ["ID document", "Clinic card", "Prescription"],
                "processing_time": "Same day",
                "fees": "Free for South African citizens",
                "category": "Health Services"
            },
            # Education Services
            {
                "name": "Matric Certificate Application",
                "description": "Apply for your National Senior Certificate (NSC) or replacement certificate.",
                "required_documents": ["ID document", "Previous school reports", "Affidavit if lost"],
                "processing_time": "6-8 weeks",
                "fees": "R141 for replacement",
                "category": "Education Services"
            },
            {
                "name": "NSFAS Bursary Application",
                "description": "Apply for National Student Financial Aid Scheme funding for tertiary education.",
                "required_documents": ["ID document", "Matric certificate", "Parents/guardian proof of income"],
                "processing_time": "3-6 months",
                "fees": "Free application",
                "category": "Education Services"
            },
            # Business Registration
            {
                "name": "CIPC Company Registration",
                "description": "Register a new company with the Companies and Intellectual Property Commission.",
                "required_documents": ["ID copies of directors", "Proof of address", "Company name reservation"],
                "processing_time": "5-7 working days",
                "fees": "From R125",
                "category": "Business Registration"
            },
            {
                "name": "SARS Business Tax Registration",
                "description": "Register your business for tax with the South African Revenue Service.",
                "required_documents": ["ID document", "Proof of address", "Business registration documents"],
                "processing_time": "21 working days",
                "fees": "Free",
                "category": "Business Registration"
            },
            # Tax Services
            {
                "name": "eFiling Registration",
                "description": "Register for SARS eFiling to submit tax returns online.",
                "required_documents": ["ID document", "Proof of residence", "Banking details"],
                "processing_time": "24-48 hours",
                "fees": "Free",
                "category": "Tax Services"
            },
            {
                "name": "Income Tax Return Submission",
                "description": "File your annual income tax return with SARS.",
                "required_documents": ["IRP5/IT3(a) certificate", "Medical aid certificate", "Retirement annuity certificates"],
                "processing_time": "7-21 working days",
                "fees": "Free",
                "category": "Tax Services"
            },
            # National ID
            {
                "name": "Smart ID Card Application",
                "description": "Apply for the new Smart ID card.",
                "required_documents": ["Green barcoded ID book", "Birth certificate", "Proof of residence"],
                "processing_time": "10-14 working days",
                "fees": "R140",
                "category": "National ID"
            }
        ]
    }
}

def get_local_services(country, service_categories=None):
    """
    Get local services for a specific country, optionally filtered by service categories
    
    Args:
        country (str): The country to get services for
        service_categories (list, optional): List of service categories to filter by
        
    Returns:
        list: List of services matching the criteria
    """
    # Get services for the specified country
    country_data = LOCAL_SERVICES.get(country, {})
    services = country_data.get('services', [])
    
    # If no services found for the country, use the first available country's services
    if not services and LOCAL_SERVICES:
        first_country = next(iter(LOCAL_SERVICES.values()))
        services = first_country.get('services', [])
    
    # Filter by service categories if provided
    if service_categories:
        # Normalize categories for case-insensitive comparison
        categories = [cat.lower() for cat in service_categories]
        services = [
            service for service in services 
            if service.get('category', '').lower() in categories
            or any(cat.lower() in service.get('name', '').lower() for cat in service_categories)
        ]
    
    return services

def get_personalized_services(user_data, api_key):
    """
    Get personalized services based on user's country and preferences using Google's Gemini API
    with fallback to local data if API fails
    """
    country = user_data.get('country', 'Nigeria')  # Default to Nigeria if not specified
    services_needed = user_data.get('services_needed', [])
    
    try:
        print("API Key: ", api_key)
        if not api_key or api_key == 'your_gemini_api_key_here':
            # print error message
            print("No API key provided")
            raise ValueError("No API key provided")
            
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        services_needed_str = ", ".join(services_needed)
        
        prompt = f"""
        Based on the following user information, provide a list of relevant government services in {country}.
        
        User Preferences:
        - Country: {country}
        - Interested Services: {services_needed_str}
        
        Please provide:
        1. A list of 5-7 relevant government services
        2. A brief description of each service
        3. Required documents for each service
        4. Estimated processing time
        
        Format the response as a valid JSON object with the following structure:
        {{
            "services": [
                {{
                    "name": "Service Name",
                    "description": "Brief description",
                    "required_documents": ["Document 1", "Document 2"],
                    "processing_time": "X-X days/weeks",
                    "fees": "Cost if any"
                }}
            ]
        }}
        
        IMPORTANT: Only return the JSON object, no additional text or markdown formatting.
        """
        
        # Initialize the Gemini model
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Generate content
        print("prompt: ", prompt)
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Sometimes Gemini includes markdown code blocks, so we'll remove them
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0].strip()
            
        # Parse the response
        services_data = json.loads(response_text)
        return services_data
        
    except json.JSONDecodeError as e:
        st.error("Error parsing the response from Gemini. Falling back to local service data.")
        st.error(f"Response content: {response_text if 'response_text' in locals() else 'No response'}")
        return {"services": get_locals_services(country, services_needed)}
    except Exception as e:
        st.warning(f"Using local service data as fallback: {str(e)}")
        return {"services": get_local_services(country, services_needed)}

def services_list():
    st.title("Government Services")
    
    # Check if we should show service details
    if st.session_state.get('show_service_details', False) and 'selected_service' in st.session_state:
        service_details()
        return
    
    # Get user data from session state - check both user_data and user_profile_data
    user_data = st.session_state.get('user_data', {})
    profile_data = st.session_state.get('user_profile_data', {})
    
    # If we have profile data but not user_data, use profile_data
    if not user_data and profile_data:
        user_data = profile_data
    
    if not user_data:
        st.warning("Please complete the onboarding process to get personalized service recommendations.")
        st.session_state['current_page'] = 'welcome'
        st.rerun()
        return
        
    # Show appropriate heading based on context
    if st.session_state.get('came_from_profile', False):
        st.markdown("### 🎯 Personalized Services Based on Your Profile")
    else:
        st.markdown("### Browse Available Government Services")
    
    # Try to get API key from environment or session state
    api_key = os.getenv("GEMINI_API_KEY") or st.session_state.get('gemini_api_key')
    
    if not api_key or api_key == 'your_gemini_api_key_here':
        st.warning("No Gemini API key found. Using local service data instead.")
        # Fall back to local services
        country = user_data.get('country', 'Nigeria')
        services_needed = user_data.get('needs', [])
        services_data = {"services": get_local_services(country, services_needed)}
        st.session_state['services_data'] = services_data
        
    # Show loading state
    with st.spinner("Analyzing your profile to find the most relevant services..."):
        # Check if we already have services data
        if 'services_data' not in st.session_state:
            try:
                # Get personalized services from Gemini API
                services_data = get_personalized_services(user_data, api_key)
                
                if not services_data or 'services' not in services_data:
                    raise ValueError("No services data returned from API")
                    
                # Store services in session state for details view
                st.session_state['services_data'] = services_data
                
            except Exception as e:
                st.error("Sorry, we encountered an issue getting personalized recommendations.")
                st.warning("Showing local services instead.")
                # Fall back to local services
                country = user_data.get('country', 'Nigeria')
                services_needed = user_data.get('needs', [])
                services_data = {"services": get_local_services(country, services_needed)}
                st.session_state['services_data'] = services_data
        else:
            services_data = st.session_state['services_data']
            
        # Display services with personalized message if coming from profile
        country = user_data.get('country', 'your location')
        if st.session_state.get('came_from_profile', False):
            st.success(f"🎯 Found {len(services_data['services'])} personalized services in {country} based on your profile:")
            # Show a summary of why these services were selected
            if 'needs' in user_data and user_data['needs']:
                st.info(f"✨ Based on your interests: {', '.join(user_data['needs'])}")
            # Reset the flag
            st.session_state['came_from_profile'] = False
        else:
            st.success(f"Found {len(services_data['services'])} services in {country}:")
        
        # Show a message if services were filtered by profile data
        if profile_data and 'needs' in profile_data and profile_data['needs']:
            st.info(f"✨ Personalized for: {', '.join(profile_data['needs'])}")
        
        # Create columns for service cards
        cols = st.columns(1)  # Single column for better readability of detailed cards
        
        for idx, service in enumerate(services_data['services']):
            with cols[0]:  # Always use first (and only) column
                with st.expander(f"🔹 {service.get('name', 'Service')}", expanded=False):
                    # Service description
                    st.markdown(f"**Description:** {service.get('description', 'No description available')}")
                    
                    # Why this service is relevant (if available)
                    if 'why_relevant' in service and service['why_relevant']:
                        st.markdown(f"**Why this matters for you:** {service['why_relevant']}")
                    
                    # Service details in a more organized way
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Processing Time**")
                        st.info(f"⏱️ {service.get('processing_time', 'Varies')}")
                    with col2:
                        st.markdown("**Fees**")
                        st.info(f"💰 {service.get('fees', 'Varies')}")
                    
                    # Required documents (if available)
                    if 'required_documents' in service and service['required_documents']:
                        with st.expander("📋 Required Documents", expanded=False):
                            for doc in service['required_documents']:
                                st.markdown(f"- {doc}")
                    
                    # Category tag (if available)
                    if 'category' in service and service['category']:
                        st.markdown(f"**Category:** `{service['category']}`")
                    
                    # View Details button
                    if st.button("View Full Details", key=f"details_{idx}", use_container_width=True):
                        st.session_state['selected_service'] = service
                        st.session_state['show_service_details'] = True
                        st.rerun()

def service_details():
    """Show detailed information about a selected service"""
    st.title("Service Details")
    
    if 'selected_service' not in st.session_state:
        st.error("No service selected. Please go back and select a service.")
        if st.button("← Back to Services"):
            st.session_state['show_service_details'] = False
            st.rerun()
        return
    
    service = st.session_state['selected_service']
    
    # Service header with name and category
    st.markdown(f"## {service.get('name', 'Service Details')}")
    
    # Display category if available
    if 'category' in service and service['category']:
        st.markdown(f"**Category:** {service['category']}")
    
    # Description
    st.markdown("### 📝 Description")
    st.write(service.get('description', 'No description available.'))
    
    # Why this service is relevant (if available)
    if 'why_relevant' in service and service['why_relevant']:
        st.markdown("### 💡 Why This Matters for You")
        st.info(service['why_relevant'])
    
    # Key details in columns
    st.markdown("### ℹ️ Key Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**⏱️ Processing Time**")
        st.info(f"{service.get('processing_time', 'Varies')}")
        
        if 'eligibility' in service and service['eligibility']:
            st.markdown("**✅ Eligibility**")
            st.info(service['eligibility'])
    
    with col2:
        st.markdown("**💰 Fees**")
        st.info(service.get('fees', 'Varies'))
        
        if 'website' in service and service['website']:
            st.markdown("**🌐 Website**")
            st.markdown(f"[{service['website']}]({service['website']})")
    
    # Required documents
    if 'required_documents' in service and service['required_documents']:
        st.markdown("### 📋 Required Documents")
        st.warning("Make sure you have these documents ready when applying:")
        for i, doc in enumerate(service['required_documents'], 1):
            st.markdown(f"{i}. **{doc}**")
    
    # Application process if available
    if 'application_process' in service and service['application_process']:
        st.markdown("### 📝 How to Apply")
        st.write(service['application_process'])
    
    # Additional notes if available
    if 'additional_notes' in service and service['additional_notes']:
        st.markdown("### 📌 Additional Notes")
        st.info(service['additional_notes'])
    
    # Back button at the bottom
    st.markdown("---")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("← Back to Services", use_container_width=True):
            st.session_state['show_service_details'] = False
            st.rerun()
    with col2:
        if 'website' in service and service['website']:
            st.link_button("🌐 Visit Official Website", service['website'], use_container_width=True)
