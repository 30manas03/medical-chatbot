


from flask import Flask, render_template, jsonify, request, session
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from src.prompt import *
import os
import markdown

app = Flask(__name__)

# Add a secret key for session management
app.secret_key = os.urandom(24)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

embeddings = download_hugging_face_embeddings()

index_name = "medical-chatbot-1"
docsearch = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embeddings)

llm = ChatGroq(model="gemma2-9b-it",api_key=GROQ_API_KEY)

# Prompt to reformulate a question based on chat history
history_aware_prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
])

# Create a retriever that considers conversation history
history_aware_retriever = create_history_aware_retriever(llm, docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3}), history_aware_prompt)

# Prompt for answering the question
# qa_prompt = ChatPromptTemplate.from_messages([
#     ("system", "Answer the user's questions based on the below context:\n\n{context}"),
#     MessagesPlaceholder(variable_name="chat_history"),
#     ("user", "{input}"),
# ])
system_prompt = (
    "You are an Medical assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use ten sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
])

# Chain to combine documents and generate an answer
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

# Final retrieval chain
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    # Initialize chat history in session if it doesn't exist
    if 'chat_history' not in session:
        session['chat_history'] = []

    msg = request.form["msg"]
    input = msg
    print(input)

    # Convert session history to LangChain message format
    chat_history_messages = []
    for human, ai in session['chat_history']:
        chat_history_messages.append(HumanMessage(content=human))
        chat_history_messages.append(AIMessage(content=ai))

    # Invoke the chain with the current input and history
    result = rag_chain.invoke({"input": input, "chat_history": chat_history_messages})
    answer = result["answer"]

    html_answer = markdown.markdown(answer)

    # Update session chat history
    session['chat_history'].append((input, answer))
    session.modified = True  # Ensure the session is saved

    return str(html_answer)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host="0.0.0.0", port=port, debug=False)