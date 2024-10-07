from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
import os

# Utwórz plik bazy danych SQLite
db_file = "example_database.db"
if os.path.exists(db_file):
    os.remove(db_file)

engine = create_engine(f'sqlite:///{db_file}')

# Deklarujemy bazę ORM
Base = declarative_base()

# Tworzymy trzy tabele - Author, Book i Genre z relacjami jeden do wielu
class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, nullable=False)
    books = relationship('Book', back_populates='author', cascade='all, delete-orphan')

    def __repr__(self):
        return f"Author(id={self.id}, name='{self.name}')"

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, nullable=False)
    books = relationship('Book', back_populates='genre', cascade='all, delete-orphan')

    def __repr__(self):
        return f"Genre(id={self.id}, name='{self.name}')"

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship('Author', back_populates='books')
    genre_id = Column(Integer, ForeignKey('genres.id'))
    genre = relationship('Genre', back_populates='books')

    def __repr__(self):
        return f"Book(id={self.id}, title='{self.title}', author={self.author.name}, genre={self.genre.name})"

# Tworzymy tabele w bazie danych
Base.metadata.create_all(engine)

# Tworzymy sesję ORM
Session = sessionmaker(bind=engine)
session = Session()


# Funkcje CRUD dla dowolnej tabeli
def create_record(table, **kwargs):
    record = table(**kwargs)
    session.add(record)
    try:
        session.commit()
        print(f"Record added successfully.")
    except IntegrityError as e:
        session.rollback()
        print(f"An error occurred: {e}")

def read_table(table_number):
    table = None
    if table_number == 7:
        table = Book
    elif table_number == 8:
        table = Author
    elif table_number == 9:
        table = Genre

    if table:
        data = session.query(table).all()
        for row in data:
            print(row.__dict__)
    else:
        print("Invalid table number.")

def update_record_author(author_id, new_name):
   author = session.query(Author).get(author_id)
   if author:
        author.name = new_name
        try:
            session.commit()
            print(f"Author with ID {author_id} updated successfully.")
        except IntegrityError as e:
            session.rollback()
            print(f"An error occurred: {e}")
   else:
        print(f"Author with ID {author_id} not found.")

def delete_record(table_number, record_id):
    table = None
    if table_number == 7:
        table = Book
    elif table_number == 8:
        table = Author
    elif table_number == 9:
        table = Genre

    if table:
        record = session.query(table).get(record_id)
        if record:
            session.delete(record)
            session.commit()
            print(f"Record deleted successfully.")
        else:
            print(f"Record with ID {record_id} not found.")
    else:
        print("Invalid table number.")

# Funkcja inner join
def inner_join():
    data = session.query(Book, Author).join(Author).all()
    for book, author in data:
        print(f"Book: {book.title}, Author: {author.name}")

# Funkcja left join
def left_join():
    data = session.query(Book, Genre).outerjoin(Genre).all()
    for book, genre in data:
        genre_name = genre.name if genre else 'Unknown'
        print(f"Book: {book.title}, Genre: {genre_name}")

# Potwierdzenie zapisania zmian w bazie danych
def commit_changes():
    try:
        session.commit()
        print("All changes committed successfully.")
    except IntegrityError as e:
        session.rollback()
        print(f"An error occurred: {e}")

# Dodajemy przykładowe dane do tabel
authors_data = [
    {"name": "John Doe"},
    {"name": "Jane Smith"},
    {"name": "Michael Johnson"},
    {"name": "Emily Davis"},
    {"name": "Christopher Brown"},
    {"name": "Amanda Wilson"},
    {"name": "Daniel Taylor"},
    {"name": "Sophia White"},
    {"name": "Ryan Martinez"},
    {"name": "Olivia Garcia"},
]

books_data = [
    {"title": "Python Basics", "author_id": 1, "genre_id": 1},
    {"title": "Data Science Fundamentals", "author_id": 2, "genre_id": 2},
    {"title": "Mystery Novel", "author_id": 3, "genre_id": 3},
    {"title": "Web Development 101", "author_id": 4, "genre_id": 1},
    {"title": "Artificial Intelligence", "author_id": 5, "genre_id": 2},
    {"title": "Romantic Drama", "author_id": 6, "genre_id": 3},
    {"title": "JavaScript Mastery", "author_id": 7, "genre_id": 1},
    {"title": "The Science of Mindfulness", "author_id": 8, "genre_id": 2},
    {"title": "Epic Fantasy", "author_id": 9, "genre_id": 3},
    {"title": "Machine Learning in Practice", "author_id": 10, "genre_id": 1},
    {"title": "Historical Fiction", "author_id": 1, "genre_id": 3},
    {"title": "Game Development Essentials", "author_id": 2, "genre_id": 1},
    {"title": "Thriller: Behind the Scenes", "author_id": 3, "genre_id": 2},
    {"title": "Poetry Anthology", "author_id": 4, "genre_id": 3},
]

genres_data = [
    {"name": "Science Fiction"},
    {"name": "Mystery"},
    {"name": "Romance"},
    {"name": "Programming"},
    {"name": "Self-Help"},
    {"name": "Fantasy"},
    {"name": "Historical"},
    {"name": "Biography"},
    {"name": "Horror"},
    {"name": "Poetry"},
]

for data in authors_data:
    create_record(Author, **data)

for data in books_data:
    create_record(Book, **data)

for data in genres_data:
    create_record(Genre, **data)


# Prosty interfejs konsolowy
def console_interface():
    while True:
        print("\nOptions:")
        print("1. Add Record")
        print("2. View Table")
        print("3. Update Author Name")
        print("4. Delete Record")
        print("5. Inner Join (Book & Author)")
        print("6. Left Join (Book & Genre)")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "0":
            commit_changes()
            break

        elif choice == "1":
          table_number = int(input("Enter table number (7 for Books, 8 for Authors, 9 for Genres): "))
          if table_number in [7, 8, 9]:
                table_class = {7: Book, 8: Author, 9: Genre}[table_number]
                data = {}
                for column in table_class.__table__.columns:
                    data[column.name] = input(f"Enter {column.name}: ")
                create_record(table_class, **data)
          else:
                print("Invalid table number.")

        elif choice == "2":
            table_number = int(input("Enter table number (7 for Books, 8 for Authors, 9 for Genres): "))
            read_table(table_number)

        elif choice == "3":
            author_id = int(input("Enter author ID: "))
            new_name = input("Enter new name: ")
            update_record_author(author_id, new_name)

        elif choice == "4":
            table_number = int(input("Enter table number (7 for Books, 8 for Authors, 9 for Genres): "))
            record_id = int(input("Enter record ID: "))
            delete_record(table_number, record_id)

        elif choice == "5":
            inner_join()

        elif choice == "6":
            left_join()

        else:
            print("Invalid choice. Try again.")

# Uruchomienie interfejsu konsolowego
console_interface()
