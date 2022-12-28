import streamlit as st
import re
from random import seed
import os
import openai

openai.api_key = st.secrets["openai_api_key"]

def main(): 
    st.title("Hack Sales With Personality Based Scripts")
    st.subheader("AI-based Copy Generator for your unique product, based on your lead's profile.")
    st.markdown("We use the **HIS (Human Intelligence System)** with 4 categories (Knight, Explorer, Healer, Wizard). HIS is a proven sales framework that has been used at top insurance and real estate firms including DBS, AIA and ERA. See https://www.personality-central.com.sg/reviews .")
    st.markdown("Not sure which type? Go to https://www.themindreader.ai/analyze to get a prediction in 2 min just using your photo or text.")


    with st.form(key='my_form'):
        product = st.text_input(label = "What do you want to sell?",
                          value = "vacuum cleaner")
        category = st.selectbox(label = "Which personality type are you selling to?",
                          options = ["Knight", "Explorer", "Healer", "Wizard"])
        features = st.text_area(label = "List features of your product: (optional)", height=150, max_chars=200)

        if len(product) < 3:
            st.header("text is too short to make prediction.")

        submitted = st.form_submit_button(label='Submit')
    if submitted:
        st.subheader("Sales Copy:")
        st.write(generate_copy(category, product, features))

def generate_copy(category, product, features):
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
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
    return response.choices[0].text

if __name__ == '__main__':
    main()
