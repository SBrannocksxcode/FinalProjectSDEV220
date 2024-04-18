import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random

class RecommendationLogic:
    def __init__(self, genre_books):
        self.genre_books = genre_books
        self.borrowed_books = set()  # Use a set to track borrowed books

    def recommend_books(self, selected_genres):
        available_books = [(title, author) for genre in selected_genres for title, author in self.genre_books.get(genre, {}).items() if title not in self.borrowed_books]
        
        if not available_books:
            messagebox.showinfo("Recommended Books", "No books match the selected genres or all are currently borrowed.")
        else:
            recommendations = random.sample(available_books, min(3, len(available_books)))
            recommendation_text = "\n".join([f"{title} by {author}" for title, author in recommendations])
            messagebox.showinfo("Recommended Books", recommendation_text)

    def borrow_book(self, book_title):
        # Check if the book title is in any genre and is not already borrowed
        is_available = any(book_title in self.genre_books[genre] and book_title not in self.borrowed_books for genre in self.genre_books)
        
        if is_available:
            self.borrowed_books.add(book_title)
            messagebox.showinfo("Book Borrowed", f"{book_title} has been borrowed successfully.")
        else:
            messagebox.showinfo("Book Not Available", f"{book_title} is not available or already borrowed.")

    def return_book(self, book_title):
        # Check if the book title is in the borrowed set
        if book_title in self.borrowed_books:
            self.borrowed_books.remove(book_title)
            messagebox.showinfo("Book Returned", f"{book_title} has been returned.")
        else:
            messagebox.showinfo("Book Not Borrowed", f"{book_title} is not currently borrowed.")

class GenreSelectionGUI:
    def __init__(self, root):
        self.genre_frame = ttk.Frame(root, style="Dark.TFrame")
        self.genre_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.genre_var1 = tk.StringVar()
        self.genre_var2 = tk.StringVar()
        self.genre_var3 = tk.StringVar()

        self.genre_label1 = ttk.Label(self.genre_frame, text="Genre 1:", style="White.TLabel")
        self.genre_label1.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.genre_menu1 = ttk.Combobox(self.genre_frame, textvariable=self.genre_var1, values=list(genre_books.keys()), style="Red.TCombobox")
        self.genre_menu1.grid(row=0, column=1, padx=5, pady=5)

        self.genre_label2 = ttk.Label(self.genre_frame, text="Genre 2:", style="White.TLabel")
        self.genre_label2.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.genre_menu2 = ttk.Combobox(self.genre_frame, textvariable=self.genre_var2, values=list(genre_books.keys()), style="Red.TCombobox")
        self.genre_menu2.grid(row=1, column=1, padx=5, pady=5)

        self.genre_label3 = ttk.Label(self.genre_frame, text="Genre 3:", style="White.TLabel")
        self.genre_label3.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.genre_menu3 = ttk.Combobox(self.genre_frame, textvariable=self.genre_var3, values=list(genre_books.keys()), style="Red.TCombobox")
        self.genre_menu3.grid(row=2, column=1, padx=5, pady=5)

    def get_selected_genres(self):
        return [self.genre_var1.get(), self.genre_var2.get(), self.genre_var3.get()]

class BookRecommendationGUI:
    def __init__(self, root, genre_books):
        self.root = root
        self.genre_books = genre_books
        self.logic = RecommendationLogic(self.genre_books)  # Create instance of RecommendationLogic

        self.bg_image = tk.PhotoImage(file="C:/Users/steve/OneDrive/Desktop/SDEV/LibRecV2/librarybooks.png")  # Update the path to librarybooks.png
        self.root.geometry(f"{self.bg_image.width()}x{self.bg_image.height()}")

        self.canvas = tk.Canvas(self.root, width=self.bg_image.width(), height=self.bg_image.height())
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        self.canvas.create_text(self.bg_image.width() / 2, self.bg_image.height() - 50, text="BOONE COUNTY LIBRARY", fill="white", font=("Arial", 24, "bold"), anchor="s")

        self.genre_gui = GenreSelectionGUI(self.root)

        self.recommend_button = ttk.Button(self.root, text="Recommend Books", command=self.recommend_books, style="Red.TButton")
        self.recommend_button.place(relx=0.5, rely=0.9, anchor="center")

        self.borrow_button = ttk.Button(self.root, text="Borrow Book", command=self.borrow_book, style="Red.TButton")
        self.borrow_button.place(relx=0.3, rely=0.9, anchor="center")

        self.return_button = ttk.Button(self.root, text="Return Book", command=self.return_book, style="Red.TButton")
        self.return_button.place(relx=0.7, rely=0.9, anchor="center")

        self.style = ttk.Style()
        self.style.configure("Dark.TFrame", background="black")
        self.style.configure("White.TLabel", foreground="white", background="black")
        self.style.configure("Red.TCombobox", fieldbackground="red", foreground="black")
        self.style.configure("Red.TButton", foreground="black", background="red", font=('Arial', 10, 'bold'))

    def recommend_books(self):
        selected_genres = self.genre_gui.get_selected_genres()
        self.logic.recommend_books(selected_genres)  # Call recommend_books from RecommendationLogic instance

    def borrow_book(self):
        book_title = simpledialog.askstring("Borrow Book", "Enter the title of the book you want to borrow:")
        if book_title:
            self.logic.borrow_book(book_title)  # Call borrow_book from RecommendationLogic instance

    def return_book(self):
        book_title = simpledialog.askstring("Return Book", "Enter the title of the book you want to return:")
        if book_title:
            self.logic.return_book(book_title)  # Call return_book from RecommendationLogic instance

# Dictionary mapping genres to books and authors
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

# Create main window
root = tk.Tk()
root.title("Book Recommendation System")

# Create BookRecommendationGUI object
app = BookRecommendationGUI(root, genre_books)

# Run the application
root.mainloop()

