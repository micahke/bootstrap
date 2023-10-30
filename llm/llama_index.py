import hashlib
from typing import List
from llama_index.indices.base import BaseIndex
from llama_index.llms.utils import LLMType
from llama_index.schema import BaseNode
from llama_index.storage.docstore.simple_docstore import SimpleDocumentStore
from llama_index.storage.index_store.simple_index_store import SimpleIndexStore
from llama_index.vector_stores.simple import SimpleVectorStore
import openai
import os
from data.config import IndexType, ModelType
from data.errors import NO_API_KEY
from llama_index import Document, ServiceContext, StorageContext, TreeIndex, VectorStoreIndex, load_index_from_storage
from loader.customloader import CustomLoader
from util.fs import read_file
from llama_index.node_parser import SimpleNodeParser
from llama_index.llms import OpenAI
from util.fs import get_bootstrap_dir

class LlamaClient:
    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            print(NO_API_KEY)
            exit(0)
        else:
            openai.api_key = api_key

    def generate_doc(self, filepath: str) -> Document:
        filename = filepath.split('/')[-1]
        relative_path = os.path.relpath(filepath, os.getcwd())
        doc = CustomLoader.load(filepath)
        if doc:
            doc.metadata = {
                "file_name": filename,
                "relative_path": relative_path
            }
        else:
            doc =  Document(
                text=read_file(filepath),
                extra_info={
                    "file_name": filename,
                    "relative_path": relative_path
                }
            )
        # Set the ID as the MD5 hash of the filepath 
        hash = hashlib.md5(filepath.encode()).hexdigest()
        doc.id_ = hash
        return doc


    def parse_nodes(self, docs: List[Document]) -> List[BaseNode]:
        parser = SimpleNodeParser.from_defaults(
            chunk_size=512,
            chunk_overlap=20
        )
        nodes = parser.get_nodes_from_documents(docs)
        return nodes

    def generate_index_from_nodes(self, llm: LLMType, index_type: IndexType, nodes: List[BaseNode], progress: bool = False) -> BaseIndex:
        service_context = ServiceContext.from_defaults(
            llm=llm,
        )
        index = None
        if index_type == IndexType.TREE:
            index = TreeIndex(nodes, service_context=service_context, show_progress=progress)
        else:
            index = VectorStoreIndex(nodes, service_context=service_context, show_progress=progress)
        return index


    def query(self, index: BaseIndex, prompt: str):
        qe = index.as_query_engine(streaming=True)
        response = qe.query(prompt)

        print('\n')

        if hasattr(response, 'response_gen') and response.response_gen is not None:
            response_txt = ""
            for text in response.response_gen:
                print(text, end="", flush=True)
                response_txt += text
        print("\n")
            

    def save_index(self, index: BaseIndex):
        storagepath = os.path.join(get_bootstrap_dir(), "storage")
        index.storage_context.persist(storagepath)


    def load_index(self, llm: LLMType) -> BaseIndex:
        storagepath = os.path.join(get_bootstrap_dir(), "storage")
        storage_context = StorageContext.from_defaults(
            docstore=SimpleDocumentStore.from_persist_dir(persist_dir=storagepath),
            vector_store=SimpleVectorStore.from_persist_dir(persist_dir=storagepath),
            index_store=SimpleIndexStore.from_persist_dir(persist_dir=storagepath),
        )
        service_context = ServiceContext.from_defaults(
            llm=llm
        )
        index = load_index_from_storage(storage_context)
        index._service_context = service_context
        return index
