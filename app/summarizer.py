from app.llm import LLMClient
from app.models.message import Message
from app.models.role import Role
from app.prompts import SUMMARY_PROMPT


class Summarizer:

    def __init__(self, llm):
        self.llm = llm

    def summarize(
        self,
        messages: list[Message],
        previous_summary: Message | None = None,
    ) -> Message:
        conversation = []

        if previous_summary is not None:

            conversation.append(
                Message(
                    Role.USER,
                    "Previous long-term memory:\n\n" + previous_summary.content,
                )
            )

        conversation.append(
            Message(
                Role.USER,
                "New conversation messages:\n\n"
                + "\n".join(
                    f"{message.role.value}: {message.content}" for message in messages
                ),
            )
        )

        prompt = [
            Message(Role.SYSTEM, SUMMARY_PROMPT),
            *conversation,
        ]

        response = self.llm.chat(prompt)

        return Message(
            Role.SYSTEM,
            response.content.strip(),
        )
