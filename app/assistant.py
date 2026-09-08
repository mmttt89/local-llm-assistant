from app.llm import LLMClient
from app.memory import Memory
from app.models.message import Message
from app.models.role import Role
from app.prompts import RAG_PROMPT
from app.rag import RAG


class Assistant:

    def __init__(
        self,
        llm,
        memory,
        rag: RAG | None = None,
    ):
        self.memory = memory
        self.llm = llm
        self.rag = rag

    def ask(self, question: str) -> str:
        self.memory.add_user(question)
        messages = self.memory.messages()

        # Search our knowledge base

        if self.rag is not None:
            results = self.rag.search(question, top_k=1)
            if results:
                context = "\n\n---\n\n".join(
                    f"Source: {result['source']}\n"
                    f"Similarity: {result['score']:.3f}\n"
                    f"{result['text']}"
                    for result in results
                )
                rag_message = Message(
                    Role.SYSTEM,
                    RAG_PROMPT.format(context=context),
                )

                messages = [
                    messages[0],
                    rag_message,
                    *messages[1:],
                ]

        response = self.llm.chat(messages)

        self.memory.add_assistant(response.content)

        return response
