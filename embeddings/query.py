from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import RetrievalQAWithSourcesChain
from templates.system_prompt import SYSTEM_PROMPT
import toml

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

'''
def query():
    db = FAISS.load_local("faiss_index", _get_embeddings())
    model = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.5,
                       openai_api_key=get_openai_api_key(), streaming=True)  # max temperature is 2 least is 0
    retriever = db.as_retriever(search_kwargs={
                                         "k": sources},  qa_template=SYSTEM_PROMPT, question_generator_template=CONDENSE_PROMPT)  # 9 is the max sources
    qa = ConversationalRetrievalChain.from_llm(
        llm=model, retriever=retriever, return_source_documents=True)
    return qa
'''

def get_chain(db,system_prompt):
    chain_type_kwargs = {"prompt": system_prompt}
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        ChatOpenAI(temperature=0), 
        chain_type="stuff", 
        retriever=db.as_retriever(),
        chain_type_kwargs=chain_type_kwargs,
        reduce_k_below_max_tokens=True
    )
    return chain

def get_system_prompt():
    messages = [
        SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
    prompt = ChatPromptTemplate.from_messages(messages)
    return prompt

def _get_embeddings():
    model = "shibing624/text2vec-base-chinese"
    embeddings = HuggingFaceEmbeddings(model_name = model)
    return embeddings

def get_openai_api_key() -> str:
    with open(".streamlit/secrets.toml", "r") as secrets_file:
        secrets = toml.load(secrets_file)
    return secrets["OPENAI_KEY"]