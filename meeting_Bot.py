import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.chat_models.oci_generative_ai import ChatOCIGenAI

# Load environment variables from .env file
load_dotenv()


COHERE_API_KEY = os.environ['COHERE_API_KEY']

import cohere

# compartment_id = os.environ["COMPARTMENT"]
# endpoint =  os.environ["SERVICE_ENDPOINT"]

# App title
st.title("Meeting Summary Generator")

# response = co.chat(model = 'command-a-03-2025',
#                        message = prompt)

# Transcript file uploader
uploaded_file = st.file_uploader("Upload meeting transcript (TXT)", type=["txt"])
if uploaded_file is not None:
    transcript_text = uploaded_file.read().decode("utf-8")
    st.text_area("Transcript Preview", transcript_text, height=200)

    # Generate summary when button is clicked
    if st.button("Generate Summary"):
        with st.spinner("Generating summary..."):
            # Load environment variables
            # load_dotenv()


            # Initialize OCI Gen AI Chat model
            llm = cohere.Client(COHERE_API_KEY)

            # Prepare prompt with transcript
            prompt = f"""
[ --- CONTEXT --- ] 
Attached/Below is the raw transcript of a 2-hour virtual meeting held today regarding Project Y. 
Key participants included Alice (Product Lead), Bob (Lead Engineer), and Charlie (Marketing Manager). 
The meeting covered Q2 roadmap planning, resource allocation challenges, and a review of recent user feedback.

[ --- ROLE --- ]
Act as a highly efficient executive assistant with expertise in creating concise, actionable meeting summaries for busy executives.

[ --- OBJECTIVE --- ]
Produce a concise summary of the meeting, focusing *only* on:
 - Key decisions made during the session. 
 - Specific action items assigned (clearly identify the owner and deadline if mentioned in the transcript). 
 - Any major unresolved issues or points requiring further discussion/escalation.

[ --- FORMAT --- ]
- Structure the summary using clear bullet points.
- Organize the bullet points under three distinct headings: "Key Decisions," "Action Items," and "Pending Issues / Points for Escalation." 
- The entire summary must fit on a single page (approximately 300-400 words maximum).

[ --- TONE / STYLE --- ]
- Adopt a purely factual, neutral, and professional tone. 
- The style must be extremely concise and objective. Avoid interpretations or opinions.

[ --- CONSTRAINTS --- ]
- Extract *only* information directly related to decisions, actions, and unresolved issues. Ignore off-topic discussions,
  general brainstorming, or lengthy debates unless they directly resulted in one of these outcomes. 
- For each action item, clearly state the item, the assigned owner's name (Alice, Bob, or Charlie), and the deadline, if specified in the transcript. 
  **Bold** the owner's name. 
- If an owner or deadline for an action is unclear from the transcript, note that explicitly (e.g., "Action: - Owner: Unclear, Deadline: Not specified").

[ --- TRANSCRIPT --- ]

{transcript_text}
"""
            # Get and display response
            response = llm.chat(model = 'command-a-03-2025',
                       message = prompt)
            st.subheader("Meeting Summary")
            st.markdown(response.text)

# Footer
st.write("---")
st.write("Powered by OCI Generative AI and Streamlit")
