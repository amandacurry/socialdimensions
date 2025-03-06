import streamlit as st
from streamlit_gsheets import GSheetsConnection
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
from google.oauth2 import service_account
from shillelagh.backends.apsw.db import connect
import random

st.set_page_config(
    page_title="Social Dimenstions Annotation Task",
    page_icon="👩‍💻",
    layout="wide"
)

st.header("Social Dimensions Annotation Task")
st.markdown("****")
st.markdown("<div id='linkto_top'></div>", unsafe_allow_html=True)    



# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
credentials = service_account.Credentials.from_service_account_info(
            st.secrets['connections']['gsheets'], 
            scopes=["https://www.googleapis.com/auth/spreadsheets",],)

url = "https://docs.google.com/spreadsheets/d/1ZJICABhy361FCbYYxWmPbpKMI7nI_Bs7DRn4Le83TwY/edit?usp=sharing" # responses
dataset_url = "https://docs.google.com/spreadsheets/d/1KBhebUEIc3Y6kaTH6cUzYaDrFslxDt9bLU35UUTDD6A/edit?usp=sharing"

client=gspread.authorize(credentials)

countries = ['United States', 'United Kingdom', 'China', 'Canada', 'United Arab Emirates', 'Australia', 'Andorra', 'Afghanistan', 'Antigua and Barbuda', 'Anguilla', 'Albania', 'Armenia', 'Angola', 'Antarctica', 'Argentina', 'American Samoa', 'Austria', 'Aruba', 'Azerbaijan', 'Bosnia and Herzegovina', 'Barbados', 'Bangladesh', 'Belgium', 'Burkina Faso', 'Bulgaria', 'Bahrain', 'Burundi', 'Benin', 'Saint Barthelemy', 'Bermuda', 'Brunei', 'Bolivia', 'Brazil', 'Bahamas, The', 'Bhutan', 'Bouvet Island', 'Botswana', 'Belarus', 'Belize', 'Cocos (Keeling) Islands', 'Congo, Democratic Republic of the', 'Central African Republic', 'Congo, Republic of the', 'Switzerland', 'Cote d\'Ivoire', 'Cook Islands', 'Chile', 'Cameroon', 'Colombia', 'Costa Rica', 'Cuba', 'Cape Verde', 'Curacao', 'Christmas Island', 'Cyprus', 'Czech Republic', 'Germany', 'Djibouti', 'Denmark', 'Dominica', 'Dominican Republic', 'Algeria', 'Ecuador', 'Estonia', 'Egypt', 'Western Sahara', 'Eritrea', 'Spain', 'Ethiopia', 'Finland', 'Fiji', 'Falkland Islands (Islas Malvinas)', 'Micronesia, Federated States of', 'Faroe Islands', 'France', 'France, Metropolitan', 'Gabon', 'Grenada', 'Georgia', 'French Guiana', 'Guernsey', 'Ghana', 'Gibraltar', 'Greenland', 'Gambia, The', 'Guinea', 'Guadeloupe', 'Equatorial Guinea', 'Greece', 'South Georgia and the Islands', 'Guatemala', 'Guam', 'Guinea-Bissau', 'Guyana', 'Hong Kong (SAR China)', 'Heard Island and McDonald Islands', 'Honduras', 'Croatia', 'Haiti', 'Hungary', 'Indonesia', 'Ireland', 'Israel', 'Isle of Man', 'India', 'British Indian Ocean Territory', 'Iraq', 'Iran', 'Iceland', 'Italy', 'Jersey', 'Jamaica', 'Jordan', 'Japan', 'Kenya', 'Kyrgyzstan', 'Cambodia', 'Kiribati', 'Comoros', 'Saint Kitts and Nevis', 'Korea, South', 'Kuwait', 'Cayman Islands', 'Kazakhstan', 'Laos', 'Lebanon', 'Saint Lucia', 'Liechtenstein', 'Sri Lanka', 'Liberia', 'Lesotho', 'Lithuania', 'Luxembourg', 'Latvia', 'Libya', 'Morocco', 'Monaco', 'Moldova', 'Montenegro', 'Saint Martin', 'Madagascar', 'Marshall Islands', 'Macedonia', 'Mali', 'Burma', 'Mongolia', 'Macau (SAR China)', 'Northern Mariana Islands', 'Martinique', 'Mauritania', 'Montserrat', 'Malta', 'Mauritius', 'Maldives', 'Malawi', 'Mexico', 'Malaysia', 'Mozambique', 'Namibia', 'New Caledonia', 'Niger', 'Norfolk Island', 'Nigeria', 'Nicaragua', 'Netherlands', 'Norway', 'Nepal', 'Nauru', 'Niue', 'New Zealand', 'Oman', 'Panama', 'Peru', 'French Polynesia', 'Papua New Guinea', 'Philippines', 'Pakistan', 'Poland', 'Saint Pierre and Miquelon', 'Pitcairn Islands', 'Puerto Rico', 'Gaza Strip', 'West Bank', 'Portugal', 'Palau', 'Paraguay', 'Qatar', 'Reunion', 'Romania', 'Serbia', 'Russia', 'Rwanda', 'Saudi Arabia', 'Solomon Islands', 'Seychelles', 'Sudan', 'Sweden', 'Singapore', 'Saint Helena, Ascension, and Tristan da Cunha', 'Slovenia', 'Svalbard', 'Slovakia', 'Sierra Leone', 'San Marino', 'Senegal', 'Somalia', 'Suriname', 'South Sudan', 'Sao Tome and Principe', 'El Salvador', 'Sint Maarten', 'Syria', 'Swaziland', 'Turks and Caicos Islands', 'Chad', 'French Southern and Antarctic Lands', 'Togo', 'Thailand', 'Tajikistan', 'Tokelau', 'Timor-Leste', 'Turkmenistan', 'Tunisia', 'Tonga', 'Turkey', 'Trinidad and Tobago', 'Tuvalu', 'Taiwan, Province of China', 'Tanzania', 'Ukraine', 'Uganda', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Holy See (Vatican City)', 'Saint Vincent and the Grenadines', 'Venezuela', 'British Virgin Islands', 'Virgin Islands', 'Vietnam', 'Vanuatu', 'Wallis and Futuna', 'Samoa', 'Kosovo', 'Yemen', 'Mayotte', 'South Africa', 'Zambia', 'Zimbabwe']
def write_to_file(row, sheet_url):
    #sheet_url = collected_url #st.secrets["private_gsheets_url"] #this information should be included in streamlit secret
    sheet = client.open_by_url(sheet_url).sheet1
    sheet.append_row(row, table_range="A1:Z1") 
    #st.success('Data has been written to Google Sheets')
    
def annotate_response(labels, sheet):
    id = state.responses.iloc[state.current_response_row]['id']
    #state.response_ratings[id] = label
    write_to_file([id, annotator_id, session_id].extend(labels), sheet)
    state.current_response_row+=1
    state.run+=1
    state.r = random.randint(1, 2)
    if state.current_response_row<len(state.responses):
        state.current_response = state.responses.iloc[[state.current_response_row]]


### Defining state:
state = st.session_state

if 'PROLIFIC_PID' not in state:
    if st.query_params.to_dict():
        url_params = st.query_params.to_dict()
        annotator_id = url_params['PROLIFIC_PID']
        session_id = url_params['SESSION_ID']
    else:
        annotator_id = 'test'
        session_id = 'test'

if 'INSTRUCTIONS_READ' not in state:
    state.INSTRUCTIONS_READ = False

if "form_filled" not in state:
    state.form_filled = False


if 'responses' not in state:
    responses_to_annotate = conn.read(
        spreadsheet=dataset_url,
        worksheet="Sheet1",
        ttl="0")[['id', 'text']].dropna()
    state.response_ratings = {}
    state.responses = responses_to_annotate.sample(10)
    state.test_rows = state.responses.head(2)
    state.responses = pd.concat([state.responses, state.test_rows]).reset_index(drop=True)
    state.current_response_row = 0
    state.current_response = state.responses.iloc[[state.current_response_row]]
    state.run = 0
    state.r = random.randint(1, 2)


########### DEMOGRAPHICS FORM ##############
placeholder = st.empty()
if not state.INSTRUCTIONS_READ:

        st.write('''
            # Annotation Guidelines for Relationship Dimensions

            Each annotation should categorize interactions or relationships into one or more of the following dimensions. Annotators should consider the context, intent, and content of the text when assigning labels. If an interaction fits multiple dimensions, multiple labels may be applied.

            ---

            ## 1. Knowledge  
            **Definition:** Exchange of ideas or information; learning, teaching.  

            **Indicators:**  
            - Sharing facts, expertise, or explanations.  
            - Teaching or instructing someone.  
            - Asking or answering questions to gain understanding.  
            - Providing references or sources to support learning.  

            **Examples:**  
            *"Did you know that the Eiffel Tower expands in the summer due to heat?"*  
            *"Let me explain how this formula works in physics."*  

            ---

            ## 2. Power  
            **Definition:** Having power over the behavior and outcomes of another.  

            **Indicators:**  
            - Commands, instructions, or authoritative statements.  
            - Coercion, threats, or control over decisions.  
            - Expressing dominance or hierarchical superiority.  
            - Enforcement of rules or consequences.  

            **Examples:**  
            *"You must submit your report by noon, or there will be consequences."*  
            *"As your boss, I expect you to follow my instructions without question."*  

            ---

            ## 3. Status  
            **Definition:** Conferring status, appreciation, gratitude, or admiration upon another.  

            **Indicators:**  
            - Compliments, praise, or recognition.  
            - Assigning prestige, rank, or superiority.  
            - Expressing admiration or gratitude.  
            - Indicating social hierarchy or reputation.  

            **Examples:**  
            *"You did an amazing job on this project!"*  
            *"He’s one of the most respected scientists in the field."*  

            ---

            ## 4. Trust  
            **Definition:** Willingness to rely on the actions or judgments of another.  

            **Indicators:**  
            - Expressing confidence in someone's reliability or decisions.  
            - Seeking reassurance or demonstrating belief in another's integrity.  
            - Statements of dependence or faith in someone's actions.  

            **Examples:**  
            *"I know I can count on you to handle this."*  
            *"I trust your judgment—go ahead with the plan."*  

            ---

            ## 5. Support  
            **Definition:** Giving emotional or practical aid and companionship.  

            **Indicators:**  
            - Offering help, encouragement, or comfort.  
            - Expressing care, concern, or empathy.  
            - Providing assistance or resources for well-being.  

            **Examples:**  
            *"I'm here for you if you need anything."*  
            *"Let me know how I can help you through this."*  

            ---

            ## 6. Romance  
            **Definition:** Intimacy among people with a sentimental or sexual relationship.  

            **Indicators:**  
            - Expressions of love, affection, or romantic interest.  
            - Discussion of romantic or sexual relationships.  
            - Terms of endearment or flirtation.  

            **Examples:**  
            *"I love you so much; you mean the world to me."*  
            *"Would you like to go on a date with me this weekend?"*  

            ---

            ## 7. Similarity  
            **Definition:** Shared interests, motivations, or outlooks.  

            **Indicators:**  
            - Emphasizing commonalities in beliefs, experiences, or goals.  
            - Aligning with someone's perspective or background.  
            - Expressing unity based on shared attributes.  

            **Examples:**  
            *"We both grew up in the same town—no wonder we get along!"*  
            *"I totally agree with your views on this topic."*  

            ---

            ## 8. Identity  
            **Definition:** Shared sense of belonging to the same community or group.  

            **Indicators:**  
            - Reference to group membership, culture, or collective identity.  
            - Statements reinforcing inclusion or exclusion.  
            - Discussing traditions, heritage, or community belonging.  

            **Examples:**  
            *"As fellow artists, we understand the struggle of finding inspiration."*  
            *"We, as a nation, need to work together."*  

            ---

            ## 9. Fun  
            **Definition:** Experiencing leisure, laughter, and joy.  

            **Indicators:**  
            - Jokes, humor, or playful teasing.  
            - References to entertainment, hobbies, or games.  
            - Lighthearted and enjoyable interactions.  

            **Examples:**  
            *"That was the funniest movie I’ve ever seen!"*  
            *"Let’s go on a road trip this weekend for some adventure!"*  

            ---

            ## 10. Conflict  
            **Definition:** Contrast or diverging views.  

            **Indicators:**  
            - Disagreements, arguments, or criticism.  
            - Expressions of frustration, opposition, or hostility.  
            - Differences in opinions leading to tension.  

            **Examples:**  
            *"I completely disagree with your stance on this issue."*  
            *"You always interrupt me when I try to explain my side!"*  

            ---

            ## General Annotation Rules  
            - **Consider Context:** Some statements may seem neutral but imply deeper relational dimensions.  
            - **Apply Multiple Labels When Necessary:** If an interaction contains elements of multiple dimensions, assign all relevant labels.  
            - **Avoid Overgeneralization:** Focus on the specific intent and effect of the statement rather than assuming based on general tone.  
            - **Disregard Sarcasm Unless Clear:** If sarcasm is ambiguous, label based on literal meaning.  

            ---


        ''')
        
        st.button("I have read the instructions", on_click=lambda: state.update(INSTRUCTIONS_READ=True))

#if not state.form_filled:
if state.INSTRUCTIONS_READ:
    with placeholder.container():

        with st.form("demographics"):

            st.subheader("Tell us a bit about you")

            st.write('We are conducting research about the ways in which people of all backgrounds are using AI. To understand if there are differences in the ways different people are using AI chatbots and other technologies, we are running a survey. ')
            st.write('Any data published will be fully anonymised. ')
            st.write('USE TAB TO GO TO THE NEXT SECTION. DO NOT PRESS ENTER TO MOVE TO THE NEXT SECTION OR THE FORM WILL SUBMIT!!!')

            placeholder_s = "Select all that apply."

            gender = st.selectbox("Gender*", ("Male", "Female", "Non-binary", "Other, please specify.", "Prefer not to say"), index=None)

            gender_other = st.text_input('If you selected other, please specify:', key = 'gender')
            
            age = st.radio('Age*', ['18-24', '25-34' , '35-44', '45-54', '55-60', '60+'], None, key='_age', horizontal=True)

            nationality = st.multiselect('Nationality (You may select multiple):*', options = countries, placeholder=placeholder_s)
    
            ethnicity = st.multiselect('What is your ethnicity? You may select more than one.*', options = ['American Indian or Alaskan Native', 'Asian / Pacific Islander', 'Black or African American', 'Hispanic', 'White / Caucasian', 'Other. Please specify', 'Prefer not to say'], placeholder=placeholder_s)
            ethn_free = st.text_input('If you selected other, please specify:', key = 'ethnic')

            language = st.multiselect('What is your first language? You may select more than one, if applicable.*', options = ['English', 'Spanish', 'German', 'Chinese', 'French', 'Arabic', 'Other (Please Specify)'], placeholder=placeholder_s)
            language_free = st.text_input('If you selected other, please specify:', key = 'lang')

            religion = st.selectbox('Do you have a religious affiliation? If so, which one?*', options = ['Christian', 'Muslim', 'Jewish',  'Buddhist', 'Other, please specify.', 'None', 'Prefer not to say'], index = None)
            religion_other = st.text_input('If you selected other, please specify:', key = 'religion')

            education = st.selectbox('Current education level* ', options = ['High school or below', 'Undergraduate degree', 'Graduate degree', 'Doctorate or above', 'Prefer not to say'], index=None)
    
            
            st.markdown('***')



            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")#, on_click=populate_annotations)
            if submitted:
                all_valid = True
                required = [gender, age, nationality, language, ethnicity,  language,  religion,  education,]
                #cond = [llm_use, usecases, contexts,  prompt1, prompt2, prompt3, prompt4, prompt5, prompt6, prompt7, prompt8, prompt9, prompt10]


                demographic_information = [
                    gender, gender_other, age, ';'.join(nationality), ';'.join(ethnicity), ethn_free,
                ]

                row = [annotator_id, session_id] + demographic_information 
                write_to_file(row, url)
            
                state.form_filled = True




if state.form_filled:
    placeholder.empty()
        
    annotation = st.container(border=True)
    annotation.subheader("Utterance {} of {} ".format(state.current_response_row+1, len(state.responses)))
    annotation.write(state.responses.iloc[state.current_response_row]['text'])

    knowledge = annotation.checkbox('*Knowledge*: Exchange of ideas or information; learning, teaching', key='know_'+str(state.run))  
    power = annotation.checkbox('*Power*: Having power over the behavior and outcomes of another', key='pow_'+str(state.run))  
    status = annotation.checkbox('*Status*: Conferring status, appreciation, gratitude, or admiration upon another', key='stat_'+str(state.run))  
    trust = annotation.checkbox('*Trust*: Will of relying on the actions or judgments of another', key='trust_'+str(state.run))  
    support = annotation.checkbox('*Support*: Giving emotional or practical aid and companionship', key='supp_'+str(state.run))  
    romance = annotation.checkbox('*Romance*: Intimacy among people with a sentimental or sexual relationship', key='rom_'+str(state.run))  
    similarity = annotation.checkbox('*Similarity*: Shared interests, motivations or outlooks', key='sim_'+str(state.run))  
    identity = annotation.checkbox('*Identity*: Shared sense of belonging to the same community or group', key='id_'+str(state.run))  
    fun = annotation.checkbox('*Fun*: Experiencing leisure, laughter, and joy', key='fun_'+str(state.run))  
    conflict = annotation.checkbox('*Conflict*: Contrast or diverging views', key='con_'+str(state.run)) 
    other = annotation.checkbox('Other', key='oth_'+str(state.run))
    none = annotation.checkbox('None of the above', key='none_'+str(state.run))

        
    dimensions = [knowledge, power, status, trust, support, romance, similarity, identity, fun, conflict, other, none]


    if any(dimensions):
        annotation.button("Submit", on_click=annotate_response, args=(dimensions, url))
        knowledge = None




