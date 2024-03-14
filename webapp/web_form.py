
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


def form_enrolment_request(phone_mobile, email_personal, hhs, ward, procedure_type):
    request_body = {
        "messageId": uuid4().hex,
        "patient": {
            "phone_mobile": phone_mobile,
            "email_personal": email_personal
        },
        "participation": {
            "hhs": hhs,
            "ward": ward,
            "procedure_type": procedure_type
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

      return response_status_code


def main(): 
      st.title("PREM Enrolment Form") 

      with st.form("enrol_form"):             
            phone_mobile = st.text_input("Mobile phone")
            email_personal = st.text_input("Email address")
            hhs = st.selectbox("HHS/Hospitals", ["Alpha Private Surgery","Ayr Hospital","Bamaga Hospital","Boonah Health Service","Caboolture Hospital","Charleville Hospital","Coen Primary Health Care Centre","Dysart Hospital","Esk Health Service","Gatton Health Service","Gympie Hospital","Home Hill Hospital", "Inala Community Health Centre","Ipswich Hospital", "Moura Hospital","Nambour General Hospital","The Royal Brisbane and Women's Hospital","Thursday Island Hospital","Warwick Health Service"], index=None)
            ward = st.text_input("Ward")
            procedure_type = st.text_input("Procedure Type")
            
            st.write("")
            st.write("")
      
            if st.form_submit_button('Enrol in ZEDOC', type="primary"): 
                  request_body = form_enrolment_request(phone_mobile, email_personal, hhs, ward, procedure_type)
                  response_status = send_enrolment_request(request_body)
                  if response_status == 200: 
                        st.success("Patient successfully enrolled.")
                  else: 
                        st.error("An error occurred.")

if __name__ == '__main__':
     main()

