import tkinter as tk
from tkinter import ttk, messagebox
import random

class RecommendationLogic:
    def __init__(self, genre_books):
        self.genre_books = genre_books
        self.borrowed_books = set()

    def recommend_books(self, selected_genres):
        available_books = [(title, author) for genre in selected_genres for title, author in self.genre_books.get(genre, {}).items() if title not in self.borrowed_books]

        if not available_books:
            messagebox.showinfo("Recommended Books", "No books match the selected genres or all are currently borrowed.")
        else:
            recommendations = random.sample(available_books, min(3, len(available_books)))
            recommendation_text = "\n".join([f"{title} by {author}" for title, author in recommendations])
            messagebox.showinfo("Recommended Books", recommendation_text)

    def borrow_book(self, book_title):
        is_available = any(book_title in self.genre_books[genre] and book_title not in self.borrowed_books for genre in self.genre_books)

        if is_available:
            self.borrowed_books.add(book_title)
            messagebox.showinfo("Book Borrowed", f"{book_title} has been borrowed successfully.")
        else:
            messagebox.showinfo("Book Not Available", f"{book_title} is not available or already borrowed.")

    def return_book(self, book_title):
        if book_title in self.borrowed_books:
            self.borrowed_books.remove(book_title)
            messagebox.showinfo("Book Returned", f"{book_title} has been returned.")
        else:
            messagebox.showinfo("Book Not Borrowed", f"{book_title} is not currently borrowed.")

class GenreSelectionGUI:
    def __init__(self, parent, genre_books):
        self.parent = parent
        self.genre_books = genre_books
        self.genre_var1 = tk.StringVar()
        self.genre_var2 = tk.StringVar()
        self.genre_var3 = tk.StringVar()

        self.genre_label1 = ttk.Label(self.parent, text="Genre Preference 1:")
        self.genre_label1.place(relx=0.2, rely=0.4, anchor="center")
        self.genre_menu1 = ttk.Combobox(self.parent, textvariable=self.genre_var1, values=list(genre_books.keys()))
        self.genre_menu1.place(relx=0.5, rely=0.4, anchor="center")

        self.genre_label2 = ttk.Label(self.parent, text="Genre Preference 2:")
        self.genre_label2.place(relx=0.2, rely=0.5, anchor="center")
        self.genre_menu2 = ttk.Combobox(self.parent, textvariable=self.genre_var2, values=list(genre_books.keys()))
        self.genre_menu2.place(relx=0.5, rely=0.5, anchor="center")

        self.genre_label3 = ttk.Label(self.parent, text="Genre Preference 3:")
        self.genre_label3.place(relx=0.2, rely=0.6, anchor="center")
        self.genre_menu3 = ttk.Combobox(self.parent, textvariable=self.genre_var3, values=list(genre_books.keys()))
        self.genre_menu3.place(relx=0.5, rely=0.6, anchor="center")

    def get_selected_genres(self):
        return [self.genre_var1.get(), self.genre_var2.get(), self.genre_var3.get()]

class BookRecommendationGUI:
    def __init__(self, root, genre_books):
        self.root = root
        self.genre_books = genre_books
        self.logic = RecommendationLogic(self.genre_books)

        self.bg_image = tk.PhotoImage(file=r"C:\Users\steve\OneDrive\Desktop\SDEV\librecv5\librarybooks.png")
        self.canvas = tk.Canvas(self.root, width=self.bg_image.width(), height=self.bg_image.height())
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        self.login()

    def login(self):
        valid_users = {
            "user1": "password1",
            "user2": "password2",
            "user3": "password3",
            "user4": "password4",
            "user5": "password5"
        }

        def authenticate():
            username = username_entry.get()
            password = password_entry.get()
            if username in valid_users and valid_users[username] == password:
                login_frame.destroy()
                self.setup_app()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

        login_frame = ttk.Frame(self.canvas)
        login_frame.place(relx=0.5, rely=0.7, anchor="center")

        ttk.Label(login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        username_entry = ttk.Entry(login_frame)
        username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        password_entry = ttk.Entry(login_frame, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        login_button = ttk.Button(login_frame, text="Login", command=authenticate)
        login_button.grid(row=2, columnspan=2, padx=5, pady=5)

    def setup_app(self):
        self.genre_gui = GenreSelectionGUI(self.canvas, self.genre_books)

        recommend_button = ttk.Button(self.canvas, text="Recommend Books", command=self.recommend_books)
        recommend_button.place(relx=0.5, rely=0.9, anchor="center")

        self.root.update_idletasks()
        self.root.minsize(self.bg_image.width(), self.bg_image.height())

    def recommend_books(self):
        selected_genres = self.genre_gui.get_selected_genres()
        self.logic.recommend_books(selected_genres)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Book Recommendation System")

    # Define the genre_books dictionary here or import it from another module
    genre_books = {
        "Classic": {
            "To Kill a Mockingbird": "Harper Lee",
            "1984": "George Orwell",
            "The Catcher in the Rye": "J.D. Salinger",
            "The Great Gatsby": "F. Scott Fitzgerald",
            "Pride and Prejudice": "Jane Austen",
            "A Tale of Two Cities": "Charles Dickens"
        },
        "Fantasy": {
            "Harry Potter and the Sorcerer's Stone": "J.K. Rowling",
            "The Hobbit": "J.R.R. Tolkien",
            "The Chronicles of Narnia": "C.S. Lewis"
        },
        "Mystery": {
            "The Da Vinci Code": "Dan Brown",
            "The Girl with the Dragon Tattoo": "Stieg Larsson",
            "Angels & Demons": "Dan Brown",
            "The Girl on the Train": "Paula Hawkins"
        },
        "Romance": {
            "Gone with the Wind": "Margaret Mitchell",
            "Pride and Prejudice": "Jane Austen",
            "The Notebook": "Nicholas Sparks"
        },
        "Science Fiction": {
            "Dune": "Frank Herbert",
            "The War of the Worlds": "H.G. Wells",
            "Brave New World": "Aldous Huxley",
            "Neuromancer": "William Gibson",
            "The Martian": "Andy Weir",
            "Foundation": "Isaac Asimov",
            "Ender's Game": "Orson Scott Card",
            "The Hitchhiker's Guide to the Galaxy": "Douglas Adams",
            "Snow Crash": "Neal Stephenson",
            "Hyperion": "Dan Simmons"
        },
        "Thriller": {
            "The Girl with the Dragon Tattoo": "Stieg Larsson",
            "The Da Vinci Code": "Dan Brown",
            "The Silence of the Lambs": "Thomas Harris",
            "Gone Girl": "Gillian Flynn",
            "The Girl on the Train": "Paula Hawkins",
            "The Bourne Identity": "Robert Ludlum",
            "The Shining": "Stephen King",
            "Jurassic Park": "Michael Crichton",
            "The Hunt for Red October": "Tom Clancy",
            "Misery": "Stephen King"
        }
    }

    app = BookRecommendationGUI(root, genre_books)

    def toggle_fullscreen(event=None):
        root.attributes("-fullscreen", not root.attributes("-fullscreen"))

    root.bind("<F11>", toggle_fullscreen)
    root.bind("<Escape>", toggle_fullscreen)

    root.mainloop()
