
import streamlit as st 
import os 
import json
import datetime 
import requests 
import urllib3
from uuid import uuid4

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def inject_custom_css():
    with open('./assets/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

inject_custom_css()


def form_enrolment_request(first_name, phone_mobile, hospital, ward, unit, hhs, peer_group):
    request_body = {
        "messageId": uuid4().hex,
        "patient": {
            "first_name": first_name,
            "phone_mobile": phone_mobile
        },
        "participation": {
            "hospital": hospital,
            "ward": ward,
            "unit": unit,
            "hhs": hhs,
            "peer_group": peer_group
        }
    }
    return request_body


def send_enrolment_request(body): 
      payload = json.dumps(body)
      response = requests.request("POST",
                        "https://staging-mirth.zedoc.io/participationPost/",
                        headers={'Authorization': 'Basic emVkb2M6aW50ZWdyYXRpb24='},
                        data=payload,
                        verify=False)

      response_status_code = response.status_code
      response_body = response.text

      return response_status_code, response_body


def main(): 
      st.title("PREM Enrolment Form") 

      with st.form("enrol_form"):   
            first_name = st.text_input("First name")          
            phone_mobile = st.text_input("Mobile phone")
            hospital = st.selectbox("Hospital", ["Alpha Private Surgery","Ayr Hospital","Bamaga Hospital","Boonah Health Service","Caboolture Hospital","Charleville Hospital","Coen Primary Health Care Centre","Dysart Hospital","Esk Health Service","Gatton Health Service","Gympie Hospital","Home Hill Hospital", "Inala Community Health Centre","Ipswich Hospital", "Moura Hospital","Nambour General Hospital","The Royal Brisbane and Women's Hospital","Thursday Island Hospital","Warwick Health Service"], index=None)
            ward = st.text_input("Ward")
            unit = st.text_input("Unit")
            hhs = st.selectbox("Hospital and health services", ["Cairns and Hinterland", "Central Queensland", "Central West", "Darling Downs", "Gold Coast", "Mackay", "Metro North", "Metro South", "North West", "South West", "Sunshine Coast", "Torres and Cape", "Townsville", "West Moreton", "Wide Bay", "Children's Health Queensland"], index=None)
            peer_group = st.selectbox("Peer group", ["Small hospital", "Medium hospital", "Large hospital", "Psychiatric hospital", "Day hospital"], index=None)
            
            st.write("")
            st.write("")
      
            if st.form_submit_button('Enrol in ZEDOC', type="primary"): 
                try:
                    print("Enrolment process")
                    request_body = form_enrolment_request(first_name, phone_mobile, hospital, ward, unit, hhs, peer_group)
                    print("Request body formed")
                    response_status, response_body = send_enrolment_request(request_body)
                    print("Enrolment request sent")
                    if response_status == 200: 
                        st.success("Patient successfully enrolled.")
                    else: 
                        st.error(f"An error occurred.{str(response_body)}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")


if __name__ == '__main__':
     main()

