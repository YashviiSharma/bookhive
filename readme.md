# Library Management System

## Overview
The **Library Management System** is a web-based application designed to help librarians efficiently manage books and members. The system provides functionalities for book issuance, member management, and book tracking, ensuring smooth operation of a library.

## Features

### 1. Member Management
- Add, edit, delete, and list members.
- Generate ID cards for members.
- Fetch member details dynamically.
- Manage outstanding fines and overdue books.

### 2. Book Management
- Add, edit, delete, and list books.
- Import books from the **Frappe Library API**.
- Organize books by categories such as *Fiction, Sci-Fi, Horror*, etc.
- Store book details including *title, author, ISBN, publisher, page count, and rating*.
- Update book availability dynamically based on transactions.

### 3. Book Issuing System
- Issue books to members.
- Set due dates and calculate fines automatically.
- Prevent book issuance if a member's fine exceeds **₹500**.
- Fetch book details dynamically by **ISBN**.
- Track issued books for each member.

### 4. Transactions & Reporting
- View issued books per member.
- Calculate overdue fines dynamically (**Fine: ₹5 per day for late returns**).
- Generate and download printable ID cards with member details and issued books.
- Track rent fees per book issued.

## Tech Stack

### Backend
- **Flask (Python)** - Lightweight web framework.
- **PostgreSQL** - Database management using **Peewee ORM**.

### Frontend
- **HTML, CSS (Bootstrap)** - Responsive UI.
- **JavaScript** - For additional UI functionality.

### Additional Features
- **PDF Generation**: ID cards are generated using *WeasyPrint*.
- **External API Integration**: Books can be imported from the *Frappe Library API*.

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YashviiSharma/bookhive
cd library-management-system
```

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Initialize Database
Run the database initialization script (if applicable).

### 4. Run the Application
flask run

The application will run on **http://127.0.0.1:5000/**

## API Endpoints
![API Endpoints Screenshot](https://github.com/user-attachments/assets/66aaf1af-787f-445b-8784-26af496d03ed)

## Future Enhancements
- **Email Notifications** for due date reminders.
- **Admin Panel** with user authentication.

## Contributors
- **Yashvi and Ritika**
- **Korecent Solutions Pvt Ltd**


Screenshots
1. Home Page

    Displays total books and members in the system.In the below image we can see the navbar which consist of mostly all the operations this application do
    ![home1](https://github.com/user-attachments/assets/d500a585-afdc-44ac-b477-ea7ff6498fa9)
   In this section we can see the total members currently in our system , total books , and the monthly growth is currently hardcoded(will improvise later)
    ![home2](https://github.com/user-attachments/assets/85176765-970f-44e0-8959-757f9b29b5bc)
   Here we provide the flexiblity to the librarian to alter the plan(monthly and yearly) for student
   and below that there is a contact section which can be used by librarians if they face any issue
    ![home3](https://github.com/user-attachments/assets/fcdf87de-a4dc-40e8-b5f8-5d5531684e6b)

3. Books Section

    displays books according to genre - we can search genere
   ![book](https://github.com/user-attachments/assets/41b1e6d2-b384-4003-ae8a-694eb6a9edf3)
   ![searchbook](https://github.com/user-attachments/assets/e00536fa-6116-4059-b5e3-5f03762c8f33)
   
   After clicking on any genre we can see all the books available in that genre
   ![image](https://github.com/user-attachments/assets/edfc98d6-c2ef-4c52-9384-42a927f10070)
   
   we can search by title or author
   ![searchbyAuthor](https://github.com/user-attachments/assets/5554bbf7-702b-42f6-acc3-1ee1b6411511)
   
   Also we can apply filter to books based on ratings
   ![filterbyRating](https://github.com/user-attachments/assets/4f411655-090a-43cd-92e5-d1a3188e106b)


4. Add a new Book
       Librarians can add books with details like title, author, ISBN, etc.
       ![addbook](https://github.com/user-attachments/assets/caac34e1-0040-4250-8eb4-1b58328c49ff)

       
       on addition we can see the booklist , that will have title of book , quantity of that book and some actions like edit and delete
      ![booklist](https://github.com/user-attachments/assets/6c9c32bc-3fbb-4800-98e9-969a6a12a713)


       edit functionality
  ![image](https://github.com/user-attachments/assets/72491e2c-6293-44ac-b530-39e58784f241)

       updated quantity in book list
   ![image](https://github.com/user-attachments/assets/d41755c3-c038-458a-a174-b6dd251bd43d)


4. Download CSV
    In the bottom there is Download CSV button , which downloads a CSV file with all the book details(title , author , available copies)
    ![image](https://github.com/user-attachments/assets/c442624f-91e7-4513-8cd3-48fafd79c83f)
    downloaded CSV file-
    ![image](https://github.com/user-attachments/assets/b066c970-9af9-43f6-b198-08accac585af)
 

5.Importing a book
    we can import a book also by specifying anything like - title of book , author , isbn etc
    ![image](https://github.com/user-attachments/assets/7bd00302-9350-4839-800b-9b16f5e0b463)
    book list
    ![image](https://github.com/user-attachments/assets/8a45050e-bb42-48e9-abe1-8be2bbe1b5ba)
 
6. Add a New Member

    Allows librarians to register new members.
    ![addMember](https://github.com/user-attachments/assets/a46d0821-d9e2-4d57-8f32-b103c5764116)

      

7. List of Members

   Shows all registered members.
    
   Member list - comprise of member id, name , email , phone number and some actions (CRUD Operations) like edit and delete
   ![memberlist](https://github.com/user-attachments/assets/bcbe7725-ff1e-4133-81a9-043f1e8fde83)



8. Issue a Book

    Books can be issued to members with a due date.
    We have a form for issuing the book where the member details are automatically fetched by there id
    and the librarian will give id of book which will fetcch book name
   ![issuebook](https://github.com/user-attachments/assets/b3ccd4b3-bcb8-40fd-a03b-e3d95d358796)

   after successfully issuing the book , the book issued successfully page with member details and a button to generate id will be visible
   ![issueSuccess](https://github.com/user-attachments/assets/a4ad1ffb-374e-4a78-99a7-ca6848867579)


9. Member ID Card

    Printable ID card generation feature.
   As the user librarian clicks on generate id card , all details of user , with rental fee and book details will be visible
   ![generateId](https://github.com/user-attachments/assets/abd62129-51a8-4694-8f7d-60db265b507c)

   if the due date is already passed then a fine of 5rs will be charged per day
   ![image](https://github.com/user-attachments/assets/41ff795d-29ba-4ced-b942-7103afbe13fc)

10. Return book
    Issued book shows all the books which are issued by library member , in right side we have return button which basically returns the book , which increase the       count of available books

   ![image](https://github.com/user-attachments/assets/aa674710-8d30-42ca-ae74-38fdc756ef6a)



