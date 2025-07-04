#!/usr/bin/env python3
"""
Simple test untuk delete API dengan login cookie
"""

import requests
import json

def test_delete_with_session():
    base_url = "http://localhost:5000"
    
    # Create session
    session = requests.Session()
    
    # Login via web form
    login_response = session.get(f"{base_url}/login")
    print(f"Get login page: {login_response.status_code}")
    
    # Post login credentials
    login_data = {
        'email': 'admin@telkom.com', 
        'password': 'admin123'
    }
    
    post_login = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
    print(f"Post login: {post_login.status_code}")
    print(f"Post login headers: {dict(post_login.headers)}")
    
    # Follow redirect if any
    if post_login.status_code in [302, 301]:
        redirect_url = post_login.headers.get('Location')
        print(f"Redirecting to: {redirect_url}")
        if redirect_url.startswith('/'):
            redirect_url = base_url + redirect_url
        redirect_response = session.get(redirect_url)
        print(f"Redirect response: {redirect_response.status_code}")
    
    # Test get properties to verify session
    props_response = session.get(f"{base_url}/api/admin/properties")
    print(f"\nGet properties status: {props_response.status_code}")
    
    if props_response.status_code == 200:
        data = props_response.json()
        properties = data.get('properties', [])
        print(f"Found {len(properties)} properties")
        
        if len(properties) > 0:
            # Try delete first property
            prop = properties[0]
            prop_id = prop['id']
            prop_type = prop['property_type']
            prop_title = prop['title']
            
            print(f"\nAttempting to delete: ID={prop_id}, Type={prop_type}, Title={prop_title}")
            
            delete_url = f"{base_url}/api/admin/property/{prop_type}/{prop_id}"
            print(f"Delete URL: {delete_url}")
            
            delete_response = session.delete(delete_url)
            print(f"Delete status: {delete_response.status_code}")
            print(f"Delete response: {delete_response.text}")
            
            # Verify deletion
            verify_response = session.get(f"{base_url}/api/admin/properties")
            if verify_response.status_code == 200:
                verify_data = verify_response.json()
                remaining_props = verify_data.get('properties', [])
                print(f"Properties after delete: {len(remaining_props)}")
                
                # Check if property was actually deleted
                still_exists = any(p['id'] == prop_id and p['property_type'] == prop_type for p in remaining_props)
                print(f"Property still exists: {still_exists}")
                print(f"Delete successful: {not still_exists}")
        else:
            print("No properties to delete")
    else:
        print(f"Failed to get properties: {props_response.text}")

if __name__ == "__main__":
    test_delete_with_session()
