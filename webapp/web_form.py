
import streamlit as st 
import os 
import json
import datetime 
import requests 
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def inject_custom_css():
    with open('./assets/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

inject_custom_css()


def form_enrolment_request(identifier_nhi, first_name, last_name, gender, birth_date, phone_mobile, email_personal): 
        birth_date_str = birth_date.strftime("%Y-%m-%d") if birth_date else None
        patient = {
              "identifier_nhi": identifier_nhi, 
              "first_name" : first_name,
              "last_name": last_name,
              "gender": gender, 
              "birth_date": birth_date_str,
              "phone_mobile": phone_mobile,
              "email_personal": email_personal
        }
        return {"patient": patient }

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
      st.title("Patient Enrolment Form") 

      with st.form("enrol_form"): 
            identifier_nhi = st.text_input("National health identifier")
            first_name = st.text_input("First name")
            last_name = st.text_input("Last name")
            gender = st.selectbox("Gender", ["Male", "Female", "Diverse", "Unknown"], index=None)
            birth_date = st.date_input("Birth date", value=None, format="DD/MM/YYYY")
            phone_mobile = st.text_input("Mobile phone")
            email_personal = st.text_input("Email address")
            
            st.write("")
            st.write("")
      
            if st.form_submit_button('Enrol in ZEDOC', type="primary"): 
                  request_body = form_enrolment_request(identifier_nhi, first_name, last_name, gender, birth_date, phone_mobile, email_personal)
                  response_status = send_enrolment_request(request_body)
                  if response_status == 200: 
                        st.success("Patient successfully enrolled.")
                  else: 
                        st.error("An error occurred.")

if __name__ == '__main__':
     main()

