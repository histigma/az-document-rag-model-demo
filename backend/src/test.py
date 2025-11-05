from fastapi import FastAPI
from typing import Optional
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

app = FastAPI()

# Request 모델 정의
from pydantic import BaseModel
class QueryRequest(BaseModel):
    question: str
    k: Optional[int] = 3  # 상위 k개 문서 검색

# 벡터 DB와 RAG 모델 초기화 (예시)
embedding_model = OpenAIEmbeddings(openai_api_key="YOUR_KEY")
vectorstore = FAISS.load_local("faiss_index", embedding_model)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(openai_api_key="YOUR_KEY"),
                                       chain_type="stuff",
                                       retriever=retriever)

@app.post("/query")
def query_rag(request: QueryRequest):
    result = qa_chain.run(request.question)
    return {"answer": result}
