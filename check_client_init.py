"""Check OpenAIChatClient initialization"""
import inspect
from agent_framework.openai import OpenAIChatClient

print("OpenAIChatClient.__init__ signature:")
print(inspect.signature(OpenAIChatClient.__init__))

print("\nOpenAIChatClient docstring:")
print(OpenAIChatClient.__doc__)

print("\nTrying to inspect the class:")
for attr in dir(OpenAIChatClient):
    if not attr.startswith('_'):
        print(f"  {attr}")

