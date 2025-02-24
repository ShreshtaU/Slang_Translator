import streamlit as st
import json
import requests

# Load slang data from JSON file
def load_slang():
    with open("slang_data.json", "r") as file:
        return json.load(file)

# Save slang data to JSON file
def save_slang(slang_dict):
    with open("slang_data.json", "w") as file:
        json.dump(slang_dict, file, indent=4)

# Fetch slang meaning from Urban Dictionary if not found in JSON
def fetch_slang_meaning(word):
    url = f"https://api.urbandictionary.com/v0/define?term={word}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data["list"]:
            full_definition = data["list"][0]["definition"]
            short_definition = full_definition.split(".")[0]  # Take only the first sentence
            return short_definition
    return None

# Function to get meaning
def get_meaning(word, slang_dict):
    word = word.lower()

    if word in slang_dict:
        return slang_dict[word]

    meaning = fetch_slang_meaning(word)

    if meaning:
        slang_dict[word] = meaning  # Add to dictionary
        save_slang(slang_dict)  # Save to JSON file
        return meaning
    else:
        return "Sorry, this slang is not in our dictionary and couldn't be found online."

# Streamlit UI
st.set_page_config(page_title="Gen Z Slang Translator", page_icon="😎", layout="centered")

st.title("🟣 Gen Z Slang Translator")
st.write("Enter a slang word below to get its meaning.")

word = st.text_input("Enter a slang word:")

if st.button("Translate"):
    slang_dict = load_slang()
    meaning = get_meaning(word, slang_dict)
    st.success(f"**{word}**: {meaning}")

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: linear-gradient(to bottom (#d011bc,#ff00cf));
            [data-testid="stAppViewContainer"] {
            background-color: #E6E6FA; /* Light purple background */
            font-family: Arial, sans-serif;
        }
        .stTextInput>div>div>input {
            font-size: 18px !important;
        }
        .stButton>button {
            background-color: #6a0dad !important;
            color: white !important;
            font-size: 18px !important;
        }
    </style>
""", unsafe_allow_html=True)
