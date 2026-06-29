import os
import re

template_dir = r"c:\Users\mukesh kumar\.gemini\antigravity\scratch\projects\AIML_DEPT\templates"

def invert_theme():
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Replace rgba(255, 255, 255, 0.x) with rgba(0, 0, 0, 0.x)
                # Matches varying spacing e.g. rgba(255,255,255,0.1) or rgba(255, 255, 255, 0.1)
                content = re.sub(r'rgba\(\s*255\s*,\s*255\s*,\s*255\s*,', 'rgba(0, 0, 0,', content)
                
                # Replace 'color: white' or 'color: white;' with 'color: var(--text-primary)'
                content = re.sub(r'color:\s*white\s*;?', 'color: var(--text-primary);', content)
                
                # Also look out for 'text-fill-color: transparent' which is used in gradients, leave it alone.
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
    print("Theme inversion applied to all templates.")

if __name__ == '__main__':
    invert_theme()
