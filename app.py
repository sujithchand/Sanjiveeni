import streamlit as st
import json
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq

# 🌿 Sanjeevini: Fast, Groq-powered Ayurveda Agent with JSON Integration

# Load JSON data
def load_plant_data():
    try:
        with open("indian_medicinal_plants_metadata.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("Error: indian_medicinal_plants_metadata.json file not found.")
        return []

plant_data = load_plant_data()

# Function to search for plant information
def get_plant_info(query):
    query = query.lower()
    for plant in plant_data:
        if (plant["Plant Name"].lower() in query or 
            plant["Common Name"].lower() in query or 
            plant["Botanical Name"].lower() in query):
            return plant
    return None

# Groq Setup
llm = ChatGroq(
    groq_api_key="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",
    model_name="llama3-8b-8192"
)

# Prompt Template
template = """
You are Sanjeevini Agent, an expert in Indian medicinal plants and Ayurveda. Use the provided plant data and your Ayurvedic knowledge to answer clearly and concisely. If specific plant data is available, include details like botanical name, ethnomedicinal uses, and pharmacological activities. Avoid any tech or software references.

**Plant Data**: {plant_info}

**User Question**: {query}
"""
prompt = PromptTemplate(
    input_variables=["plant_info", "query"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)

# Streamlit UI
st.set_page_config(page_title="🌿 Sanjeevini Agent", layout="centered")

# Custom styles for larger fonts and centered layout
st.markdown("""
<style>
    html, body, [class*="css"]  {
        font-size: 18px !important;
    }
    .stChatMessageContent p {
        font-size: 18px !important;
    }
    .stTextInput>div>div>input {
        font-size: 18px !important;
        text-align: center;
    }
    .block-container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌿 Sanjeevini Agent")
st.markdown("<p style='font-size:20px;'>Ask me anything about Indian medicinal plants and Ayurveda!</p>", unsafe_allow_html=True)

# Chat input
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("💬 Ask your question")

if user_input:
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    
    # Search for plant in JSON data
    plant_info = get_plant_info(user_input)
    if plant_info:
        plant_info_str = (
            f"Plant Name: {plant_info['Plant Name']}\n"
            f"Botanical Name: {plant_info['Botanical Name']}\n"
            f"Common Name: {plant_info['Common Name']}\n"
            f"Family: {plant_info['Family']}\n"
            f"Phytochemical Compounds: {plant_info['Phytochemical Compounds']}\n"
            f"Ethnomedicinal Uses: {plant_info['Ethnomedicinal Uses']}\n"
            f"Pharmacological Activities: {plant_info['Pharmacological Activities']}\n"
            f"Source Reference: {plant_info['Source Reference']}"
        )
    else:
        plant_info_str = "No specific plant data found in the database. Please provide general Ayurvedic knowledge."
    
    # Run the chain with plant info and user query
    response = chain.run(query=user_input, plant_info=plant_info_str)
    st.session_state.chat_history.append({"role": "ai", "text": response})

# Display chat
for msg in st.session_state.chat_history:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["text"], unsafe_allow_html=True)

# Sidebar with popular plants
with st.sidebar:
    st.header("🌱 Popular Medicinal Plants")
    popular_plants = [
        ("Tulsi", "Ocimum tenuiflorum"),
        ("Neem", "Azadirachta indica"),
        ("Amla", "Phyllanthus emblica"),
        ("Ashwagandha", "Withania somnifera"),
        ("Brahmi", "Bacopa monnieri"),
        ("Turmeric", "Curcuma longa")
    ]
    for common, botanical in popular_plants:
        st.markdown(f"**🌿 {common}**", unsafe_allow_html=True)
        st.caption(f"*{botanical}*")