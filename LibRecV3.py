import tkinter as tk
from tkinter import ttk, messagebox
import random

class RecommendationLogic:
    def __init__(self, genre_books):
        self.genre_books = genre_books

    def recommend_books(self, selected_genres):
        filtered_books = [(title, author) for genre in selected_genres for title, author in self.genre_books.get(genre, {}).items()]
        if not filtered_books:
            messagebox.showinfo("Recommended Books", "No books match the selected genres.")
        else:
            recommendations = []
            while len(recommendations) < 3:
                book = random.choice(filtered_books)
                if book not in recommendations:
                    recommendations.append(book)
            recommendation_text = "\n".join([f"{title} by {author}" for title, author in recommendations])
            messagebox.showinfo("Recommended Books", recommendation_text)

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

        self.bg_image = tk.PhotoImage(file=r"C:\Users\steve\OneDrive\Desktop\SDEV\LibRecV2\librarybooks.png")
        self.root.geometry(f"{self.bg_image.width()}x{self.bg_image.height()}")

        self.canvas = tk.Canvas(self.root, width=self.bg_image.width(), height=self.bg_image.height())
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        self.canvas.create_text(self.bg_image.width() / 2, self.bg_image.height() - 50, text="BOONE COUNTY LIBRARY", fill="white", font=("Arial", 24, "bold"), anchor="s")

        self.genre_gui = GenreSelectionGUI(self.root)

        self.recommend_button = ttk.Button(self.root, text="Recommend Books", command=self.recommend_books, style="Red.TButton")
        self.recommend_button.place(relx=0.5, rely=0.9, anchor="center")

        self.style = ttk.Style()
        self.style.configure("Dark.TFrame", background="black")
        self.style.configure("White.TLabel", foreground="white", background="black")
        self.style.configure("Red.TCombobox", fieldbackground="red", foreground="black")
        self.style.configure("Red.TButton", foreground="black", background="red", font=('Arial', 10, 'bold'))

    def recommend_books(self):
        selected_genres = self.genre_gui.get_selected_genres()
        logic = RecommendationLogic(self.genre_books)
        logic.recommend_books(selected_genres)

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
