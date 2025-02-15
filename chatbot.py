# An example LLM chatbot using Cohere API and Streamlit that references a PDF
# Adapted from the StreamLit OpenAI Chatbot example - https://github.com/streamlit/llm-examples/blob/main/Chatbot.py

# import streamlit as st
# import cohere
# import fitz # An alias for the PyMuPDF library.

# def pdf_to_documents(pdf_path):
#     """
#     Converts a PDF to a list of 'documents' which are chunks of a larger document that can be easily searched 
#     and processed by the Cohere LLM. Each 'document' chunk is a dictionary with a 'title' and 'snippet' key
    
#     Args:
#         pdf_path (str): The path to the PDF file.
    
#     Returns:
#         list: A list of dictionaries representing the documents. Each dictionary has a 'title' and 'snippet' key.
#         Example return value: [{"title": "Page 1 Section 1", "snippet": "Text snippet..."}, ...]
#     """

#     doc = fitz.open(pdf_path)
#     documents = []
#     text = ""
#     chunk_size = 1000
#     for page_num in range(len(doc)):
#         page = doc.load_page(page_num)
#         text = page.get_text()
#         part_num = 1
#         for i in range(0, len(text), chunk_size):
#             documents.append({"title": f"Page {page_num + 1} Part {part_num}", "snippet": text[i:i + chunk_size]})
#             part_num += 1
#     return documents

# # Check if a valid Cohere API key is found in the .streamlit/secrets.toml file
# # Learn more about Streamlit secrets here - https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management
# api_key_found = False
# if hasattr(st, "secrets"):
#     if "COHERE_API_KEY" in st.secrets.keys():
#         if st.secrets["COHERE_API_KEY"] not in ["", "4D7UmoRHr0pz1ZMCgbSTNOII3zb90bLOs1BLPFAt"]:
#             api_key_found = True

# # Add a sidebar to the Streamlit app
# with st.sidebar:
#     if api_key_found:
#         cohere_api_key = st.secrets["COHERE_API_KEY"]
#         # st.write("API key found.")
#     else:
#         cohere_api_key = st.text_input("Cohere API Key", key="chatbot_api_key", type="password")
#         st.markdown("[Get a Cohere API Key](https://dashboard.cohere.ai/api-keys)")
    
#     my_documents = []
#     selected_doc = st.selectbox("Select your departure location", ["Tai Tam Middle School", "Repulse Bay"])
#     if selected_doc == "Tai Tam Bus Schedule":
#         my_documents = pdf_to_documents('docs/HKISTaiTamBusSchedule.pdf')
#     elif selected_doc == "Repulse Bay Bus Schedule":    
#         my_documents = pdf_to_documents('docs/HKISRepulseBayBusSchedule.pdf')
#     else:
#         my_documents = pdf_to_documents('docs/HKISTaiTamBusSchedule.pdf')

#     # st.write(f"Selected document: {selected_doc}")

# # Set the title of the Streamlit app
# st.title("💬 HKIS Bus Helper")

# # Initialize the chat history with a greeting message
# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "Chatbot", "text": "Hi! I'm the HKIS Bus Helper. Select your location from the dropdown then ask me where you'd like to go and I'll do my best to find a school bus that will get you there."}]

# # Display the chat messages
# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["text"])

# # Get user input
# if prompt := st.chat_input():
#     # Stop responding if the user has not added the Cohere API key
#     if not cohere_api_key:
#         st.info("Please add your Cohere API key to continue.")
#         st.stop()

#     # Create a connection to the Cohere API
#     client = cohere.Client(api_key=cohere_api_key)
    
#     # Display the user message in the chat window
#     st.chat_message("User").write(prompt)

#     preamble = """You are the Hong Kong International School Bus Helper bot. You help people understand the bus schedule.
#     When someone mentions a location you should refer to the document to see if there are buses that stop nearby.
#     Respond with advice about which buses will stop the closest to their destination, the name of the stop they 
#     should get off at and the name of the suburb that the stop is located in. 
#     Finish with brief instructions for how they can get from the stop to their destination.
#     Group the buses you recommend by the time they depart. If the document is about Tai Tam then group your recommendations by the following departure times: 3:15, 4:20 and 5pm. 
#     If the document is about repulse bay then state the departure time is 4pm.
#     """

#     # Send the user message and pdf text to the model and capture the response
#     response = client.chat(chat_history=st.session_state.messages,
#                            message=prompt,
#                            documents=my_documents,
#                            prompt_truncation='AUTO',
#                            preamble=preamble)
    
#     # Add the user prompt to the chat history
#     st.session_state.messages.append({"role": "User", "text": prompt})
    
#     # Add the response to the chat history
#     msg = response.text
#     st.session_state.messages.append({"role": "Chatbot", "text": msg})

#     # Write the response to the chat window
#     st.chat_message("Chatbot").write(msg)



# import cohere
# import streamlit as st
# import os
# import textwrap
# import json

# # Check if a valid Cohere API key is found in the .streamlit/secrets.toml file
# # api_key_found = False
# # if hasattr(st, "secrets"):
# #     if "COHERE_API_KEY" in st.secrets.keys():
# #         if st.secrets["COHERE_API_KEY"] not in ["", "4D7UmoRHr0pz1ZMCgbSTNOII3zb90bLOs1BLPFAt"]:
# #             api_key_found = True

# # with st.sidebar:
# #     if api_key_found:
# #         cohere_api_key = st.secrets["COHERE_API_KEY"]
# #     else:
# #         cohere_api_key = st.text_input("Cohere API Key", key="chatbot_api_key", type="password")
# #         st.markdown("[Get a Cohere API Key](https://dashboard.cohere.ai/api-keys)")

# # Set up Cohere client
# co = cohere.ClientV2("4D7UmoRHr0pz1ZMCgbSTNOII3zb90bLOs1BLPFAt") # Get your free API key: https://dashboard.cohere.com/api-keys

# def generate_breakfast_idea(dietary_preference, temperature):
    
#     prompt = f"""
# Generate a breakfast idea based on the dietary preference. Return the breakfast idea without additional commentary.

# Dietary Preference: Vegetarian
# Breakfast Idea: Avocado toast with cherry tomatoes and a sprinkle of feta cheese

# Dietary Preference: Vegan
# Breakfast Idea: Smoothie bowl topped with granola, banana, and chia seeds

# Dietary Preference: Gluten-Free
# Breakfast Idea: Quinoa porridge with almond milk and fresh berries

# Dietary Preference: {dietary_preference}
# Breakfast Idea:"""

#     # Call the Cohere Chat endpoint
#     response = co.chat( 
#             messages=[{"role": "user", "content": prompt}],
#             model="command-r-plus-08-2024", 
#             temperature=temperature)
        
#     return response.message.content[0].text

# def generate_name(idea, temperature):
    
#     prompt= f"""
# Generate a catchy name for the breakfast idea. Return the name without additional commentary.

# Breakfast Idea: Avocado toast with cherry tomatoes and a sprinkle of feta cheese
# Breakfast Name: Avocado Delight

# Breakfast Idea: Smoothie bowl topped with granola, banana, and chia seeds
# Breakfast Name: Berry Bliss Bowl

# Breakfast Idea: Quinoa porridge with almond milk and fresh berries
# Breakfast Name: Quinoa Morning Magic

# Breakfast Idea: {idea}
# Breakfast Name:"""

#     # Call the Cohere Chat endpoint
#     response = co.chat( 
#             messages=[{"role": "user", "content": prompt}],
#             model="command-r-plus-08-2024", 
#             temperature=temperature)
        
#     return response.message.content[0].text

# # The front end code starts here

# st.title("🍳 Breakfast Idea Generator")

# form = st.form(key="user_settings")
# with form:
#   st.write("Enter your dietary preference [Example: Vegetarian, Vegan, Gluten-Free] ")
#   # User input - Dietary preference
#   dietary_input = st.text_input("Dietary Preference", key = "dietary_input")

#   # Create a two-column view
#   col1, col2 = st.columns(2)
#   with col1:
#       # User input - The number of ideas to generate
#       num_input = st.slider(
#         "Number of ideas", 
#         value = 3, 
#         key = "num_input", 
#         min_value=1, 
#         max_value=10,
#         help="Choose to generate between 1 to 10 ideas")
#   with col2:
#       # User input - The 'temperature' value representing the level of creativity
#       creativity_input = st.slider(
#         "Creativity", value = 0.5, 
#         key = "creativity_input", 
#         min_value=0.1, 
#         max_value=0.9,
#         help="Lower values generate more “predictable” output, higher values generate more “creative” output")  
#   # Submit button to start generating ideas
#   generate_button = form.form_submit_button("Generate Idea")

#   if generate_button:
#     if dietary_input == "":
#       st.error("Dietary preference field cannot be blank")
#     else:
#       my_bar = st.progress(0.05)
#       st.subheader("Breakfast Ideas:")

#       for i in range(num_input):
#           st.markdown("""---""")
#           breakfast_idea = generate_breakfast_idea(dietary_input, creativity_input)
#           breakfast_name = generate_name(breakfast_idea, creativity_input)
#           st.markdown("##### " + breakfast_name)
#           st.write(breakfast_idea)
#           my_bar.progress((i+1)/num_input)

# # Breakfast Helper Bot

# import streamlit as st
# import cohere

# # Check if a valid Cohere API key is found in the .streamlit/secrets.toml file
# api_key_found = False
# if hasattr(st, "secrets"):
#     if "COHERE_API_KEY" in st.secrets.keys():
#         if st.secrets["COHERE_API_KEY"] not in ["", "4D7UmoRHr0pz1ZMCgbSTNOII3zb90bLOs1BLPFAt"]:
#             api_key_found = True

# # Add a sidebar to the Streamlit app
# with st.sidebar:
#     if api_key_found:
#         cohere_api_key = st.secrets["COHERE_API_KEY"]
#     else:
#         cohere_api_key = st.text_input("Cohere API Key", key="chatbot_api_key", type="password")
#         st.markdown("[Get a Cohere API Key](https://dashboard.cohere.ai/api-keys)")

# # Set the title of the Streamlit app
# st.title("🍳 Breakfast Helper Bot")

# # Initialize the chat history with a greeting message
# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "Chatbot", "text": "Hi! I'm the Breakfast Helper Bot. Tell me your cuisine preference, dietary restrictions, and flavor profile, and I'll help you decide what to have for breakfast!"}]

# # Display the chat messages
# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["text"])

# # Get user input
# if prompt := st.chat_input():
#     # Stop responding if the user has not added the Cohere API key
#     if not cohere_api_key:
#         st.info("Please add your Cohere API key to continue.")
#         st.stop()

#     # Create a connection to the Cohere API
#     client = cohere.Client(api_key=cohere_api_key)
    
#     # Display the user message in the chat window
#     st.chat_message("User").write(prompt)

#     preamble = """You are the Breakfast Helper Bot. You assist users in deciding what to choose for breakfast based on their cuisine preferences, dietary restrictions, and flavor profiles. 
#     Provide suggestions that cater to their preferences and include brief descriptions of the dishes. 
#     Ask follow-up questions if necessary to refine the suggestions."""
    
#     # Send the user message to the model and capture the response
#     response = client.chat(chat_history=st.session_state.messages,
#                            message=prompt,
#                            prompt_truncation='AUTO',
#                            preamble=preamble)
    
#     # Add the user prompt to the chat history
#     st.session_state.messages.append({"role": "User", "text": prompt})
    
#     # Add the response to the chat history
#     msg = response.text
#     st.session_state.messages.append({"role": "Chatbot", "text": msg})

#     # Write the response to the chat window
#     st.chat_message("Chatbot").write(msg)

# # Customizing the appearance
# st.markdown(
#     """
#     <style>
#     .stChat {
#         background-color: #d4edda; /* Pastel light green */
#         border: 2px solid #8B4513; /* Brown outline */
#     }
#     .stChat .stChatInput {
#         background-color: #d4edda; /* Pastel light green */
#         border: 2px solid #8B4513; /* Brown outline */
#     }
#     .stChat .stChatInput button {
#         background-color: #add8e6; /* Light pastel blue */
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# Breakfast Helper Bot

import streamlit as st
import cohere

# Check if a valid Cohere API key is found in the .streamlit/secrets.toml file
api_key_found = False
if hasattr(st, "secrets"):
    if "COHERE_API_KEY" in st.secrets.keys():
        if st.secrets["COHERE_API_KEY"] not in ["", "4D7UmoRHr0pz1ZMCgbSTNOII3zb90bLOs1BLPFAt"]:
            api_key_found = True

# Add a sidebar to the Streamlit app
with st.sidebar:
    if api_key_found:
        cohere_api_key = st.secrets["COHERE_API_KEY"]
    else:
        cohere_api_key = st.text_input("Cohere API Key", key="chatbot_api_key", type="password")
        st.markdown("[Get a Cohere API Key](https://dashboard.cohere.ai/api-keys)")

# Set the title of the Streamlit app
st.title("🍳 Breakfast Helper Bot")

# Initialize the chat history with a greeting message
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "Chatbot", "text": "Hi! I'm the Breakfast Helper Bot. Tell me your cuisine preference, dietary restrictions, flavor profile, and age, and I'll help you decide what to have for breakfast!"}]

# Display the chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["text"])

# Get user input
if prompt := st.chat_input():
    # Stop responding if the user has not added the Cohere API key
    if not cohere_api_key:
        st.info("Please add your Cohere API key to continue.")
        st.stop()

    # Create a connection to the Cohere API
    client = cohere.Client(api_key=cohere_api_key)
    
    # Display the user message in the chat window
    st.chat_message("User").write(prompt)

    preamble = """You are the Breakfast Helper Bot. You assist users in deciding what to have for breakfast based on their cuisine preferences, dietary restrictions, flavor profiles, and age. Provide suggestions that cater to their preferences and explain why those options are suitable for them."""
    
    # Send the user message to the model and capture the response
    response = client.chat(chat_history=st.session_state.messages,
                           message=prompt,
                           prompt_truncation='AUTO',
                           preamble=preamble)
    
    # Add the user prompt to the chat history
    st.session_state.messages.append({"role": "User", "text": prompt})
    
    # Add the response to the chat history
    msg = response.text
    st.session_state.messages.append({"role": "Chatbot", "text": msg})

    # Write the response to the chat window
    st.chat_message("Chatbot").write(msg)

# Custom CSS for styling
st.markdown("""
<style>
    .stChat {
        background-color: #d4edda; 
        border: 2px solid #8B4513;
    }
    .stChat .stChatInput {
        background-color: #add8e6; 
    }
    .stChat .stChatMessage {
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
</style>
""", unsafe_allow_html=True)