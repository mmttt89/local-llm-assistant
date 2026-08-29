🤖 Local AI Coding Assistant

A local AI assistant built with Python + LM Studio, designed to explore how modern AI assistants work under the hood.

Instead of relying on a hosted AI API, this project runs the language model locally and gradually builds the capabilities normally found in larger AI assistants — including conversation memory, summarization, embeddings, and Retrieval-Augmented Generation (RAG).

🚧 Work in progress

This is an experimental/learning project. The architecture and implementation are evolving as new AI concepts are introduced and tested.

⸻

✨ What can it do?

The assistant currently supports:

* 🧠 Local LLM inference through LM Studio
* 💬 Conversation history
* 📝 Long-term conversation summarization
* 🔎 Semantic search using embeddings
* 📚 Retrieval-Augmented Generation (RAG)
* 🎯 Similarity-based retrieval filtering
* ⚡ Token and response-time statistics

The goal is not simply to build a chatbot, but to understand how the individual pieces of an AI assistant work together.

⸻

🏗️ Architecture

The current architecture is intentionally simple:

                         ┌───────────────┐
                         │   User Input  │
                         └───────┬───────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │    Assistant    │
                        └───────┬─────────┘
                                │
                 ┌──────────────┼──────────────┐
                 │              │              │
                 ▼              ▼              ▼
             Memory           RAG            LLM
                 │              │              │
                 │              ▼              │
                 │         Embeddings          │
                 │              │              │
                 │              ▼              │
                 │      Relevant Context       │
                 │              │              │
                 └──────────────┼──────────────┘
                                │
                                ▼
                         ┌───────────────┐
                         │     Qwen      │
                         │   via LM      │
                         │    Studio     │
                         └───────┬───────┘
                                 │
                                 ▼
                              Response

⸻

📁 Project Structure

```
chat/
│
├── app/
│   ├── main.py
│   ├── assistant.py       # Coordinates the assistant
│   ├── llm.py             # LM Studio API client
│   ├── memory.py          # Conversation history
│   ├── summarizer.py      # Compresses older conversations
│   ├── embeddings.py      # Embedding model client
│   ├── rag.py             # Retrieval-Augmented Generation
│   ├── prompts.py         # System and task prompts
│   ├── config.py          # Application configuration
│   │
│   └── models/
│       ├── message.py
│       ├── role.py
│       └── llm_response.py
│
├── documents/
│   ├── architecture.md
│   ├── authentication.md
│   └── networking.md
│
└── README.md
```

⸻

🧩 How the pieces work

LLM

llm.py communicates with the OpenAI-compatible API provided by LM Studio.

```
Python
   ↓
LM Studio API
   ↓
Local LLM
   ↓
Response

The current generation model is Qwen.
```

⸻

Memory

memory.py keeps track of the conversation.

Recent messages remain available to the model while older conversations can be compressed into a summary.

```
Conversation
     │
     ├── Recent messages
     │
     └── Older messages
              ↓
          Summarizer
              ↓
        Long-term summary

This prevents the conversation history from growing indefinitely.
```

⸻

Summarization

summarizer.py extracts durable information from older conversations.

For example:
```
User:
"My favorite food is kebab."
        ↓
Memory summary:
- User's favorite food is kebab.

The goal is to preserve useful information while reducing the number of tokens sent to the model.
```

⸻

Embeddings

embeddings.py communicates with a local embedding model.

Currently the project uses: **Nomic Embed Text v1.5**

Text is converted into a numerical vector:

```
"JWT authentication"
        ↓
Embedding model
        ↓
[0.12, -0.08, 0.31, ...]

These vectors allow the application to compare the semantic similarity between pieces of text.
```
⸻

RAG

rag.py implements the current Retrieval-Augmented Generation pipeline.

The process is:
```
Documents
    ↓
Chunks
    ↓
Embeddings
    ↓
Similarity search
    ↓
Relevant chunks
    ↓
Qwen
    ↓
Answer
```

For example, when asking:

```
How does authentication work?
```

the assistant can retrieve relevant information from:

```
documents/authentication.md
```

and provide it to the language model as additional context.
⸻

🔍 Semantic Search

The project currently uses cosine similarity to compare the embedding of the user’s question with the embeddings of document chunks.

Conceptually:
```
User question
      ↓
Embedding
      ↓
Query vector
      │
      ▼
Compare against document vectors
      │
      ▼
Similarity scores
      │
      ▼
Filter weak matches
      │
      ▼
Relevant context
```

A similarity threshold prevents unrelated documents from being sent to the model.

⸻

📊 Token Usage

The assistant also reports token usage and response time:
```
──────────────────────────
Messages:           7
Prompt Tokens:      276
Completion Tokens:  159
Total Tokens:       435
Response Time:      6.49 s
──────────────────────────
```

This makes it easier to observe how conversation history and retrieved context affect the model’s performance.

⸻

🚀 Getting Started

Requirements

You will need:

* Python 3.10+
* LM Studio
* A compatible local language model
* A compatible embedding model
* Enough RAM/VRAM for the models you choose

The project currently uses:

LLM:
Qwen 7B
Embedding:
Nomic Embed Text v1.5

⸻

1. Clone the repository

git clone https://github.com/mmttt89/local-llm-assistant.git
cd local-llm-assistant

⸻

2. Install dependencies

Install the required Python package:

pip install requests

⸻

3. Start LM Studio

Load your language model and embedding model in LM Studio and start the local server.

The application expects an OpenAI-compatible endpoint:

http://localhost:1234

⸻

4. Configure the models

Update:

app/config.py

Example:
```
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
EMBEDDING_URL = "http://localhost:1234/v1/embeddings"
EMBEDDING_MODEL = "text-embedding-nomic-embed-text-v1.5"
MODEL = "qwen"
TEMPERATURE = 0.2
MAX_TOKENS = 1024
SUMMARY_THRESHOLD = 14
SUMMARY_KEEP_LAST = 6
```

Note: **Make sure the model identifiers match the models exposed by your LM Studio server.**

⸻


5. Run the assistant

From the project root:

python3 main.py

Then start chatting:

You: How does authentication work?
AI:
The application uses JWT authentication...

⸻

🛣️ Roadmap

The project is being developed incrementally.

✅ Completed

* Local LLM communication
* Conversation history
* Sliding conversation window
* Conversation summarization
* Local embeddings
* Semantic similarity search
* Similarity threshold
* Basic RAG integration
* Token and response-time monitoring

🔨 Next

* Persistent embedding index
* Better document chunking
* Document metadata
* Improved retrieval/ranking
* RAG evaluation
* Persistent vector database
* Web search / external knowledge
* Tool calling
* Agent capabilities

The roadmap may change as the project evolves.

⸻

🎯 Why this project?

Large AI assistants can feel like magic.

This project is an attempt to break that magic down into understandable components.

Instead of asking:

“How does an AI assistant work?”

the project explores the question one component at a time:
```
LLM
 ↓
Conversation History
 ↓
Memory
 ↓
Summarization
 ↓
Embeddings
 ↓
Semantic Search
 ↓
RAG
 ↓
Tools
 ↓
Agents
```

The goal is to understand why each component exists, what problem it solves, and how it changes the behavior of the assistant.

⸻

🤝 Contributions

This project is primarily a learning experiment, but ideas, improvements, issues, and discussions are welcome.

If you find something interesting or have a better approach, feel free to open an issue or pull request.

⸻

📜 License

Add your preferred license here.

For an open-source learning project, MIT is a simple choice.