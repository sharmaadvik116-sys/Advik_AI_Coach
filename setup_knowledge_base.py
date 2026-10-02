import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# Load the same .env file used by app.py
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY was not found in .env")


client = OpenAI(api_key=api_key)


# Find the knowledge folder
knowledge_folder = Path(__file__).parent / "knowledge"


if not knowledge_folder.exists():
    raise FileNotFoundError(
        "The knowledge folder was not found."
    )


# Find all Markdown knowledge files
knowledge_files = sorted(
    knowledge_folder.glob("*.md")
)


if not knowledge_files:
    raise FileNotFoundError(
        "No Markdown files were found in the knowledge folder."
    )


print()
print("Creating a new Remote Sensing knowledge base...")
print()


# Create a new vector store
vector_store = client.vector_stores.create(
    name="Advik Remote Sensing Knowledge Base"
)


print(f"Knowledge base created: {vector_store.id}")
print()
print(f"Found {len(knowledge_files)} knowledge files.")
print()


# Upload every knowledge file
for file_path in knowledge_files:

    print(f"Uploading: {file_path.name}")

    with open(file_path, "rb") as file:

        result = client.vector_stores.files.upload_and_poll(
            vector_store_id=vector_store.id,
            file=file
        )

    print(f"Completed: {file_path.name}")
    print(f"Status: {result.status}")
    print()


# Update .env with the new vector store ID
env_path = Path(__file__).parent / ".env"


existing_lines = []

if env_path.exists():
    existing_lines = env_path.read_text().splitlines()


new_lines = []

vector_store_line_found = False


for line in existing_lines:

    if line.startswith("REMOTE_SENSING_VECTOR_STORE_ID="):

        new_lines.append(
            f"REMOTE_SENSING_VECTOR_STORE_ID={vector_store.id}"
        )

        vector_store_line_found = True

    else:

        new_lines.append(line)


if not vector_store_line_found:

    new_lines.append(
        f"REMOTE_SENSING_VECTOR_STORE_ID={vector_store.id}"
    )


env_path.write_text(
    "\n".join(new_lines) + "\n"
)


print("=" * 60)
print("REMOTE SENSING KNOWLEDGE BASE READY")
print("=" * 60)

print()
print("New Vector Store ID:")
print(vector_store.id)

print()
print("The Vector Store ID has been updated automatically in .env.")
print()
print("Knowledge base setup complete.")