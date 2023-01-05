import streamlit as st
import re
from random import seed
import os
import openai
import streamlit_authenticator as stauth
import yaml
from yaml import SafeLoader

openai.api_key = st.secrets["openai_api_key"]

def main(): 

    authenticator, config = init_auth()
    name, authentication_status, username = authenticator.login('Login', 'main')

    if authentication_status:
        st.sidebar.title(f"Username: {name}")
        st.sidebar.subheader("Tokens Used: " + str(get_tokens(config, username)))
        if st.sidebar.button('Reset Password'):
            pw_reset(authenticator, authentication_status, username)
        authenticator.logout("Logout", "sidebar")
        copy_tool(config, username)
        update_config(config)

    elif authentication_status == False:
        st.error('Username/password is incorrect')
    if authentication_status is None or authentication_status == False:
        if st.button('Register New User'):
            register_new_user(authenticator, config)
        if st.button('Forgot Password'):
            forgot_pw(authenticator)
        if st.button('Forgot Username'):
            forgot_username(authenticator)

def register_new_user(authenticator, config):
    try:
        st.subheader(f"Use the same email as your Stripe payment email.")
        if authenticator.register_user('Register user', preauthorization=False):
            st.success('User registered successfully')
            update_config(config)
    except Exception as e:
        st.error(e)

def pw_reset(authenticator, authentication_status, username):
    try:
        if authenticator.reset_password(username, 'Reset password'):
            st.success('Password modified successfully')
            update_config(config)
    except Exception as e:
        st.error(e)

def forgot_pw(authenticator):
    try:
        username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
        if username_forgot_pw:
            st.success('New password sent securely')
            update_config(config)
        elif username_forgot_pw == False:
            st.error('Username not found')
    except Exception as e:
        st.error(e)

def forgot_username(authenticator):
    try:
        username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
        if username_forgot_username:
            st.success('Username sent securely')
        elif username_forgot_username == False:
            st.error('Email not found')
    except Exception as e:
        st.error(e)

def copy_tool(config, username):
    st.title("Hack Sales With Personality Based Scripts")
    st.subheader("AI-based Copy Generator for your unique product, based on your lead's profile.")
    st.markdown("We use the **HIS (Human Intelligence System)** with 4 categories (Knight, Explorer, Healer, Wizard). HIS is a proven sales framework that has been used at top insurance and real estate firms including DBS, AIA and ERA. See https://www.personality-central.com.sg/reviews .")
    st.markdown("Not sure which type? Go to https://www.themindreader.ai/analyze to get a prediction in 2 min just using your photo or text.")

    # Using the "with" syntax
    with st.form(key='my_form'):
        product = st.text_input(label = "What do you want to sell?",
                          value = "vacuum cleaner", max_chars=50)
        category = st.selectbox(label = "Which personality type are you selling to?",
                          options = ["Knight", "Explorer", "Healer", "Wizard"])
        features = st.text_area(label = "List features of your product: (optional)", height=150, max_chars=200)
        tokens = st.slider('Max tokens of generated copy:', 100, 300, 200)
        # input validation
        if len(product) < 3:
            st.header("text is too short to make prediction.")

        submitted = st.form_submit_button(label='Submit')
    if submitted:
        if get_tokens(config, username) > 1500:
            st.error('No more tokens. Upgrade your plan or purchase more.')
        else:
            st.subheader("Sales Copy:")
            with st.spinner('Generating Copy...'):
                response = generate_copy(category, product, features, tokens)
                st.write(response.choices[0].text)
                config["credentials"]["usernames"][username]["tokens"] += response.usage.total_tokens
                update_config(config)

def generate_copy(category, product, features, tokens):
    if category == "Knight":
        prompt = f"""INSERT INTO knight (description) VALUES ('Knights are diligent and conscientious clients who consider their purchases carefully. Their keywords are family, security, safe,government and authority.');\
        Features: {features} .Write a sales pitch to sell {product} to a knight excluding the word knight and including features plus 1 benefit of {product} from your general knowledge.""" 
    elif category == "Explorer":
        prompt = f"""INSERT INTO explorer (description) VALUES ('Explorers are fun-loving and light hearted clients who love to buy when excited or on impulse. Keywords are right now, enjoyment, leisure, pleasure, instinctive.');\
        Features: {features} .Write a sales pitch to sell {product} to an explorer excluding the word explorer and including features plus 1 benefit of {product} from your general knowledge.""" 
    elif category == "Healer":
        prompt = f"""INSERT INTO healer (description) VALUES ('Healers are sensitive and approachable clients who considers the wider social impact of their purchases. Their keywords are contribution, legacy, humanitarian, future generations and giving.');\
        Features: {features} .Write a sales pitch to sell {product} to a healer excluding the word healer and including features plus 1 benefit of {product} from your general knowledge.""" 
    else:
        prompt = f"""INSERT INTO wizard (description) VALUES ('Wizards are analytical and skeptical clients who seek status, power and acheivement in their purchases. Keywords are statistics, prestige, power, knowledge, competence, systems, expert, master and competition.');\
        Features: {features} .Write a sales pitch to sell {product} to a wizard excluding the word wizard and including features plus 1 benefit of {product} from your general knowledge.""" 
    print(prompt)

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
    return response

def update_config(config):
    with open('./config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

def get_tokens(config, username):
    return config["credentials"]["usernames"][username]["tokens"]

def init_auth():
    with open('./config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            config['preauthorized']
        )
    return authenticator, config

if __name__ == '__main__':
    main()
