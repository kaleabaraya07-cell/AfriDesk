import os
import shutil

# Files to move to the afridesk package
files_to_move = [
    'assistant.py',
    'clinics.py',
    'figma.py',
    'locations.py',
    'questions.py',
    'response.py',
    'services.py'
]

# Create afridesk directory if it doesn't exist
os.makedirs('afridesk', exist_ok=True)

# Move files to afridesk directory
for file in files_to_move:
    if os.path.exists(file):
        shutil.move(file, os.path.join('afridesk', file))
        print(f'Moved {file} to afridesk/{file}')

print('\nFiles moved successfully. Please run the following command to update the imports:')
print('python update_imports.py')

# Create update_imports.py to update the imports
with open('update_imports.py', 'w') as f:
    f.write('''import os
import re

def update_imports(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update imports to use afridesk package
    updated_content = re.sub(
        r'^from\s+(?!afridesk\\.|\w+\s+import|\s*\Z)(\w+)\s+import',
        r'from afridesk.\1 import',
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

print('\nImports updated successfully. You can now run the application with:')
print('streamlit run app.py')
''')
