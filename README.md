# Hobi Pazarı

---

## Description
This application is a graphical user interface for a marketplace dedicated to hobbies. It allows users to log in, view, and interact with hobby-related products and services.

## Note: 
The product addition feature is not operational.

If you face problems about using customtkinter try to install it globally

## Installation and Setup

### Prerequisites
- Python 3.x
- PostgreSQL

### Libraries
The application requires the following Python libraries:
- customtkinter
- tkcalendar
- psycopg2

You can install these libraries using pip:
```bash
pip install customtkinter tkcalendar psycopg2
```

## Database Initialization
Before running the application, set up the PostgreSQL database.

1. Install PostgreSQL.
2. Create a database called `hobby_db_1` or whatever name you like.
3. Open a query from PGAdmin4 or using PostgreSQL command propmpt
3. Using the `schema.sql` file, initialize tables, functions, triggers, sequences etc.
4. Finally, using the `data.sql` file, add appropriate data to the database.
5. Now you're ready to deploy your project.

## Running the Application
To run the application, navigate to the project directory and run the `main.py` file:
```bash
python main.py
```

## Usage
After starting the application, a login screen will appear. Create a new user or enter your user credentials to access the marketplace. 


## Application Overview
Here is some explanations about `tkinter`, `customtkinter` and `psycopg2`. Which is required to understand this project and to benefit from it.

### tkinter
- **What it is**: `tkinter` is the standard GUI (Graphical User Interface) toolkit for Python. It is an interface to the Tk GUI toolkit.
- **Use in Project**: `tkinter` not actively used in this project. It is base of `customtkinter` library.

### customtkinter
- **What it is**: `customtkinter` is an extension of the standard `tkinter` library. It provides a more modern and customizable look for the Tkinter widgets.
- **Use in Project**: `customtkinter` is used to enhance the visual appeal of our project. Because with using it there is no need to waste time to make it look beautiful.

### psycopg2
- **What it is**: `psycopg2` is a PostgreSQL database adapter for the Python programming language. It is a mature and fully-featured database driver.
- **Use in Project**: `psycopg2` is used to connect Python applications to a PostgreSQL database. It allows executing SQL queries, handling database operations, and managing database connections in Python.

---

## Overview of Code

#### Database Connection
- **Connection Establishment**: The application uses `psycopg2` to establish a connection to a PostgreSQL database.
  ```python
  conn = psycopg2.connect(host="localhost", port="5432", database="hobby_db_1", user="postgres", password="123")
  cur = conn.cursor()
  ```
  This code creates a connection to a local PostgreSQL database named `hobby_db_1` using the specified host, port, user credentials, and then creates a cursor object for executing queries.

#### Global Variables
- **User and Product Information**: The application defines global variables to store user and product information.
  These variables (`global_username`, `global_userid`, `global_productname`) are used throughout the application to manage and track the current user's information and selected product details.

#### CustomTkinter Configuration
- **DPI Awareness and Widget Scaling**: The application configures `customtkinter` settings for better UI scaling and display.
  ```python
  ctk.deactivate_automatic_dpi_awareness()
  ctk.set_widget_scaling(1.3)
  ```
  These settings ensure that the application's graphical interface scales appropriately across different screen resolutions and DPI settings.


### Main Application Class
- **Class Definition and Initialization**: `MainApplication` is the primary class of the application, extending `ctk.CTk`.
  ```python
  class MainApplication(ctk.CTk):
      def __init__(self, *args, **kwargs):
          ...
  ```
  It initializes the main window of the application, setting the title to "Hobi Pazarı" and configuring the window size and position.

- **Window Centering Method**: A method `center_window` calculates the appropriate position to center the application window on the screen.

- **Navigation Between Screens**: The application has methods like `show_homepage` and `logout` to handle navigation between different screens (e.g., from the login screen to the homepage and vice versa).

### Homepage Class Overview

The `Homepage` class, derived from `customtkinter.CTkFrame`, represents the main user interface after successful login.

#### Key Functionalities

- **Initialization**: The class constructor initializes various UI elements including buttons, frames, and a scrollable container for products.
- **Profile and Logout**: Displays the current user's username and provides a logout button.
- **Navigation Buttons**: Includes buttons for accessing the shopping cart (`Sepet`), purchased items (`Satın Alınanlar`), and user profile update.
- **Search Functionality**: Allows users to search for products using a search bar. The `search_ref` method refreshes the product display based on the search query.
- **Product Display**: Uses a scrollable frame to display products. Products are added dynamically from the database based on the search query or default criteria.
- **Shopping Cart Management**: Functions to handle the addition of products to the shopping cart and updating the cart display.
- **Additional Windows**: Methods to open additional windows for the shopping cart, purchased items, and user profile update.

#### Database Interaction

- **Product Search**: The `search` method executes a database query to fetch products based on the name or default criteria.
- **Dynamic Content Update**: The UI dynamically updates to display products and information fetched from the database.

### LoginScreen Class Overview

The `LoginScreen` class, extending `customtkinter.CTkFrame`, is responsible for handling the user login functionality of the application.

#### Key Functionalities

- **UI Elements**: The class initializes the login screen with username and password entry fields, login and register buttons, and a label for displaying error messages.
- **Event Handling**:
  - **Login Process**: The `on_login_click` method handles the login logic. It retrieves the username and password from the entry fields, checks credentials against the database, and either shows an error or proceeds to the main application upon successful authentication.
  - **Registration Process**: The `on_register_click` method opens a registration window where new users can sign up.

#### Database Interaction

- **Credential Verification**: Uses a database query to verify the entered username and password. This process is crucial for authenticating users.

#### Global Variables

- **User Information Storage**: Upon successful login, the user's username and user ID are stored in global variables (`global_username`, `global_userid`) for use throughout the application.


#### Other classes are similar to these. You can deduce the functionality of the other classes by analogy. 

## Contributing
Contributions to this project are welcome. Please fork the repository, make your changes, and submit a pull request.

---

For any questions or issues, please open an issue in the project's GitHub repository.
