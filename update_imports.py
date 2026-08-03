import os
import re

def update_imports(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update imports to use afridesk package
    updated_content = re.sub(
        r'^from\s+(?!afridesk\.|\w+\s+import|\s*\Z)(\w+)\s+import',
        r'from afridesk. import',
        content,
        flags=re.MULTILINE
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

# Update imports in all Python files
for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.py') and not file.startswith('update_imports'):
            file_path = os.path.join(root, file)
            print(f'Updating imports in {file_path}')
            update_imports(file_path)

print('
Imports updated successfully. You can now run the application with:')
print('streamlit run app.py')
