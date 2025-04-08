import requests
import matplotlib.pyplot as plt
import os

USERNAME = "frostdev03"
TOKEN = os.getenv("GH_TOKEN")  # Save a GitHub token in your repo secrets

def fetch_repos(username):
    repos = []
    page = 1
    while True:
        print(f"Fetching page {page} of repos...")
        url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
        response = requests.get(url, headers={"Authorization": f"token {TOKEN}"})
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    print(f"Fetched {len(repos)} repos.")
    return repos


def fetch_languages(repo):
    url = repo["languages_url"]
    response = requests.get(url, headers={"Authorization": f"token {TOKEN}"})
    return response.json()

def aggregate_languages(repos):
    language_totals = {}
    for repo in repos:
        langs = fetch_languages(repo)
        for lang, bytes_used in langs.items():
            language_totals[lang] = language_totals.get(lang, 0) + bytes_used
    return language_totals

def plot_languages(language_totals):
    langs = list(language_totals.keys())
    sizes = list(language_totals.values())

    plt.figure(figsize=(10, 6))
    plt.pie(sizes, labels=langs, autopct="%1.1f%%", startangle=140)
    plt.axis("equal")
    plt.title(f"Programming Languages Used by {USERNAME}")
    plt.savefig("lang_stats.png", bbox_inches="tight")

def update_readme():
    with open("README.md", "w") as f:
        f.write(f"# 🧪 Language Usage Stats for `{USERNAME}`\n\n")
        f.write("This chart represents the total usage of programming languages across all public repositories.\n\n")
        f.write("![Language Stats](lang_stats.png)\n")

def main():
    print("Starting analysis...")
    repos = fetch_repos(USERNAME)
    if not repos:
        print("No repositories found or API failed.")
        return
    lang_totals = aggregate_languages(repos)
    print(f"Language data: {lang_totals}")
    plot_languages(lang_totals)
    update_readme()
    print("Done!")


if __name__ == "__main__":
    main()
