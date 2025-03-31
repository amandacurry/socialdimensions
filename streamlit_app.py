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
demographics_url = "https://docs.google.com/spreadsheets/d/1iDwU43J-8OPCnfg9D8l2fOu36OwGlG3eitqHQ1iX_iM/edit?usp=sharing"

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

def bold_substring(text, substring):
    return text.replace(substring, f"<b>{substring}</b>")


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
        ttl="0")[['id', 'text', 'h_text']].dropna()
    test_questions = conn.read(
        spreadsheet=dataset_url,
        worksheet="test_questions",
        ttl="0")[['id', 'text', 'h_text']].dropna()
    state.response_ratings = {}
    state.responses = responses_to_annotate.sample(47)
    state.test_rows = test_questions.sample(3)
    state.responses = pd.concat([state.responses, state.test_rows]).reset_index(drop=True)
    state.current_response_row = 0
    state.current_response = state.responses.iloc[[state.current_response_row]]
    state.run = 0
    state.r = random.randint(1, 2)

if 'INSTRUCTIONS' not in state:
    state.INSTRUCTIONS = 0


########### DEMOGRAPHICS FORM ##############
placeholder = st.empty()
if not state.INSTRUCTIONS_READ:

    if state.INSTRUCTIONS == 0:
        st.write('''
                # Annotation Guidelines for Social Dimensions
                    
                **Social Dimensions** are the types of relationships or interactions that people have with each other. These dimensions can be used to describe the nature of interactions between people in a text.
                Experts have identified ten social dimensions:
                    
                1. **Knowledge**: Exchange of ideas or information; learning, teaching.
                2. **Power**: Having power over the behavior and outcomes of another.
                3. **Status**: Conferring status, appreciation, gratitude, or admiration upon another.
                4. **Trust**: Will of relying on the actions or judgments of another.
                5. **Support**: Giving emotional or practical aid and companionship.
                6. **Romance**: Intimacy among people with a sentimental or sexual relationship.
                7. **Similarity**: Shared interests, motivations or outlooks.
                8. **Identity**: Shared sense of belonging to the same community or group.
                9. **Fun**: Experiencing leisure, laughter, and joy.
                10. **Conflict**: Contrast or diverging views.
                    
                In this task, we want to understand which of these relationships are evident in a piece of text, with the exception of **Romance**.
                Each annotation should categorize interactions or relationships into one or more of the following dimensions. Annotators should consider the context, intent, and content of the text when assigning labels. If an interaction fits multiple dimensions, multiple labels may be applied.

                Let's look at each one more carefully.
                    ''')
        st.button("Click here to continue.", on_click=lambda: state.update(INSTRUCTIONS=1))

    if state.INSTRUCTIONS == 1:
        st.write('''
            # Annotation Guidelines for Social Dimensions
            
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

                 ''')
        st.button("Next", on_click=lambda: state.update(INSTRUCTIONS=2))

    if state.INSTRUCTIONS == 2:
        st.write('''
            # Annotation Guidelines for Social Dimensions
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

 

                 ''')
        st.button("More", on_click=lambda: state.update(INSTRUCTIONS=3))

    if state.INSTRUCTIONS == 3:
        st.write('''
            # Annotation Guidelines for Social Dimensions
            ## 6. Similarity  
            **Definition:** Shared interests, motivations, or outlooks.  

            **Indicators:**  
            - Emphasizing commonalities in beliefs, experiences, or goals.  
            - Aligning with someone's perspective or background.  
            - Expressing unity based on shared attributes.  

            **Examples:**  
            *"We both grew up in the same town—no wonder we get along!"*  
            *"I totally agree with your views on this topic."*  

            ---

            ## 7. Identity  
            **Definition:** Shared sense of belonging to the same community or group.  

            **Indicators:**  
            - Reference to group membership, culture, or collective identity.  
            - Statements reinforcing inclusion or exclusion.  
            - Discussing traditions, heritage, or community belonging.  

            **Examples:**  
            *"As fellow artists, we understand the struggle of finding inspiration."*  
            *"We, as a nation, need to work together."*  

            ---

            ## 8. Fun  
            **Definition:** Experiencing leisure, laughter, and joy.  

            **Indicators:**  
            - Jokes, humor, or playful teasing.  
            - References to entertainment, hobbies, or games.  
            - Lighthearted and enjoyable interactions.  

            **Examples:**  
            *"That was the funniest movie I’ve ever seen!"*  
            *"Let’s go on a road trip this weekend for some adventure!"*  

            ---

            ## 9. Conflict  
            **Definition:** Contrast or diverging views.  

            **Indicators:**  
            - Disagreements, arguments, or criticism.  
            - Expressions of frustration, opposition, or hostility.  
            - Differences in opinions leading to tension.  

            **Examples:**  
            *"I completely disagree with your stance on this issue."*  
            *"You always interrupt me when I try to explain my side!"*  
 

                 ''')
        st.button("And finally...", on_click=lambda: state.update(INSTRUCTIONS=4))

    if state.INSTRUCTIONS == 4:
        st.write('''
            # Annotation Guidelines for Social Dimensions
            
            ## General Annotation Rules  
            - **Consider Context:** Some statements may seem neutral but imply deeper relational dimensions.  
            - **Apply Multiple Labels When Necessary:** If an interaction contains elements of multiple dimensions, assign all relevant labels.  
            - **Avoid Overgeneralization:** Focus on the specific intent and effect of the statement rather than assuming based on general tone.  
            - **Disregard Sarcasm Unless Clear:** If sarcasm is ambiguous, label based on literal meaning.  

                 ''')
        st.button("I have read the instructions", on_click=lambda: state.update(INSTRUCTIONS_READ=True))
        
    

#if not state.form_filled:
if state.INSTRUCTIONS_READ:
    with placeholder.container():

        with st.form("demographics"):

            st.subheader("Tell us a bit about you")

            st.write('We want to know a bit about you to understand how different people interpret the text. ')
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
            st.subheader("Personality Traits")
            st.write('The task is subjective. The following questions help us understand how personality traits might affect your interpretation of the utterances.')
            options = ['Strongly disagree', "Disagree", "Neutral", "Agree", "Strongly agree"]
            big_1 = st.radio('I see myself as someone who is reserved.', options = options, index=None, horizontal=True)
            big_2 = st.radio('I see myself as someone who is generally trusting.', options = options,  index=None, horizontal=True)
            big_3 = st.radio('I see myself as someone who tends to be lazy.', options = options,  index=None, horizontal=True)
            big_4 = st.radio('I see myself as someone who is relaxed, handles stress well.', options = options,  index=None, horizontal=True)
            big_5 = st.radio('I see myself as someone who has few artistic interests.', options = options,  index=None, horizontal=True)
            big_6 = st.radio('I see myself as someone who is outgoing, sociable.', options = options, index=None, horizontal=True)
            big_7 = st.radio('I see myself as someone who tends to find fault with others.', options = options, index=None, horizontal=True)
            big_8 = st.radio('I see myself as someone who does a thorough job.', options = options, index=None, horizontal=True)
            big_9 = st.radio('I see myself as someone who gets nervous easily.', options = options, index=None, horizontal=True)
            big_10 = st.radio('I see myself as someone who has an active imagination.', options = options,  index=None, horizontal=True)


            st.markdown("""
                <style>
                .stSlider [data-baseweb=slider]{
                    width: 30%;
                }
                div[class*="stSlider"] > label > div[data-testid="stMarkdownContainer"] > p {
                    font-size: 20px;
                }
                div[class*="stSelectbox"] > label > div[data-testid="stMarkdownContainer"] > p {
                    font-size: 20px;
                }
                div[class*="stTextInput"] > label > div[data-testid="stMarkdownContainer"] > p {
                    font-size: 20px;
                }
                div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {
                    font-size: 20px;
                }
                div[class*="stMultiSelect"] > label > div[data-testid="stMarkdownContainer"] > p {
                    font-size: 20px;
                }
                """,unsafe_allow_html=True)
            
            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")#, on_click=populate_annotations)
            if submitted:
                all_valid = True
                required = [gender, age, nationality, language, ethnicity,  language,  religion,  education,]
                #cond = [llm_use, usecases, contexts,  prompt1, prompt2, prompt3, prompt4, prompt5, prompt6, prompt7, prompt8, prompt9, prompt10]

                if any(field is None or field == "" for field in required):
                    st.warning("Please complete all required fields in the form.")
                    all_valid = False

                demographic_information = [
                    gender, gender_other, age, ';'.join(nationality), ';'.join(ethnicity), ethn_free, ';'.join(language),  religion,  education
                ]

                big5 = [big_1, big_2, big_3, big_4, big_5, big_6, big_7, big_8, big_9, big_10]


                row = [annotator_id, session_id] + demographic_information + big5
                if all_valid:
                    write_to_file(row, demographics_url)
                
                    state.form_filled = True




if state.form_filled:
    placeholder.empty()
        
    annotation = st.container(border=True)
    annotation.subheader("Utterance {} of {} ".format(state.current_response_row+1, len(state.responses)))
    annotation.write("Please read the following utterance and select the dimensions that you think are present in the section in **bold**. If you think none of the dimensions apply, please select 'None of the above'. Select all that apply.")
    text = bold_substring(state.responses.iloc[state.current_response_row]['text'], state.responses.iloc[state.current_response_row]['h_text'])
    #annotation.write(state.responses.iloc[state.current_response_row]['text'])
    #annotation.markdown(text)

    annotation.markdown(
        """
        <style>
            .highlight {
                background-color: whitesmoke;
                padding: 10px;
                border-radius: 5px;
                display: block;
                margin: 20px;
                font-size: 18px;
            }
        </style>
        <div class="highlight">
            """ + text + """
        </div>
        """,
        unsafe_allow_html=True
    )

    annotation.write("Which of the following social dimensions apply to the section in **bold**?")
    
    #romance = annotation.checkbox('**Romance**: Intimacy among people with a sentimental or sexual relationship', key='rom_'+str(state.run))  
    fun = annotation.checkbox('**Fun**: Experiencing leisure, laughter, and joy', key='fun_'+str(state.run))

    trust = annotation.checkbox('**Trust**: Will of relying on the actions or judgments of another', key='trust_'+str(state.run))  
    support = annotation.checkbox('**Support**: Giving emotional or practical aid and companionship', key='supp_'+str(state.run))  
    similarity = annotation.checkbox('**Similarity**: Shared interests, motivations or outlooks', key='sim_'+str(state.run))  
    identity = annotation.checkbox('**Identity**: Shared sense of belonging to the same community or group', key='id_'+str(state.run))  
    
    status = annotation.checkbox('**Status**: Conferring status, appreciation, gratitude, or admiration upon another', key='stat_'+str(state.run))  

    knowledge = annotation.checkbox('**Knowledge**: Exchange of ideas or information; learning, teaching', key='know_'+str(state.run))  
    power = annotation.checkbox('**Power**: Having power over the behavior and outcomes of another', key='pow_'+str(state.run))  

    conflict = annotation.checkbox('**Conflict**: Contrast or diverging views', key='con_'+str(state.run)) 

    other = annotation.checkbox('Other', key='oth_'+str(state.run))
    other_sp = annotation.text_input('If you selected other, please specify:', key = 'other_'+str(state.run))
    none = annotation.checkbox('None of the above', key='none_'+str(state.run))

        
    dimensions = [knowledge, power, status, trust, support, similarity, identity, fun, conflict, other, other_sp, none]


    if any(dimensions):
        annotation.button("Submit", on_click=annotate_response, args=(dimensions, url))

if state.current_response_row == len(state.responses):
    annotation.empty()
    st.subheader("Thank you!")
    annotation.write("This is the last utterance. Thank you for participating! The completion code is: C18E9D69")



