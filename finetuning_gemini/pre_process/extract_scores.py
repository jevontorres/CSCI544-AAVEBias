import re
import json

input_path = "/Users/kritee/Documents/CSCI544/dataset/sae_ind.txt"
output_path = "/Users/kritee/Documents/CSCI544/dataset/sae_ind.jsonl"

traits = ["Intelligence", "Determination", "Calmness", "Politeness", "Aggression",
          "Sophistication", "Incoherence", "Rudeness", "Stupidity",
          "Articulation", "Unsophistication", "Laziness"]

data = []
with open(input_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

i = 0
while i < len(lines):
    if lines[i].startswith("Input:"):
        entry = {}
        text = lines[i].replace("Input:", "").strip()
        entry["text"] = text
        entry["traits"] = {}

        # look for score lines
        for j in range(1, 20):  # up to 20 lines after Input
            if i + j >= len(lines):
                break
            line = lines[i + j].strip()
            match = re.match(rf"^({'|'.join(traits)}):\s*(\d+)", line)
            if match:
                trait, score = match.groups()
                entry["traits"][trait] = int(score)

        # ensure all traits are present
        if len(entry["traits"]) == len(traits):
            data.append(entry)
        i += j
    else:
        i += 1

# Write to JSONL
with open(output_path, "w", encoding='utf-8') as out_file:
    for item in data:
        out_file.write(json.dumps(item) + "\n")

print(f"✅ Converted {len(data)} entries to JSONL: {output_path}")
