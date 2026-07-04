import os
import glob

for f in glob.glob('tests/test_agents/*.py'):
    with open(f, 'r') as file:
        content = file.read()
    content = content.replace('mock_llm_factory(mock_response)()', 'mock_llm_factory(mock_response)')
    content = content.replace('mock_llm_factory(None)()', 'mock_llm_factory(None)')
    with open(f, 'w') as file:
        file.write(content)
