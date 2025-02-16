Library Management System

This is a web-based Library Management System that allows librarians to manage books and members efficiently. The system enables book issuance, member management, and book tracking.


Member Management:

    Add, edit, delete, and list members.
    Generate ID cards for members.

Book Management:

    Add, edit, delete, and list books.
    Import books from an external API.

Book Issuing System:

    Issue books to members.
    Set due dates and calculate fines automatically.
    Prevent issuance if fines exceed ₹500.

Transaction & Reporting:

    View issued books per member.
    Calculate overdue fines dynamically.
    Generate printable ID cards.

Tech Stack

    Backend: Flask (Python)
    Database: SQLite (using Peewee ORM)
    Frontend: HTML, CSS (Bootstrap), JavaScript (Fetch API)
    PDF Generation: WeasyPrint
    External API Integration: Frappe Library API

Screenshots
1️⃣ Home Page

    Displays total books and members in the system.
![home1](https://github.com/user-attachments/assets/d500a585-afdc-44ac-b477-ea7ff6498fa9)
![home2](https://github.com/user-attachments/assets/85176765-970f-44e0-8959-757f9b29b5bc)
![home3](https://github.com/user-attachments/assets/fcdf87de-a4dc-40e8-b5f8-5d5531684e6b)


2️⃣ Add a New Member

    Allows librarians to register new members.

3️⃣ List of Members

    Shows all registered members.

4️⃣ Add a New Book

    Librarians can add books with details like title, author, ISBN, etc.

5️⃣ Issue a Book

    Books can be issued to members with a due date.

6️⃣ Member ID Card

    Printable ID card generation feature.
