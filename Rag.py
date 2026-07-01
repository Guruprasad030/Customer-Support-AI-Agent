import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

load_dotenv()


class RAGEngine:

    def __init__(self):

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.3
        )

        self.vectorstore = None
        self.qa_chain = None

    def load_documents(self, folder="data"):

        documents = []

        for file in os.listdir(folder):

            if file.endswith(".pdf"):

                loader = PyPDFLoader(
                    os.path.join(folder, file)
                )

                documents.extend(loader.load())

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = splitter.split_documents(documents)

        self.vectorstore = FAISS.from_documents(
            chunks,
            self.embedding_model
        )

        self.vectorstore.save_local("vectorstore")

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 3}
            ),
            return_source_documents=True
        )

    def load_vectorstore(self):

        self.vectorstore = FAISS.load_local(
            "vectorstore",
            self.embedding_model,
            allow_dangerous_deserialization=True
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 3}
            ),
            return_source_documents=True
        )

    def ask(self, question):

        if self.qa_chain is None:
            self.load_vectorstore()

        result = self.qa_chain.invoke({"query": question})

        return {
            "answer": result["result"],
            "sources": result["source_documents"]
                  }
