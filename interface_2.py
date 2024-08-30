import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
import os
import base64
import tempfile
# Set the path where the vector stores will be saved
vectorstore_path = "hypothesis_2/vector_stores"

def process_pdf_file(pdf_file):
    # Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.read())
        tmp_file_path = tmp_file.name
    
    # If the vector store does not exist, create it
    print("Vector store not found. Creating a new one...")
    print("pdf" + tmp_file_path)
    loader = PyPDFLoader(file_path=tmp_file_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50, separator="\n")
    docs = text_splitter.split_documents(documents=documents)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(vectorstore_path)
    print("Vector store created and saved.")


def openai_prompt(prompt_text):
    # Instantiate the OpenAI model object
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    # Define the messages for the OpenAI call
    messages = [
        ("system", "You are a helpful assistant that responds to user prompts."),
        ("human", prompt_text),
    ]

    # Invoke the OpenAI model with the messages
    ai_msg = llm.invoke(messages)

    # Return the content of the response
    return ai_msg.content

# Initialize the QA system
def qa(prompt):
    # Perform the similarity search in the vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever()
    
    # Search the vector store for similar documents
    similar_docs = retriever.get_relevant_documents(prompt)

    # Combine similar document content
    context = "\n".join([doc.page_content for doc in similar_docs])

    # Use the generated prompt and context to create the function
    return openai_prompt(f"{prompt}. \n\n In the following you can find the information about the sensor {context}")



# Function to convert image file to base64
def get_image_base64(path):
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return f"data:image/jpg;base64,{encoded}"

# Load images and convert to base64
# user_icon_base64 = get_image_base64("path_to_user_icon.jpg")
agent_icon_base64 = get_image_base64("assets/agsotec_icon.png")

def run_similiarity_search_interface():
    st.title('Similarity Search Interface')
    
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        print(uploaded_file)
        process_pdf_file(uploaded_file)
        st.success('File successfully processed and stored in vector store!')

    # Initialize the conversation in session state if it doesn't exist
    if 'conversation' not in st.session_state:
        st.session_state.conversation = [f"<div class='containerMessage'><img src='{agent_icon_base64}'/> <div class='message'>Hello there</div> </div>"]
        
    with st.form(key='agent_form'):
        prompt = st.text_area("Enter your prompt:", help="Enter a prompt to run the agent.")
        submit_button = st.form_submit_button(label='Send')

    if submit_button and prompt:
        # Append user message to the conversation with an icon
        st.session_state.conversation.append(f"<div style='margin-left: 30%'><div class='message user'><img src='{agent_icon_base64}' alt='Agent' style='height:20px;width:20px; margin-left:95%;margin-top:5%;'/></div>{prompt}</div>")
        
        if prompt:
                with st.spinner('Running the agent...'):
                    output = qa().run(prompt)

                    # Agentennachrichten zur Konversation hinzufügen
                    st.session_state.conversation.append(f"<div style='width:70%'><div class='message agent'><img src='{agent_icon_base64}' alt='Agent' style='height:20px;width:20px;'/> </div>{output}</div>")
                
        else:
            st.error("Please enter a prompt.")

    # Display the conversation
    for message_html in reversed(st.session_state.conversation):
        st.markdown(message_html, unsafe_allow_html=True)


def run_similiarity_search_interface2():
    # st.title('Similarity Search Interface')
    
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        process_pdf_file(uploaded_file)
        st.success('File successfully processed and stored in vector store!')

    # Initialize the conversation in session state if it doesn't exist
    if 'conversation' not in st.session_state:
        st.session_state.conversation = [f"<div class='containerMessage'><img src='{agent_icon_base64}'/> <div class='message'>Hello there</div> </div>"]
        
    with st.form(key='agent_form'):
        prompt = st.text_area("Enter your prompt:", help="Enter a prompt to run the agent.")
        submit_button = st.form_submit_button(label='Send')

    if submit_button and prompt:
        # Append user message to the conversation with an icon
        st.session_state.conversation.append(f"<div style='margin-left: 30%'><div class='message user'><img src='{agent_icon_base64}' alt='Agent' style='height:20px;width:20px; margin-left:95%;margin-top:5%;'/></div>{prompt}</div>")
        
        if prompt:
                with st.spinner('Running the agent...'):
                    output = qa(prompt)

                    # Agentennachrichten zur Konversation hinzufügen
                    st.session_state.conversation.append(f"<div style='width:70%'><div class='message agent'><img src='{agent_icon_base64}' alt='Agent' style='height:20px;width:20px;'/> </div>{output}</div>")
                
        else:
            st.error("Please enter a prompt.")

    # Display the conversation
    for message_html in reversed(st.session_state.conversation):
        st.markdown(message_html, unsafe_allow_html=True)

run_similiarity_search_interface2()



