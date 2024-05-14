import tkinter as tk  # Import the tkinter module with alias 'tk' for GUI creation
from tkinter import ttk, messagebox, simpledialog  # Import specific classes from tkinter for GUI elements and dialogs
import random  # Import the random module for generating random recommendations

class RecommendationLogic:
    def __init__(self, genre_books):
        """
        Initialize the RecommendationLogic class.

        Parameters:
        - genre_books (dict): A dictionary mapping genres to books and authors.
        """
        self.genre_books = genre_books
        self.borrowed_books = set()  # Use a set to track borrowed books

    def recommend_books(self, selected_genres):
        """
        Generate and display book recommendations based on selected genres.

        Parameters:
        - selected_genres (list): A list of selected genres (strings).

        Displays a message box with recommended books based on the selected genres.
        """
        available_books = [(title, author) for genre in selected_genres for title, author in self.genre_books.get(genre, {}).items() if title not in self.borrowed_books]
        
        if not available_books:
            # Show a message if no books match selected genres or all are borrowed
            messagebox.showinfo("Recommended Books", "No books match the selected genres or all are currently borrowed.")
        else:
            # Randomly select and display up to 3 book recommendations
            recommendations = random.sample(available_books, min(3, len(available_books)))
            recommendation_text = "\n".join([f"{title} by {author}" for title, author in recommendations])
            messagebox.showinfo("Recommended Books", recommendation_text)

    def borrow_book(self, book_title):
        """
        Borrow a book from the library.

        Parameters:
        - book_title (str): The title of the book to borrow.

        Checks if the book is available and not already borrowed, then updates the borrowed_books set.
        """
        # Check if the book title is in any genre and is not already borrowed
        is_available = any(book_title in self.genre_books[genre] and book_title not in self.borrowed_books for genre in self.genre_books)
        
        if is_available:
            # Add the borrowed book to the set of borrowed books and display a success message
            self.borrowed_books.add(book_title)
            messagebox.showinfo("Book Borrowed", f"{book_title} has been borrowed successfully.")
        else:
            # Display a message indicating that the book is not available
            messagebox.showinfo("Book Not Available", f"{book_title} is not available or already borrowed.")

    def return_book(self, book_title):
        """
        Return a borrowed book to the library.

        Parameters:
        - book_title (str): The title of the book to return.

        Checks if the book is currently borrowed and removes it from the borrowed_books set.
        """
        # Check if the book title is in the borrowed set
        if book_title in self.borrowed_books:
            # Remove the book from the borrowed set and display a return message
            self.borrowed_books.remove(book_title)
            messagebox.showinfo("Book Returned", f"{book_title} has been returned.")
        else:
            # Display a message indicating that the book is not currently borrowed
            messagebox.showinfo("Book Not Borrowed", f"{book_title} is not currently borrowed.")

class GenreSelectionGUI:
    def __init__(self, root):
        """
        Initialize the GenreSelectionGUI class.

        Parameters:
        - root (tk.Tk): The root window of the application.
        """
        self.genre_frame = ttk.Frame(root, style="Dark.TFrame")  # Create a frame for genre selection
        self.genre_frame.place(relx=0.5, rely=0.5, anchor="center")  # Place the frame at the center of the root window

        self.genre_var1 = tk.StringVar()  # Variable to store selected value from genre_menu1
        self.genre_var2 = tk.StringVar()  # Variable to store selected value from genre_menu2
        self.genre_var3 = tk.StringVar()  # Variable to store selected value from genre_menu3

        # Create labels and comboboxes for genre selection within the genre_frame
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
        """
        Retrieve the selected genres from the comboboxes.

        Returns:
        - list: A list of selected genres.
        """
        return [self.genre_var1.get(), self.genre_var2.get(), self.genre_var3.get()]

class BookRecommendationGUI:
    def __init__(self, root, genre_books):
        """
        Initialize the BookRecommendationGUI class.

        Parameters:
        - root (tk.Tk): The root window of the application.
        - genre_books (dict): A dictionary mapping genres to books and authors.
        """
        self.root = root  # Store the root window
        self.genre_books = genre_books  # Store the genre_books dictionary
        self.logic = RecommendationLogic(self.genre_books)  # Create an instance of RecommendationLogic for handling logic

        self.bg_image = tk.PhotoImage(file=r"C:\Users\steve\OneDrive\Desktop\SDEV\librecv5\librarybooks.png")  # Load a background image for the GUI
        self.root.geometry(f"{self.bg_image.width()}x{self.bg_image.height()}")  # Set the window size based on the image dimensions

        # Create a canvas to display the background image and library name text
        self.canvas = tk.Canvas(self.root, width=self.bg_image.width(), height=self.bg_image.height())
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        self.canvas.create_text(self.bg_image.width() / 2, self.bg_image.height() - 50, text="BOONE COUNTY LIBRARY", fill="white", font=("Arial", 24, "bold"), anchor="s")

        self.login()  # Call the login method to authenticate users

    def login(self):
        """
        Display a login screen to authenticate users.
        """
        # Define valid username-password pairs
        valid_users = {
            "user1": "password1",
            "user2": "password2"
        }

        def authenticate():
            """
            Authenticate the user based on entered credentials.
            """
            username = username_entry.get()
            password = password_entry.get()
            if username in valid_users and valid_users[username] == password:
                self.setup_app()  # Proceed to set up the main application if login is successful
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")  # Display an error for invalid credentials

        # Create a login frame with entry fields for username and password
        login_frame = ttk.Frame(self.root, style="Dark.TFrame")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(login_frame, text="Username:", style="White.TLabel").grid(row=0, column=0, padx=5, pady=5)
        username_entry = ttk.Entry(login_frame)  # Entry widget for entering the username
        username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(login_frame, text="Password:", style="White.TLabel").grid(row=1, column=0, padx=5, pady=5)
        password_entry = ttk.Entry(login_frame, show="*")  # Entry widget for entering the password (masked)
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        login_button = ttk.Button(login_frame, text="Login", command=authenticate)  # Button to trigger authentication
        login_button.grid(row=2, columnspan=2, padx=5, pady=5)

    def setup_app(self):
        """
        Set up the main application after successful login.
        """
        self.genre_gui = GenreSelectionGUI(self.root)  # Create an instance of GenreSelectionGUI for genre selection

        # Create buttons for recommending, borrowing, and returning books
        self.recommend_button = ttk.Button(self.root, text="Recommend Books", command=self.recommend_books, style="Red.TButton")
        self.recommend_button.place(relx=0.5, rely=0.9, anchor="center")

        self.borrow_button = ttk.Button(self.root, text="Borrow Book", command=self.borrow_book, style="Red.TButton")
        self.borrow_button.place(relx=0.3, rely=0.9, anchor="center")

        self.return_button = ttk.Button(self.root, text="Return Book", command=self.return_book, style="Red.TButton")
        self.return_button.place(relx=0.7, rely=0.9, anchor="center")

        # Configure styles for various GUI elements
        self.style = ttk.Style()
        self.style.configure("Dark.TFrame", background="black")  # Configure dark theme for frames
        self.style.configure("White.TLabel", foreground="white", background="black")  # Configure white labels on black background
        self.style.configure("Red.TCombobox", fieldbackground="red", foreground="black")  # Configure red comboboxes
        self.style.configure("Red.TButton", foreground="black", background="red", font=('Arial', 10, 'bold'))  # Configure red buttons

    def recommend_books(self):
        """
        Handle the process of recommending books based on selected genres.
        """
        selected_genres = self.genre_gui.get_selected_genres()  # Retrieve selected genres from GenreSelectionGUI
        self.logic.recommend_books(selected_genres)  # Call the recommend_books method from RecommendationLogic instance

    def borrow_book(self):
        """
        Handle the process of borrowing a book.
        """
        book_title = simpledialog.askstring("Borrow Book", "Enter the title of the book you want to borrow:")
        if book_title:
            self.logic.borrow_book(book_title)  # Call the borrow_book method from RecommendationLogic instance

    def return_book(self):
        """
        Handle the process of returning a borrowed book.
        """
        book_title = simpledialog.askstring("Return Book", "Enter the title of the book you want to return:")
        if book_title:
            self.logic.return_book(book_title)  # Call the return_book method from RecommendationLogic instance

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
root = tk.Tk()  # Create the main Tkinter window
root.title("Book Recommendation System")  # Set the title of the window

# Create BookRecommendationGUI object to start the application
app = BookRecommendationGUI(root, genre_books)

# Run the Tkinter event loop to display the GUI and handle user interactions
root.mainloop()