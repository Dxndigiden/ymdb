import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle
from reviews.models import Review, Title
from users.models import User


def import_category():
    with open('static/data/category.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            Category.objects.create(
                name=row['name'],
                slug=row['slug'],
            )


def import_comment():
    with open('static/data/comments.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            Comment.objects.create(
                text=row['text'],
                author_id=row['author'],
                pub_date=row['pub_date'],
                review_id=row['review_id'],
            )


def import_genre():
    with open('static/data/genre.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            Genre.objects.create(
                name=row['name'],
                slug=row['slug'],
            )


def import_review():
    with open('static/data/review.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            Review.objects.create(
                text=row['text'],
                author_id=row['author'],
                score=row['score'],
                pub_date=row['pub_date'],
                title_id=row['title_id'],
            )


def import_title():
    with open('static/data/titles.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            Title.objects.create(
                name=row['name'],
                year=row['year'],
                category_id=row['category'],
            )


def import_users():
    with open('static/data/users.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            User.objects.create(
                username=row['username'],
                email=row['email'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                bio=row['bio'],
                role=row['role'],
            )


def import_genre_title():
    with open('static/data/genre_title.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            GenreTitle.objects.create(
                title_id=row['title_id'],
                genre_id=row['genre_id'],
            )


class Command(BaseCommand):
    help = 'Import data from csv file.'

    def handle(self, *args, **options):
        import_users()
        import_category()
        import_genre()
        import_title()
        import_review()
        import_genre_title()
        import_comment()
        self.stdout.write(self.style.SUCCESS('Data imported from csv.'))
