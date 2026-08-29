from app.models.message import Message
from app.models.role import Role
from app.prompts import SYSTEM_PROMPT, MEMORY_CONTEXT_TEMPLATE
from app.config import SUMMARY_KEEP_LAST, SUMMARY_THRESHOLD
from app.summarizer import Summarizer


class Memory:
    def __init__(self, llm):
        self._messages = [Message(Role.SYSTEM, SYSTEM_PROMPT)]
        self._summary = None
        self._summarizer = Summarizer(llm)

    def _trim_history(self):
        history = self._messages[1:]
        if len(history) <= SUMMARY_THRESHOLD:
            return

        old_messages = history[:-SUMMARY_KEEP_LAST]
        recent_messages = history[-SUMMARY_KEEP_LAST:]

        print("\n========== SUMMARIZING ==========")
        if self._summary:
            print("\n--- PREVIOUS SUMMARY ---")
            print(self._summary.content)

        print("\n--- OLD MESSAGES ---")
        for message in old_messages:
            print(f"{message.role}: {message.content}")

        print("==================================\n")

        self._summary = self._summarizer.summarize(old_messages, self._summary)
        self._messages = [self._messages[0], *recent_messages]

    def _build_context(self):
        system_content = SYSTEM_PROMPT

        if self._summary:
            system_content += "\n\n" + MEMORY_CONTEXT_TEMPLATE.format(
                summary=self._summary.content
            )

        context = [
            Message(Role.SYSTEM, system_content)
        ]

        context.extend(self._messages[1:])
        return context

    def add_user(self, text: str):
        self._messages.append(Message(Role.USER, text))
        # self._trim_history()

    def add_assistant(self, text: str):
        self._messages.append(Message(Role.ASSISTANT, text))
        self._trim_history()

    def messages(self) -> list[Message]:
        return self._build_context()

    def size(self):
        return len(self._messages)
