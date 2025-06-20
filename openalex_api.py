import requests

BASE_URL = "https://api.openalex.org"


def get_author(author_id):
    return requests.get(f"{BASE_URL}/authors/{author_id}").json()


def get_works_by_author(author_id):
    url = f"{BASE_URL}/works?filter=author.id:{author_id}&per-page=200"
    return requests.get(url).json()['results']


def get_related_concepts(work):
    return [concept['display_name'] for concept in work.get('concepts', [])]


def get_coauthors(works, author_id):
    coauthors = {}
    for work in works:
        for author in work.get('authorships', []):
            if author.get('author', {}).get('id') != author_id:
                name = author['author']['display_name']
                coauthors[name] = coauthors.get(name, 0) + 1
    return coauthors
