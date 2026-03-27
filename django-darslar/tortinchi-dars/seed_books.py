import random
from datetime import date
from books.models import Category, Author, Book, BookCategories


category_names = [
    "Programming",
    "Artificial Intelligence",
    "Startup",
    "Business",
    "Psychology",
    "Finance",
    "Science",
    "History",
    "Productivity",
    "Software Engineering",
    "Data Science",
    "Machine Learning",
]

categories = {
    name: Category.objects.get_or_create(name=name)[0]
    for name in category_names
}

authors_data = [
    ("Robert C. Martin", 1952),
    ("Martin Fowler", 1963),
    ("Eric Evans", 1965),
    ("Kent Beck", 1961),
    ("Donald Knuth", 1938),
    ("Andrew Hunt", 1964),
    ("David Thomas", 1956),
    ("Steve McConnell", 1962),
    ("Joshua Bloch", 1961),
    ("Brian Kernighan", 1942),
    ("Dennis Ritchie", 1941),
    ("Bjarne Stroustrup", 1950),
    ("Guido van Rossum", 1956),
    ("Mark Lutz", 1956),
    ("Luciano Ramalho", 1969),
    ("Peter Norvig", 1956),
    ("Stuart Russell", 1962),
    ("Ian Goodfellow", 1985),
    ("Yoshua Bengio", 1964),
    ("Geoffrey Hinton", 1947),
    ("Andrew Ng", 1976),
    ("Sebastian Raschka", 1989),
    ("Aurélien Géron", 1972),
    ("Thomas H. Cormen", 1956),
    ("Robert Sedgewick", 1946),
    ("Timothy Ferriss", 1977),
    ("Cal Newport", 1982),
    ("James Clear", 1986),
    ("Daniel Kahneman", 1934),
    ("Nassim Nicholas Taleb", 1960),
    ("Eric Ries", 1978),
    ("Steve Blank", 1953),
    ("Peter Thiel", 1967),
    ("Ben Horowitz", 1966),
    ("Walter Isaacson", 1952),
    ("Erich Gamma", 1961),
    ("David Beazley", 1963),
]

for name, year in authors_data:
    Author.objects.get_or_create(
        name=name,
        defaults={
            "dob": date(year, 1, 1),
            "bio": f"{name} is a well known author in tech/business field",
        },
    )

books_data = [
    ("Clean Code", "Robert C. Martin", 2008, ["Programming", "Software Engineering"]),
    ("Clean Architecture", "Robert C. Martin", 2017, ["Software Engineering"]),
    ("The Pragmatic Programmer", "Andrew Hunt", 1999, ["Programming"]),
    ("Refactoring", "Martin Fowler", 1999, ["Software Engineering"]),
    ("Domain-Driven Design", "Eric Evans", 2003, ["Software Engineering"]),
    ("Test Driven Development", "Kent Beck", 2002, ["Programming"]),
    ("Introduction to Algorithms", "Thomas H. Cormen", 2009, ["Programming"]),
    ("Design Patterns", "Erich Gamma", 1994, ["Software Engineering"]),
    ("Artificial Intelligence: A Modern Approach", "Stuart Russell", 2010, ["Artificial Intelligence"]),
    ("Deep Learning", "Ian Goodfellow", 2016, ["Machine Learning", "Artificial Intelligence"]),
    ("Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow", "Aurélien Géron", 2019, ["Machine Learning", "Data Science"]),
    ("Python Cookbook", "David Beazley", 2013, ["Programming"]),
    ("Fluent Python", "Luciano Ramalho", 2015, ["Programming"]),
    ("Effective Java", "Joshua Bloch", 2018, ["Programming"]),
    ("The Lean Startup", "Eric Ries", 2011, ["Startup", "Business"]),
    ("Zero to One", "Peter Thiel", 2014, ["Startup", "Business"]),
    ("The Hard Thing About Hard Things", "Ben Horowitz", 2014, ["Startup", "Business"]),
    ("Atomic Habits", "James Clear", 2018, ["Productivity", "Psychology"]),
    ("Deep Work", "Cal Newport", 2016, ["Productivity"]),
    ("Thinking, Fast and Slow", "Daniel Kahneman", 2011, ["Psychology"]),
    ("The Black Swan", "Nassim Nicholas Taleb", 2007, ["Finance", "Psychology"]),
    ("The 4-Hour Workweek", "Timothy Ferriss", 2007, ["Business", "Productivity"]),
    ("Working Effectively with Legacy Code", "Michael Feathers", 2004, ["Software Engineering"]),
    ("Patterns of Enterprise Application Architecture", "Martin Fowler", 2002, ["Software Engineering"]),
    ("Code Complete", "Steve McConnell", 2004, ["Programming", "Software Engineering"]),
]

# books_data ichidagi yo'q authorlarni ham avtomatik yaratadi
for _, author_name, _, _ in books_data:
    Author.objects.get_or_create(
        name=author_name,
        defaults={
            "dob": date(1970, 1, 1),
            "bio": f"{author_name} is a known author.",
        },
    )

expanded_books = []
while len(expanded_books) < 100:
    expanded_books.extend(books_data)
expanded_books = expanded_books[:100]

created_count = 0

for index, (title, author_name, year, cat_list) in enumerate(expanded_books, start=1):
    author = Author.objects.get(name=author_name)

    unique_title = f"{title} #{index}"

    book, created = Book.objects.get_or_create(
        title=unique_title,
        defaults={
            "description": f"{title} by {author_name}",
            "author": author,
            "published_year": year,
            "isbn": str(9780000000000 + index),
            "price": random.randint(15, 100),
        },
    )

    if created:
        created_count += 1

    for cat in cat_list:
        BookCategories.objects.get_or_create(
            book=book,
            category=categories[cat],
        )

print(f"DONE: {created_count} books created")
