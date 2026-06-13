import base64
import json
import os
import re

js_file_path = "app/src/main/assets/fonts_base64.js"
output_dir = "app/src/main/res/font"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(js_file_path, "r", encoding="utf-8") as f:
    content = f.read()

# window.fontData = { ... };
json_str = content.strip()
if json_str.startswith("window.fontData ="):
    json_str = json_str[len("window.fontData ="):].strip()
if json_str.endswith(";"):
    json_str = json_str[:-1].strip()

# Remove trailing commas before closing braces (common in JS, invalid in JSON)
json_str = re.sub(r',\s*\}', '}', json_str)

try:
    font_data = json.loads(json_str)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    # Try a more robust way if it fails
    # Extract the object content
    match = re.search(r'\{.*\}', json_str, re.DOTALL)
    if match:
        json_str = match.group(0)
        # Still need to handle trailing commas in the extracted part
        json_str = re.sub(r',\s*\}', '}', json_str)
        font_data = json.loads(json_str)
    else:
        raise

mapping = {
    "BebasNeue-Regular.ttf": "bebas_neue.ttf",
    "DMSans-Regular.ttf": "dm_sans.ttf",
    "DMSans-Bold.ttf": "dm_sans_bold.ttf"
}

for src_name, target_name in mapping.items():
    if src_name in font_data:
        print(f"Extracting {src_name} to {target_name}...")
        b64_data = font_data[src_name]
        font_bytes = base64.b64decode(b64_data)
        with open(os.path.join(output_dir, target_name), "wb") as f:
            f.write(font_bytes)
    else:
        print(f"Warning: {src_name} not found in font data.")
