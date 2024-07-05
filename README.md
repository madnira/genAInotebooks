# genAInotebooks


*model folder* contains the hugging face models saved locally
-- all-mpnet-base-v2 model Readme file which shares the details of this open source model from hugging face

*notebooks folder* contains all the jupyter notebook files
- chunking.ipynb -> PyPDF library is used to extract texts from pdf files and create chunks
- embedding.ipynb -> opens source *sentence transformer* models are used from hugging face to create text embeddings from the chunked files. Storing the HF models locally is also demonstrated in this notebook
- vectordb_retrieval.ipynb -> *Milvus* is an open source vector DB tool which also provides Indexing for searching th vector embeddings. Milvus enables to create local vector db on your hard disk and use index search locally.
- rag.ipynb -> simple RAG based work flow of retreival text data from the vector db and passing on to a LLM with the user query is demonstrated. *Gemini-1.0-pro* is used as an LLM here over API call in python
