import json
from sklearn.model_selection import train_test_split

# Load JSON file
with open("indiv_chatgpt3.5turbo.json", "r") as f:
    data = json.load(f)  # This should be a list

# Split
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Save to new JSON files
with open("train_trimmed.json", "w") as f_train:
    json.dump(train_data, f_train, indent=2)

with open("test_trimmed.json", "w") as f_test:
    json.dump(test_data, f_test, indent=2)