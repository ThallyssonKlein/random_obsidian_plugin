import json
import random
import requests
import os

JSON_URL = "https://raw.githubusercontent.com/obsidianmd/obsidian-releases/HEAD/community-plugins.json"  # Substitua pela URL real
SORTED_FILES = "sorted.json"


def fetch_data_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting JSON: {e}")
        return None


def load_sorteds():
    if os.path.exists(SORTED_FILES):
        with open(SORTED_FILES, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_sorted(objeto):
    sorted = load_sorteds()
    sorted.append(objeto)

    with open(SORTED_FILES, "w", encoding="utf-8") as f:
        json.dump(sorted, f, indent=4, ensure_ascii=False)


def save_new(dados, sorteados):
    rest = [item for item in dados if item not in sorteados]

    if not rest:
        print("All items were sorted!")
        return None

    chosen = random.choice(rest)
    save_sorted(chosen)
    return chosen


def main():
    data = fetch_data_from_url(JSON_URL)
    if not isinstance(data, list):
        print("The json does not contain a valid array.")
        return

    sorteds = load_sorteds()
    chosen = save_new(data, sorteds)

    if chosen:
        print("Sorted object:")
        print(json.dumps(chosen, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
