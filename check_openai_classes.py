"""Check what's available in agent_framework.openai"""
import agent_framework.openai as openai_module

print("Available classes in agent_framework.openai:")
for item in dir(openai_module):
    if not item.startswith('_'):
        print(f"  - {item}")

