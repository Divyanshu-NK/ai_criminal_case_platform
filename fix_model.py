import os

agent_dir = r"d:\scratch\ai_criminal_case_platform\app\agents"
for root, _, files in os.walk(agent_dir):
    for f in files:
        if f.endswith(".py"):
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
            updated = False
            for old_model in ['gemini-3.5-flash', 'gemini-2.5-pro', 'gemini-2.5-flash']:
                if old_model in content:
                    content = content.replace(old_model, 'gemini-2.5-flash')
                    updated = True
            if updated:
                with open(path, "w", encoding="utf-8") as file:
                    file.write(content)
                print(f"Updated {path}")

