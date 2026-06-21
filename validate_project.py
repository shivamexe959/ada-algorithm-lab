import os
import subprocess

def run_cmd(args):
    try:
        result = subprocess.run(args, capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

print("Starting validation check...")

# 1. Check file existence
required_files = [
    'index.html',
    'styles.css',
    'app.js',
    'scripts/algorithms.js',
    'scripts/visualizers.js'
]

missing_files = []
for f in required_files:
    if not os.path.exists(f):
        missing_files.append(f)

if missing_files:
    print("[ERROR] Missing files: " + str(missing_files))
    exit(1)
else:
    print("[OK] All required files exist.")

# 2. Check HTML script references
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

references = {
    'styles.css': 'href="styles.css"',
    'app.js': 'src="app.js"',
    'algorithms.js': 'src="scripts/algorithms.js"',
    'visualizers.js': 'src="scripts/visualizers.js"'
}

all_refs_ok = True
for name, ref in references.items():
    if ref not in html:
        print("[ERROR] index.html is missing reference to " + name + " ('" + ref + "')")
        all_refs_ok = False
    else:
        print("[OK] index.html references " + name)

if not all_refs_ok:
    exit(1)

# 3. Check JS files syntax using node --check
js_files = [
    'app.js',
    'scripts/algorithms.js',
    'scripts/visualizers.js'
]

all_js_ok = True
for f in js_files:
    ok, err = run_cmd(['node', '--check', f])
    if not ok:
        print("[ERROR] Syntax error in " + f + ":\n" + str(err))
        all_js_ok = False
    else:
        print("[OK] JavaScript syntax is valid for " + f)

if not all_js_ok:
    exit(1)

print("\nSUCCESS: The modular codebase is syntactically sound and references are correct.")
