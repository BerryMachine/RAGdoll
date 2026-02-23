RAG pipeline for school work made with ollama, chromadb, pypdf, marker.
LLM: deepseek-r1 (ollama)
Embedding: bge-m3 (ollama)



## IMPORTANT NOTES
chromadb's PersistentClient() is not compatible python@3.14+, specifically the config.py .
To fix this, I...
1. Used ModuleNotFoundError instead of ImportError (line 17)
2. Added fallback to pydantic_settings
3. Added type annotations for... (~line 268-282)
- ```chroma_coordinator_host: str = "localhost"```
- ```chroma_logservice_host: str = "localhost"```
- ```chroma_logservice_port: int = 50052```
4. Forced pydantic_settings for Python 3.14+
5. Removed pydantic.v1 validators on Python 3.14+ (~line 139)
6. Ensured pydantic-settings is in dependencies

Test Environment
- Python 3.14.3
- Mac M2 chip
- chromadb 1.5.1
- pydantic 2.12.5
- pydantic-settings 2.13.1

Additional dependencies required for this fix include: 
```pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-grpc```

Refer to the following 
https://github.com/chroma-core/chroma/issues/5996