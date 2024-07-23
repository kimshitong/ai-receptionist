from openai import OpenAI

# SECRET_KEY asst_La2WPtxgPEY5Mi2CxHt0G7s0
# API_KEY = "sk-proj-gnexVjdEJazJLhwjJFW7T3BlbkFJkOB8aAg4zQwilj"

API_KEY_TWO = ""
ASSISTANT_ID = ""

client = OpenAI(api_key=API_KEY_TWO)

my_assistants = client.beta.assistants.list(
    order="desc",
    limit="20",
)

my_assistant = client.beta.assistants.retrieve(ASSISTANT_ID)

# my_updated_assistant = client.beta.assistants.update(
#   ASSISTANT_ID,
#   instructions="You are an HR bot, and you have access to files to answer employee questions about company policies. Always response with info from either of the files.",
#   name="HR Helper",
#   tools=[{"type": "file_search"}],
#   model="gpt-4-turbo"
# )

empty_thread = client.beta.threads.create()
# {
#   "id": THREAD_ID,
#   "object": "thread",
#   "created_at": 1699012949,
#   "metadata": {},
#   "tool_resources": {}
# }

THREAD_ID = empty_thread['id']

my_thread = client.beta.threads.retrieve(empty_thread['id'])
# {
#   "id": THREAD_ID,
#   "object": "thread",
#   "created_at": 1699014083,
#   "metadata": {},
#   "tool_resources": {
#     "code_interpreter": {
#       "file_ids": []
#     }
#   }
# }


thread_message = client.beta.threads.messages.create(
  THREAD_ID,
  role="user",
  content="How does AI work? Explain it in simple terms.",
)
print(thread_message)
# {
#   "id": "msg_abc123",
#   "object": "thread.message",
#   "created_at": 1713226573,
#   "assistant_id": null,
#   "thread_id": "thread_abc123",
#   "run_id": null,
#   "role": "user",
#   "content": [
#     {
#       "type": "text",
#       "text": {
#         "value": "How does AI work? Explain it in simple terms.",
#         "annotations": []
#       }
#     }
#   ],
#   "attachments": [],
#   "metadata": {}
# }

thread_messages = client.beta.threads.messages.list("thread_abc123")

# {
#   "object": "list",
#   "data": [
#     {
#       "id": "msg_abc123",
#       "object": "thread.message",
#       "created_at": 1699016383,
#       "assistant_id": null,
#       "thread_id": "thread_abc123",
#       "run_id": null,
#       "role": "user",
#       "content": [
#         {
#           "type": "text",
#           "text": {
#             "value": "How does AI work? Explain it in simple terms.",
#             "annotations": []
#           }
#         }
#       ],
#       "attachments": [],
#       "metadata": {}
#     },
#     {
#       "id": "msg_abc456",
#       "object": "thread.message",
#       "created_at": 1699016383,
#       "assistant_id": null,
#       "thread_id": "thread_abc123",
#       "run_id": null,
#       "role": "user",
#       "content": [
#         {
#           "type": "text",
#           "text": {
#             "value": "Hello, what is AI?",
#             "annotations": []
#           }
#         }
#       ],
#       "attachments": [],
#       "metadata": {}
#     }
#   ],
#   "first_id": "msg_abc123",
#   "last_id": "msg_abc456",
#   "has_more": false
# }


from openai import OpenAI
client = OpenAI()

message = client.beta.threads.messages.retrieve(
  message_id="msg_abc123",
  thread_id="thread_abc123",
)
print(message)
