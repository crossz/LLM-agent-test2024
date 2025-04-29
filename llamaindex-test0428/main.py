# 1. 环境配置 
import os 
from llama_index.core  import (
    VectorStoreIndex, 
    SimpleDirectoryReader,
    Settings,
    StorageContext,
    load_index_from_storage 
)
from llama_index.llms.openai  import OpenAI 
from llama_index.embeddings.huggingface import HuggingFaceEmbedding 
from llama_index.llms.openai_like import OpenAILike
from dotenv import load_dotenv 
 
# 加载环境变量 
load_dotenv()

# 使用 BGE 小型英文模型
# settings = Settings(
#     embed_model=HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
# )
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.embed_model = embed_model


 
# 2. 模型配置 
Settings.llm  = OpenAILike(
    temperature=0.1,
    model="Qwen/Qwen2.5-7B-Instruct",
    api_key=os.getenv("SILICONFLOW_API_KEY"), 
    api_base="https://api.siliconflow.cn/v1"   # 国内可用API端点[2]()
)
 
# 3. 数据准备函数 
def load_documents(data_dir):
    return SimpleDirectoryReader(
        input_dir=data_dir,
        required_exts=[".txt", ".pdf", ".docx"]  # 支持多种文档格式[7]()
    ).load_data()
 
# 4. 索引管理模块 
class IndexManager:
    def __init__(self, persist_dir="./storage"):
        self.persist_dir  = persist_dir 
        
    def create_index(self, documents):
        index = VectorStoreIndex.from_documents( 
            documents,
            show_progress=True  # 显示进度条[1]()
        )
        self._persist(index)
        return index 
    
    def load_index(self):
        storage_context = StorageContext.from_defaults(persist_dir=self.persist_dir) 
        return load_index_from_storage(storage_context)
    
    def _persist(self, index):
        index.storage_context.persist(persist_dir=self.persist_dir) 
 
# 5. 查询引擎 
class QueryEngine:
    def __init__(self, index):
        self.query_engine  = index.as_query_engine( 
            similarity_top_k=3,  # 返回前3个相关结果[3]()
            response_mode="compact"  # 压缩式响应 
        )
    
    def query(self, question):
        return self.query_engine.query(question) 
 
# 6. 主程序 
def main():
    data_dir = "./data"
    persist_dir = "./storage"
    
    # 初始化索引管理器 
    manager = IndexManager(persist_dir)
    
    # 检查是否已有存储的索引 
    if not os.path.exists(persist_dir): 
        print("创建新索引...")
        documents = load_documents(data_dir)
        index = manager.create_index(documents) 
    else:
        print("加载已有索引...")
        index = manager.load_index() 
    
    # 初始化查询引擎 
    engine = QueryEngine(index)
    
    # 示例查询 
    questions = [
        "文档的核心观点是什么？",
        "列出三个关键数据点",
        "作者的主要建议有哪些？"
    ]
    
    for q in questions:
        print(f"\n问题：{q}")
        response = engine.query(q) 
        print(f"回答：{response}")
 
if __name__ == "__main__":
    main()