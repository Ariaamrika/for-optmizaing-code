import streamlit as st
import openai
import time
import os

# Streamlit app title
st.title("Contract Assistant")

# Instructions for the user
st.write("Upload a contract, and I'll help you review and suggest improvements.")

# Load OpenAI credentials from environment variables
openai.api_key = 'sk-PXMp-0lTnx3t3S4EZlNi3rkgXSZU95nCwdaEpzq8tsT3BlbkFJiGEwKEviccyRb6hXAq5YFKXBTO0321GkbrxrADs0AA'
assistant_id = 'asst_1NOkNSxpgxecCLcx0zKL1rq7'
thread_id = 'thread_XUioq42i4faTF85PVrv1YpVC'

if not openai.api_key or not assistant_id :
    st.error("Missing API key, assistant ID, or thread ID. Make sure they are set in environment variables.")
else:
    # File uploader for the user to upload the contract
    uploaded_file = st.file_uploader("Choose a contract file", type=["txt", "docx", "pdf"])

    # Function to process the message from the assistant
    def process_message_with_citations(message):
        return message['content']  # You can add further formatting here if needed.

    # If a file is uploaded
    if uploaded_file is not None:
        # Display the file content
        st.write("Processing the contract...")

        # Contract checking instructions
        contract_content = uploaded_file.getvalue().decode('utf-8')
        prompt = f'''
        Please review the following contract:
        
        {contract_content}
        
        1. Check for compliance with legal regulations.
        2. Identify missing sections or incomplete parts.
        3. Suggest improvements for clarity, fairness, and completeness.
        '''

        # Call OpenAI API to create a new run for the existing thread and assistant
        client = openai.ChatCompletion
        
        with st.spinner("Analyzing contract..."):
            response = client.create(
                model="gpt-4",
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                assistant_id=assistant_id,
                thread_id=thread_id
            )
            assistant_response = response['choices'][0]['message']['content']

        # Display the assistant's response
        st.write("Assistant's Response:")
        st.markdown(process_message_with_citations(assistant_response), unsafe_allow_html=True)

    else:
        st.write("Please upload a contract to get started.")
