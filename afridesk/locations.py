import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import json
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# Sample data - in a real app, this would come from a database
GOVERNMENT_OFFICES = {
    "Nairobi": [
        {"name": "Kenyatta National Hospital", "type": "Hospital", "lat": -1.3048, "lon": 36.8154, "address": "Hospital Road, Nairobi"},
        {"name": "Mama Lucy Kibaki Hospital", "type": "Hospital", "lat": -1.3045, "lon": 36.9012, "address": "Kangundo Road, Nairobi"},
        {"name": "Nairobi County Health Department", "type": "Health Center", "lat": -1.2833, "lon": 36.8167, "address": "City Hall, Nairobi"},
    ],
    "Lagos": [
        {"name": "Lagos University Teaching Hospital (LUTH)", "type": "Hospital", "lat": 6.5244, "lon": 3.3892, "address": "Idi-Araba, Lagos"},
        {"name": "Lagos State Primary Health Care Board", "type": "Health Center", "lat": 6.5244, "lon": 3.3792, "address": "Ikeja, Lagos"},
        {"name": "Maternal and Child Centre", "type": "Clinic", "lat": 6.4541, "lon": 3.3947, "address": "Amuwo Odofin, Lagos"},
    ],
    "Cairo": [
        {"name": "Kasr Al Ainy Hospital", "type": "Hospital", "lat": 30.0318, "lon": 31.2266, "address": "Manial, Cairo"},
        {"name": "Ain Shams University Hospital", "type": "Hospital", "lat": 30.0771, "lon": 31.2859, "address": "Abbaseya, Cairo"},
        {"name": "Ministry of Health and Population", "type": "Health Center", "lat": 30.0444, "lon": 31.2357, "address": "Cairo Governorate 11511, Egypt"},
    ],
    "Johannesburg": [
        {"name": "Chris Hani Baragwanath Hospital", "type": "Hospital", "lat": -26.2485, "lon": 27.9083, "address": "Soweto, Johannesburg"},
        {"name": "Charlotte Maxeke Hospital", "type": "Hospital", "lat": -26.1876, "lon": 28.0444, "address": "Parktown, Johannesburg"},
        {"name": "South African Department of Health", "type": "Health Center", "lat": -25.7449, "lon": 28.1878, "address": "Pretoria, South Africa"},
    ]
}

def get_coordinates(location):
    """Get latitude and longitude for a location using geopy"""
    try:
        geolocator = Nominatim(user_agent="afridesk_app")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        location_data = geocode(location)
        if location_data:
            return location_data.latitude, location_data.longitude
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        st.warning(f"Could not get location data: {str(e)}")
    return None, None

def create_office_map(offices, center_lat=None, center_lon=None):
    """Create a folium map with office markers"""
    if not offices:
        return None
        
    # Use first office as center if no center provided
    if center_lat is None or center_lon is None:
        center_lat = offices[0]["lat"]
        center_lon = offices[0]["lon"]
    
    # Create map centered on the first office
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles='OpenStreetMap')
    
    # Add markers for each office
    for office in offices:
        popup_text = f"<b>{office['name']}</b><br>{office['type']}<br>{office['address']}"
        folium.Marker(
            [office['lat'], office['lon']],
            popup=popup_text,
            tooltip=office['name'],
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
    
    return m

def government_offices():
    st.title("Government Office Locations")
    st.markdown("Find government offices and service centers near you.")
    
    # Get user's registration data
    user_data = st.session_state.get('user_data', {})
    user_country = user_data.get('country', 'Nigeria')  # Default to Nigeria
    user_city = user_data.get('city', 'Lagos')  # Default to Lagos
    user_address = f"{user_city}, {user_country}"
    
    st.write(f"### Showing offices near: {user_address}")
    
    # Try to get coordinates for user's location
    user_lat, user_lon = get_coordinates(user_address)
    
    # Get user's selected services from registration
    user_services = set(st.session_state.get('user_data', {}).get('services_needed', []))
    
    # Map service categories to office types
    service_to_office_type = {
        'health': ['Hospital', 'Health Center', 'Clinic'],
        'education': ['School', 'University', 'Education Office'],
        'immigration': ['Immigration', 'Passport Office'],
        'government': ['Government Office', 'State Government', 'County Government']
    }
    
    # Get relevant office types based on user's selected services
    relevant_office_types = set()
    for service in user_services:
        relevant_office_types.update(service_to_office_type.get(service.lower(), []))
    
    # If no specific services selected, show all office types
    if not relevant_office_types:
        relevant_office_types = None
    
    # Get offices for user's city or default city, filtered by relevant types
    offices = []
    for city_offices in GOVERNMENT_OFFICES.values():
        for office in city_offices:
            if relevant_office_types is None or any(office_type.lower() in office['type'].lower() 
                                                 for office_type in relevant_office_types):
                offices.append(office)
    
    # If we have user's location, sort offices by distance
    if user_lat and user_lon:
        for office in offices:
            office['distance'] = ((office['lat'] - user_lat) ** 2 + (office['lon'] - user_lon) ** 2) ** 0.5
        offices.sort(key=lambda x: x.get('distance', float('inf')))
    
    # Create and display the map
    if offices:
        map_center_lat = user_lat if user_lat else offices[0]['lat']
        map_center_lon = user_lon if user_lon else offices[0]['lon']
        
        m = create_office_map(offices[:10], map_center_lat, map_center_lon)
        if m:
            folium_static(m, width=700, height=500)
        
        # Display office list with interactive map
        st.subheader("Nearby Government Offices")
        
        # Create a container for the map
        map_placeholder = st.empty()
        
        # Create the initial map
        m = create_office_map(offices[:10], map_center_lat, map_center_lon)
        if m:
            folium_static(m, width=700, height=500)
        
        # Display office list with click handlers
        for idx, office in enumerate(offices[:10]):  # Show top 10 closest offices
            with st.expander(f"{office['name']} - {office['type']}"):
                st.write(f"**Address:** {office['address']}")
                st.write(f"**Type:** {office['type']}")
                if 'distance' in office and user_lat and user_lon:
                    st.write(f"**Distance:** ~{office['distance']*111:.1f} km from your location")
                
                # Add a button to focus on this office
                if st.button("Show on Map", key=f"show_office_{idx}"):
                    # Create a new map centered on this office
                    m = folium.Map(
                        location=[office['lat'], office['lon']], 
                        zoom_start=15,
                        tiles='OpenStreetMap'
                    )
                    # Add a marker for the selected office
                    folium.Marker(
                        [office['lat'], office['lon']],
                        popup=f"<b>{office['name']}</b><br>{office['type']}<br>{office['address']}",
                        tooltip=office['name'],
                        icon=folium.Icon(color='blue', icon='info-sign')
                    ).add_to(m)
                    
                    # Display the updated map
                    folium_static(m, width=700, height=500)
    else:
        st.warning("No government offices found in your area.")
        
    # Add a search box for other locations
    st.markdown("---")
    st.subheader("Search Other Locations")
    search_query = st.text_input("Enter a city or address to search:", user_address)
    
    if search_query and search_query != user_address:
        search_lat, search_lon = get_coordinates(search_query)
        if search_lat and search_lon:
            # Find nearby offices (simple distance-based)
            for office in offices:
                office['distance'] = ((office['lat'] - search_lat) ** 2 + (office['lon'] - search_lon) ** 2) ** 0.5
            offices.sort(key=lambda x: x.get('distance', float('inf')))
            
            # Show map for searched location
            m = create_office_map(offices[:10], search_lat, search_lon)
            if m:
                folium_static(m, width=700, height=500)
        else:
            st.warning("Could not find the specified location. Please try a different search term.")
    
    # Add office management section for admins
    # if st.checkbox("Show Admin Options", False, key="show_admin_options"):
    #     # st.subheader("Add New Office")
    #     with st.form("add_office_form"):
    #         new_office = {
    #             "name": st.text_input("Office Name"),
    #             "type": st.selectbox("Office Type", ["Immigration", "State Government", "County Government", "Other"]),
    #             "address": st.text_area("Full Address"),
    #             "lat": st.number_input("Latitude", format="%.6f"),
    #             "lon": st.number_input("Longitude", format="%.6f")
    #         }
    #         if st.form_submit_button("Add Office"):
    #             if new_office["name"] and new_office["address"]:
    #                 # In a real app, you would save this to a database
    #                 st.success(f"Added {new_office['name']} to the database!")
    #             else:
    #                 st.error("Please fill in all required fields.")
    #         st.markdown("**Services:** Document processing, Information, Applications")

def add_office_ui():
    st.sidebar.markdown("### Add a New Office")
    with st.sidebar.form("office_form"):
        name = st.text_input("Office Name")
        office_type = st.selectbox("Office Type", ["National Government", "County/State", "Local Government"])
        address = st.text_area("Full Address")
        lat = st.number_input("Latitude")
        lon = st.number_input("Longitude")
        
        if st.form_submit_button("Submit"):
            # In a real app, this would save to a database
            st.success("Office added successfully!")

# Add the ability to add new offices (for admin use)
# if st.sidebar.checkbox("Add New Office", False):
#     add_office_ui()
