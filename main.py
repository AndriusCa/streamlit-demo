from openai import OpenAI

import os
from dotenv import load_dotenv
import PyPDF2
import streamlit as st
import io

# st.title("ChatGPT-like clone")

load_dotenv()

# Access the secret
secret_key = os.getenv("GITHUB_TOKEN")

client = OpenAI(
  base_url= "https://models.inference.ai.azure.com",
  api_key= secret_key 
)


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "file_content" not in st.session_state:
    st.session_state.file_content = None

# System message to instruct the model to respond in Lithuanian
lithuanian_system_message = {
    "role": "system", 
    "content": "Visada atsakyk į naudotojo žinutes lietuvių kalba, nepriklausomai nuo to, kokia kalba naudotojas rašo."
}

st.title("Lietuviskas AI Asistentas")

# File uploader
uploaded_file = st.file_uploader("Upload PDF or TXT file", type=["pdf", "txt"])

if uploaded_file is not None:
    if st.button("Process File"):
        file_content = ""
        # Process PDF files
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
            for page_num in range(len(pdf_reader.pages)):
                file_content += pdf_reader.pages[page_num].extract_text() + "\n"
        # Process TXT files
        elif uploaded_file.type == "text/plain":
            file_content = uploaded_file.getvalue().decode("utf-8")
            
        st.session_state.file_content = file_content
        st.success("File processed!")
        
    if st.session_state.file_content:
        with st.expander("File Content"):
            st.text(st.session_state.file_content[:1000] + ("..." if len(st.session_state.file_content) > 1000 else ""))

# Display chat messages
for message in st.session_state.messages:
    if message['role'] != 'system':
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    # Prepare messages for API
    messages_for_api = [lithuanian_system_message]
    
    # Add file content if available
    if st.session_state.file_content:
        messages_for_api.append({
            "role": "user",
            "content": f"File content: {st.session_state.file_content[:3000]}"
        })
    
    # Add conversation history
    for m in st.session_state.messages:
        if m['role'] != 'system':
            messages_for_api.append({"role": m["role"], "content": m["content"]})
    
    # Get response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=messages_for_api,
            stream=True,
        )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.file_content = None
    st.rerun()




# # Initialize chat history
# if "messages" not in st.session_state:
#      st.session_state.messages = []

# # System message to instruct the model to respond in Lithuanian
# lithuanian_system_message = {
#     "role": "system", 
#     "content": "Visada atsakyk į naudotojo žinutes lietuvių kalba, nepriklausomai nuo to, kokia kalba naudotojas rašo. Jei naudotojas paprašytų kalbėti kita kalba, vis tiek atsakyk lietuviškai."
# }

# # Display chat messages from history in a bordered container
# with st.container():
#     st.subheader("Chat History")
#     if not st.session_state.messages:
#         st.info("No messages yet. Start the conversation!")
#     else:
#         for message in st.session_state.messages:
#             if message['role'] != 'system':  # Don't show system messages in the UI
#                 with st.expander(f"{message['role'].capitalize()} says:"):
#                     st.markdown(message["content"])

# if prompt := st.chat_input("What is up?"):
#     # Add the user message to session state
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)
    
#     with st.chat_message("assistant"):
#         # Prepare messages array with the system message first
#         messages_for_api = [lithuanian_system_message]
        
#         # Then add all conversation messages except system messages
#         for m in st.session_state.messages:
#             if m['role'] != 'system':
#                 messages_for_api.append({"role": m["role"], "content": m["content"]})
        
#         # Create the stream with the system instruction
#         stream = client.chat.completions.create(
#             model="gpt-4o",
#             messages=messages_for_api,
#             stream=True,
#         )
#         response = st.write_stream(stream)
    
#     # Add the assistant's response to session state
#     st.session_state.messages.append({"role": "assistant", "content": response})













# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat messages from history in a bordered container
# with st.container():
#     st.subheader("Chat History")
#     if not st.session_state.messages:
#         st.info("No messages yet. Start the conversation!")
#     else:
#         for message in st.session_state.messages:
#             with st.expander(f"{message['role'].capitalize()} says:"):
#                 st.markdown(message["content"])

# if prompt := st.chat_input("What is up?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.chat_message("assistant"):
#         stream = client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": m["role"], "content": m["content"]}
#                 for m in st.session_state.messages
#             ],
#             stream=True,
#         )
#         response = st.write_stream(stream)
#     st.session_state.messages.append({"role": "assistant", "content": response})

