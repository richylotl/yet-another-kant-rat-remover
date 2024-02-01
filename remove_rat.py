import re
import os
import shutil

if os.name == 'posix':  # Linux
    minecraft_folder = os.path.expanduser("~/.minecraft")
elif os.name == 'nt':  # Windows
    minecraft_folder = os.path.expandvars("%appdata%\\.minecraft")
else:
    print("Unsupported operating system.")
    exit()

for root, dirs, files in os.walk(os.path.join(minecraft_folder, "versions")):
    for filename in files:
        if filename.endswith(".json"):
            file_path = os.path.join(root, filename)

            with open(file_path, "r") as file:
                content = file.read()

            main_class_pattern = r'tweaker/([^/]+)/stub\.jar'
            main_match = re.search(main_class_pattern, content)
            if main_match:
                main_class = main_match.group(1)
            else:
                print(f"{filename}: This json doesn't seem to be infected")
                continue

            pattern = re.compile(r''',\s*{
\s+"name": "misc:tweaker:[^"]+",
\s+"downloads": {
\s+"artifact": {
\s+"path": "stub.jar",
\s+"sha1": "[^"]+",
\s+"size": \d+,
\s+"url": "https://tlrepo.cc/mvn/misc/tweaker/[^/]+/stub.jar"
\s+}
\s+}
\s+}''', re.DOTALL)

            match = pattern.search(content)

            pattern2 = re.compile(r""",
\s+{
\s+"name": "misc:tweaker:1.2",
\s+"url": "https://tlrepo.cc/mvn/"
\s+}""")

            match2 = pattern2.search(content)

            if match:
                content = pattern.sub('', content)
                if match2:
                    content = pattern2.sub('', content)
                with open(file_path, "w") as file:
                    file.write(content.replace("misc.tweaker.StubMain", main_class))
                print(f"{filename}: Changes made successfully")
            else:
                print(f"{filename}: This json doesn't seem to be infected")

tweaker_path = os.path.join(minecraft_folder, "libraries", "misc", "tweaker")
if os.path.exists(tweaker_path):
    shutil.rmtree(tweaker_path)
    print(f"Deleted {tweaker_path}")

print("My job seems to be done here!")
