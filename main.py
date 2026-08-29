from app.assistant import Assistant
from app.llm import LLMClient
from app.memory import Memory
from app.rag import RAG

llm = LLMClient()
memory = Memory(llm)
rag = RAG()
assistant = Assistant(llm, memory, rag)

while True:
    q=input("You: ")
    if q.lower() in {"exit","quit"}:
        break
    print("\nAI:")
    response = assistant.ask(q)
    print(response.content)
    print()
    
    print("──────────────────────────")
    print(f"Messages:           {assistant.memory.size()}")
    print(f"Prompt Tokens:      {response.prompt_tokens}")
    print(f"Completion Tokens:  {response.completion_tokens}")
    print(f"Total Tokens:       {response.total_tokens}")
    print(f"Response Time:      {response.response_time:.2f} s")
    print("──────────────────────────")
