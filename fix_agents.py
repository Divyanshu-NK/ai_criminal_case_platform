import os
import re

agent_dir = r"d:\scratch\ai_criminal_case_platform\app\agents"

# Regex to match the ChatGoogleGenerativeAI instantiation blocks ending with .with_structured_output(...)
pattern = re.compile(
    r'self\.llm\s*=\s*ChatGoogleGenerativeAI\([^)]*\)\.with_structured_output\(([^)]+)\)',
    re.MULTILINE
)

for root, _, files in os.walk(agent_dir):
    for f in files:
        if f == "agent.py":
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
            
            updated = False
            
            if "from langchain_google_genai import ChatGoogleGenerativeAI" in content:
                content = content.replace("from langchain_google_genai import ChatGoogleGenerativeAI\n", "")
                updated = True
                
            if pattern.search(content):
                content = pattern.sub(r'self.llm = self.get_llm(\1)', content)
                updated = True
                
            if updated:
                with open(path, "w", encoding="utf-8") as file:
                    file.write(content)
                print(f"Updated {path}")
