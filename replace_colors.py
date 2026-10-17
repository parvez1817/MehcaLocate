import os
import re

files_to_update = [
    'MechalocateLanding.html',
    'UserCentre.html',
    'UserLog.html',
    'UserReg.html',
    'UserDash.html',
    'Userdash.html',
    'ProLog.html',
    'ProReg.html',
    'Prodash.html',
    'ProCentre.html'
]

base_dir = r"c:\Users\parve\Videos\utube.py\mechalocatePython\config\templates"

replacements = {
    r'(?i)#0f2027': '#1a5140',
    r'(?i)#203a43': '#288760',
    r'(?i)#2c5364': '#5ca87c',
    r'(?i)#48dbfb': '#b7e5ba',
    r'(?i)#3b82f6': '#5ca87c',
    r'15,\s*32,\s*39': '26, 81, 64',
    r'32,\s*58,\s*67': '40, 135, 96',
    r'44,\s*83,\s*100': '92, 168, 124',
    r'72,\s*219,\s*251': '183, 229, 186',
    r'59,\s*130,\s*246': '92, 168, 124'
}

for filename in files_to_update:
    filepath = os.path.join(base_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        for pattern, replacement in replacements.items():
            content = re.sub(pattern, replacement, content)
            
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {filename}")
        else:
            print(f"No changes for {filename}")
    else:
        print(f"File not found: {filename}")
