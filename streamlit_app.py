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
import sqlite3
from streamlit_scroll_to_top import scroll_to_here




st.set_page_config(
    page_title="Social Dimenstions Annotation Task",
    page_icon="👩‍💻",
    layout="wide"
)

st.header("Social Dimensions Annotation Task")
st.markdown("****")
st.markdown("<div id='linkto_top'></div>", unsafe_allow_html=True)    

ANNOTATIONS_PER_ITEM = 5
ANNOTATIONS_PER_PERSON = 50
ANNOTATION_SHEET = "https://docs.google.com/spreadsheets/d/1VVZf3wtSYqxZkKzCdSk2iG_khdJTjCiSgW7lJPdISxQ/edit?gid=0#gid=0"
SOURCE_SHEET = "https://docs.google.com/spreadsheets/d/13sAE1CpqevnQPmcP_94sCugxWXjNsWlh3dVkh2qC4Ic/edit?gid=568110981#gid=568110981"
demographics_url = "https://docs.google.com/spreadsheets/d/1874zHrrRyKL-ESbeeS4Xw7ito22fPqzaEqWfKMp8eHI/edit?gid=0#gid=0"


# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
credentials = service_account.Credentials.from_service_account_info(
            st.secrets['connections']['gsheets'], 
            scopes=["https://www.googleapis.com/auth/spreadsheets",],)

client=gspread.authorize(credentials)



annotation_sheet = client.open_by_url(ANNOTATION_SHEET).sheet1

source_sheet = client.open_by_url(SOURCE_SHEET).sheet1 

state = st.session_state

@st.cache_data(ttl=1200)  # refresh every 60 seconds
def load_source_data():
    return source_sheet.get_all_records()

def get_user_annotation_count(username):
    records = annotation_sheet.get_all_records()
    return sum(1 for r in records if r["annotator"] == username)

@st.cache_data
def get_items(username):
    #st.write('Fetching items for:', username)
    
    data = annotation_sheet.get_all_records()
    user_count = sum(1 for r in data if r.get("annotator") == username)
    #st.write(f"User annotations so far: {user_count}")

    if user_count >= ANNOTATIONS_PER_PERSON:
        return []  # User reached max annotations

    source_records = load_source_data()

    # Count how many annotations each item has
    item_annotation_counts = {}
    for r in data:
        item_id = r.get("id")
        item_annotation_counts[item_id] = item_annotation_counts.get(item_id, 0) + 1

    # Filter items that still need annotations
    candidates = [row for row in source_records if item_annotation_counts.get(row["id"], 0) < ANNOTATIONS_PER_ITEM]
    print(len(candidates))
    # Exclude items already annotated by this user
    user_annotated_ids = {r.get("id") for r in data if r.get("annotator") == username}
    candidates = [c for c in candidates if c.get("id") not in user_annotated_ids]
    print(len(candidates))

    if not candidates:
        return []  # No items left to annotate

    # Shuffle for randomness
    random.shuffle(candidates)

    # Limit to remaining quota
    remaining_quota = ANNOTATIONS_PER_PERSON - user_count
    next_items = candidates[:remaining_quota]

    return next_items




countries = ['United States', 'United Kingdom', 'China', 'Canada', 'United Arab Emirates', 'Australia', 'Andorra', 'Afghanistan', 'Antigua and Barbuda', 'Anguilla', 'Albania', 'Armenia', 'Angola', 'Antarctica', 'Argentina', 'American Samoa', 'Austria', 'Aruba', 'Azerbaijan', 'Bosnia and Herzegovina', 'Barbados', 'Bangladesh', 'Belgium', 'Burkina Faso', 'Bulgaria', 'Bahrain', 'Burundi', 'Benin', 'Saint Barthelemy', 'Bermuda', 'Brunei', 'Bolivia', 'Brazil', 'Bahamas, The', 'Bhutan', 'Bouvet Island', 'Botswana', 'Belarus', 'Belize', 'Cocos (Keeling) Islands', 'Congo, Democratic Republic of the', 'Central African Republic', 'Congo, Republic of the', 'Switzerland', 'Cote d\'Ivoire', 'Cook Islands', 'Chile', 'Cameroon', 'Colombia', 'Costa Rica', 'Cuba', 'Cape Verde', 'Curacao', 'Christmas Island', 'Cyprus', 'Czech Republic', 'Germany', 'Djibouti', 'Denmark', 'Dominica', 'Dominican Republic', 'Algeria', 'Ecuador', 'Estonia', 'Egypt', 'Western Sahara', 'Eritrea', 'Spain', 'Ethiopia', 'Finland', 'Fiji', 'Falkland Islands (Islas Malvinas)', 'Micronesia, Federated States of', 'Faroe Islands', 'France', 'France, Metropolitan', 'Gabon', 'Grenada', 'Georgia', 'French Guiana', 'Guernsey', 'Ghana', 'Gibraltar', 'Greenland', 'Gambia, The', 'Guinea', 'Guadeloupe', 'Equatorial Guinea', 'Greece', 'South Georgia and the Islands', 'Guatemala', 'Guam', 'Guinea-Bissau', 'Guyana', 'Hong Kong (SAR China)', 'Heard Island and McDonald Islands', 'Honduras', 'Croatia', 'Haiti', 'Hungary', 'Indonesia', 'Ireland', 'Israel', 'Isle of Man', 'India', 'British Indian Ocean Territory', 'Iraq', 'Iran', 'Iceland', 'Italy', 'Jersey', 'Jamaica', 'Jordan', 'Japan', 'Kenya', 'Kyrgyzstan', 'Cambodia', 'Kiribati', 'Comoros', 'Saint Kitts and Nevis', 'Korea, South', 'Kuwait', 'Cayman Islands', 'Kazakhstan', 'Laos', 'Lebanon', 'Saint Lucia', 'Liechtenstein', 'Sri Lanka', 'Liberia', 'Lesotho', 'Lithuania', 'Luxembourg', 'Latvia', 'Libya', 'Morocco', 'Monaco', 'Moldova', 'Montenegro', 'Saint Martin', 'Madagascar', 'Marshall Islands', 'Macedonia', 'Mali', 'Burma', 'Mongolia', 'Macau (SAR China)', 'Northern Mariana Islands', 'Martinique', 'Mauritania', 'Montserrat', 'Malta', 'Mauritius', 'Maldives', 'Malawi', 'Mexico', 'Malaysia', 'Mozambique', 'Namibia', 'New Caledonia', 'Niger', 'Norfolk Island', 'Nigeria', 'Nicaragua', 'Netherlands', 'Norway', 'Nepal', 'Nauru', 'Niue', 'New Zealand', 'Oman', 'Panama', 'Peru', 'French Polynesia', 'Papua New Guinea', 'Philippines', 'Pakistan', 'Poland', 'Saint Pierre and Miquelon', 'Pitcairn Islands', 'Puerto Rico', 'Gaza Strip', 'West Bank', 'Portugal', 'Palau', 'Paraguay', 'Qatar', 'Reunion', 'Romania', 'Serbia', 'Russia', 'Rwanda', 'Saudi Arabia', 'Solomon Islands', 'Seychelles', 'Sudan', 'Sweden', 'Singapore', 'Saint Helena, Ascension, and Tristan da Cunha', 'Slovenia', 'Svalbard', 'Slovakia', 'Sierra Leone', 'San Marino', 'Senegal', 'Somalia', 'Suriname', 'South Sudan', 'Sao Tome and Principe', 'El Salvador', 'Sint Maarten', 'Syria', 'Swaziland', 'Turks and Caicos Islands', 'Chad', 'French Southern and Antarctic Lands', 'Togo', 'Thailand', 'Tajikistan', 'Tokelau', 'Timor-Leste', 'Turkmenistan', 'Tunisia', 'Tonga', 'Turkey', 'Trinidad and Tobago', 'Tuvalu', 'Taiwan, Province of China', 'Tanzania', 'Ukraine', 'Uganda', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Holy See (Vatican City)', 'Saint Vincent and the Grenadines', 'Venezuela', 'British Virgin Islands', 'Virgin Islands', 'Vietnam', 'Vanuatu', 'Wallis and Futuna', 'Samoa', 'Kosovo', 'Yemen', 'Mayotte', 'South Africa', 'Zambia', 'Zimbabwe']

def write_to_file(row, sheet_url):
    #sheet_url = collected_url #st.secrets["private_gsheets_url"] #this information should be included in streamlit secret
    sheet = client.open_by_url(sheet_url).sheet1
    sheet.append_row(row, table_range="A1") 

def save_annotation(item_id, username, annotation_text):
    annotation_sheet.append_row([username, item_id, annotation_text])


def annotate_response(dimensions, url):
    st.session_state.is_submitting = True
    if st.session_state.is_submitting:
        with st.spinner("Saving your annotation..."):
            labels = [state.username, state.session_id, state.candidates[0]["id"]] + dimensions
            write_to_file(labels, url)
            state.row_index+=1
            state.candidates.pop(0)
    st.session_state.is_submitting = False
    
if "username" not in state:
    state.username = ""
    state.session_id = ""

#state.username = st.text_input("Enter your state.username:")
if 'PROLIFIC_PID' not in state:
    if st.query_params.to_dict():
        url_params = st.query_params.to_dict()
        state.username = url_params['PROLIFIC_PID']
        state.session_id = url_params['SESSION_ID']
    else:
        state.username = 'amanda'
        state.session_id ='test'
    state.prev_annotations = get_user_annotation_count(state.username)
    state.PROLIFIC_PID = True

# Initialize state
if "is_submitting" not in st.session_state:
    st.session_state.is_submitting = False


if 'INSTRUCTIONS_READ' not in state:
    state.INSTRUCTIONS_READ = False
if 'INSTRUCTIONS' not in state:
    state.INSTRUCTIONS = 0

if "form_filled" not in state:
    state.form_filled = False

if "candidates"  not in state:
    #st.write('hello')
    state.candidates = get_items(state.username)

if "row_index" not in state:
    state.row_index = 0
    #state.current_item = state.candidates[state.row_index]

if state.prev_annotations>0:
    state.INSTRUCTIONS_READ = True
    state.form_filled = True

# Initialize flag
if "scroll_top" not in state:
    state.scroll_top = False

if state.scroll_top:
    scroll_js = """
    <script>
    window.addEventListener('load', function() {
        window.scrollTo(0,0);
    });
    </script>
    """
    st.components.v1.html(scroll_js, height=0)
    # Reset flag so it doesn’t scroll on every rerun
    st.session_state.scroll_top = False

import streamlit as st
from streamlit_scroll_to_top import scroll_to_here

if 'scroll_to_top' not in st.session_state:
    st.session_state.scroll_to_top = False
    
if 'scroll_to_header' not in st.session_state:
    st.session_state.scroll_to_header = False

if st.session_state.scroll_to_top:
    scroll_to_here(0, key='top')  # Scroll to the top of the page
    st.session_state.scroll_to_top = False  # Reset the state after scrolling

def scroll():
    st.session_state.scroll_to_top = True
    
def scrollheader():
    st.session_state.scroll_to_header = True

placeholder = st.empty()

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
                6. **Similarity**: Shared interests, motivations or outlooks.
                7. **Identity**: Shared sense of belonging to the same community or group.
                8. **Fun**: Experiencing leisure, laughter, and joy.
                9. **Conflict**: Contrast or diverging views.
                10. **Romance**: Intimacy among people with a sentimental or sexual relationship.
                    
                In this task, we want to understand which of these relationships are evident in a piece of text, with the exception of **Romance**.
                Each annotation should categorize interactions or relationships into one or more of the following dimensions. Annotators should consider the context, intent, and content of the text when assigning labels. If an interaction fits multiple dimensions, multiple labels may be applied.

                Let's look at each one more carefully.
                    ''')
        st.button("Click here to continue.", on_click=lambda: (state.update(INSTRUCTIONS=1), state.update(scroll_to_top = True)))

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
            *"But if you're generally curious, I'm happy to explain a few of the things that aren't entirely accurate."*  
            *"I'd recommend the first few times you do it using canned beer instead of bottled beer."*  
              
            ## 2. Power  
            **Definition:** Having power over the behavior and outcomes of another.  

            **Indicators:**  
            - Commands, instructions, or authoritative statements.  
            - Coercion, threats, or control over decisions.  
            - Expressing dominance or hierarchical superiority.  
            - Enforcement of rules or consequences.  

            **Examples:**  
            *"You must submit your report by noon, or there will be consequences."*  
            *"Your job is to take objectives But we can't actually **do** that right now."*  

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
            *"Thank you for teaching me a new word this morning."*  

                 ''')
        st.button("Next", on_click=lambda: (state.update(INSTRUCTIONS=2), state.update(scroll_to_top = True)))

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
            *"This is not the advice you've come for, but I think you need some *you* time."*  
            *"Your family has my condolences, for what little it's worth."*  

            ---

            ## 6. Similarity  
            **Definition:** Shared interests, motivations, or outlooks.  

            **Indicators:**  
            - Emphasizing commonalities in beliefs, experiences, or goals.  
            - Aligning with someone's perspective or background.  
            - Expressing unity based on shared attributes.  

            **Examples:**  
            *"We both grew up in the same town—no wonder we get along!"*  
            *"I totally agree with your views on this topic."*  
 

                 ''')
        st.button("More", on_click=lambda: (state.update(INSTRUCTIONS=3), state.update(scroll_to_top = True)))

    if state.INSTRUCTIONS == 3:
        st.write('''
            # Annotation Guidelines for Social Dimensions



            ## 7. Identity  
            **Definition:** Shared sense of belonging to the same community or group.  

            **Indicators:**  
            - Reference to group membership, culture, or collective identity.  
            - Statements reinforcing inclusion or exclusion.  
            - Discussing traditions, heritage, or community belonging.  

            **Examples:**  
            *"As fellow artists, we understand the struggle of finding inspiration."*  
            *"But what really set us apart and made our community unique was your contribution."*  

            ---

            ## 8. Fun  
            **Definition:** Experiencing leisure, laughter, and joy.  

            **Indicators:**  
            - Jokes, humor, or playful teasing.  
            - References to entertainment, hobbies, or games.  
            - Lighthearted and enjoyable interactions.  

            **Examples:**  
            *"Hahaha that's hilarious, and i feel you."*  
            *"Haha, you gave me and my girlfriend a good laugh at that haha."*  

            ---

            ## 9. Conflict  
            **Definition:** Contrast or diverging views.  

            **Indicators:**  
            - Disagreements, arguments, or criticism.  
            - Expressions of frustration, opposition, or hostility.  
            - Differences in opinions leading to tension.  

            **Examples:**  
            *"He's not some wildly popular player and your ignorance is showing."*  
            *"Because you're telling me that you literally don't care that you believe false things."*  
        
            ---
                 
           ## 10. Romance

            **Definition:** Flirting, expressions of affection, attraction, or intimacy, often signaling closeness or love between individuals. It is *not* comments about sex.

            **Indicators:**

            Declarations of love, admiration, or desire.

            Compliments on appearance, personality, or compatibility.

            References to relationships, dating, or emotional intimacy.

            **Examples:**
            "I think about you all the time, you make my days brighter."
            "You two are such a cute couple, it’s obvious how much you care for each other."
                

                 ''')
        st.button("And finally...", on_click=lambda: (state.update(INSTRUCTIONS=4), state.update(scroll_to_top = True)))

    if state.INSTRUCTIONS == 4:
        st.write('''
            # Annotation Guidelines for Social Dimensions
            
            ## General Annotation Rules  
            - **Consider Context:** Some statements may seem neutral but imply deeper relational dimensions.  
            - **Apply Multiple Labels When Necessary:** If an interaction contains elements of multiple dimensions, assign all relevant labels.  
            - **Avoid Overgeneralization:** Focus on the specific intent and effect of the statement rather than assuming based on general tone.  
            - **Disregard Sarcasm Unless Clear:** If sarcasm is ambiguous, label based on literal meaning. 
                 
            ## App-specific:
            - Use your mouse where possible.
            - Use tab to move between fields, enter will try to submit the form.
            - If you have an error, first try "Re-run" in the top right corner (click on the three dots).
            - If that doesn't work, please contact us.

                 ''')
        st.button("I have read the instructions", on_click=lambda: (state.update(INSTRUCTIONS_READ=True), state.update(scroll_to_top = True)))
        


if state.INSTRUCTIONS_READ:
    if not state.form_filled:
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


                    row = [state.username, state.session_id] + demographic_information + big5
                    if all_valid:
                        write_to_file(row, demographics_url)
                        state.form_filled = True
                        state.update(scroll_to_top = True)
                        st.rerun()



    if state.form_filled and state.row_index+state.prev_annotations<ANNOTATIONS_PER_PERSON:
        #st.write('index', state.row_index)
        with st.form("annotation_form"):
            st.subheader(f"Utterance {1+state.row_index+state.prev_annotations} of {ANNOTATIONS_PER_PERSON}")
            st.write("Please read the following utterance and select the dimensions that you think are present in the text. If you think none of the dimensions apply, please select 'None of the above'. Select all that apply.")
            
            text = state.candidates[state.row_index]['text'].replace("\n", "<br>")

            st.markdown(
                f"""
                <style>
                    .highlight {{
                        background-color: whitesmoke;
                        padding: 10px;
                        border-radius: 5px;
                        display: block;
                        margin: 20px;
                        font-size: 18px;
                        white-space: pre-wrap; /* <-- this preserves newlines */
                        word-wrap: break-word;
                    }}
                </style>
                <div class="highlight">
                    {text}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("Which of the following social dimensions apply to this text?")
            
            state.run = state.row_index  # keep for unique keys
            fun = st.checkbox('**Fun**: Experiencing leisure, laughter, and joy', key=f'fun_{state.run}')
            romance = st.checkbox('**Romance**: Intimacy among people with a sentimental or sexual relationship, flirting. It does not include general discussion around sex and sexuality.', key=f'rom_{state.run}')  
            trust = st.checkbox('**Trust**: Will of relying on the actions or judgments of another', key=f'trust_{state.run}')  
            support = st.checkbox('**Support**: Giving emotional or practical aid and companionship', key=f'supp_{state.run}')  
            similarity = st.checkbox('**Similarity**: Shared interests, motivations or outlooks', key=f'sim_{state.run}')  
            identity = st.checkbox('**Identity**: Shared sense of belonging to the same community or group', key=f'id_{state.run}')  
            status = st.checkbox('**Status**: Conferring status, appreciation, gratitude, or admiration upon another', key=f'stat_{state.run}')  
            knowledge = st.checkbox('**Knowledge**: Exchange of ideas or information; learning, teaching', key=f'know_{state.run}')  
            power = st.checkbox('**Power**: Having power over the behavior and outcomes of another', key=f'pow_{state.run}')  
            conflict = st.checkbox('**Conflict**: Contrast or diverging views', key=f'con_{state.run}') 
            other = st.checkbox('Other', key=f'oth_{state.run}')
            other_sp = st.text_input('If you selected other, please specify:', key=f'other_{state.run}')
            none = st.checkbox('None of the above', key=f'none_{state.run}')

            # Submit button for the form
            submitted = st.form_submit_button("Submit")

            if submitted:
                state.update(scroll_to_top = True)
                dimensions = [knowledge, power, status, trust, support, similarity, identity, fun, conflict, other, other_sp, none, romance]
                
                # Validation
                if none and (knowledge or power or status or trust or support or similarity or identity or fun or conflict or romance):
                    st.warning("Please select either 'None of the above' or one of the dimensions.")
                elif other and not other_sp:
                    st.warning("Please specify the other dimension.")
                elif any(dimensions):  # At least one selected
                    annotate_response(dimensions, ANNOTATION_SHEET)
                    #st.success("Annotation submitted!")
                    st.rerun()  # Load next item automatically
                else:
                    st.warning("Please select at least one option.")
                


    
    elif state.form_filled and state.row_index+state.prev_annotations>=ANNOTATIONS_PER_PERSON:
        st.subheader("Thank you!")
        placeholder.write("This is the last utterance. Thank you for participating! The completion code is: **CBN3YT5G**")

 

