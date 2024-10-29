from dotenv import load_dotenv
import os
from datetime import datetime
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw10_proj.settings")
django.setup()

from pymongo import MongoClient
from .models import Author, Quote, Tag


def get_mongodb():
    load_dotenv()

    user = os.getenv("MONGODB08_USER")
    password = os.getenv("MONGODB08_PASSWORD")
    base = os.getenv("MONGODB08_DB")
    domain = os.getenv("MONGODB08_HOST")

    uri = f"mongodb+srv://{user}:{password}@{domain}/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)
    db = client[base]

    return db


def fill_authors():
    db = get_mongodb()
    authors = db.authors.find()
    for author in authors:
        born_date_dt = datetime.strptime(author["born_date"], "%B %d, %Y")
        Author.objects.get_or_create(
            fullname=author["fullname"],
            born_date=born_date_dt,
            born_location=author["born_location"],
            description=author["description"],
        )


def fill_quotes():
    db = get_mongodb()
    quotes = db.quotes.find()
    for quote in quotes:
        # print(quote)
        tags = []
        for tag in quote["tags"]:
            t, ags = Tag.objects.get_or_create(name=tag)
            tags.append(t)

        author = db.authors.find_one({"_id": quote["author"]})
        author_p = Author.objects.get(fullname=author["fullname"])
        q, args = Quote.objects.get_or_create(
            author=author_p,
            quote=quote["quote"],
        )
        for tag in tags:
            q.tags.add(tag)


def fill_start():
    print("start Fill All")
    fill_authors()
    fill_quotes()
    print("stop Fill All")


if __name__ == "__main__":
    fill_start()
