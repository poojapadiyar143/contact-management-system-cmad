Contact Management System
A graphical Contact Management System built with Python's tkinter library. It allows users to add, edit, delete, search, and filter contacts efficiently using a GUI. Contacts are stored in a linked list and saved to categorized files for persistence.

 Features
 Contact Categories: Supports types like college, family, colleague, friend, neighbour, and relatives.

 CRUD Operations: Create, read, update, and delete contact records.

 Search & Filter: Search by name and filter by contact type.

 Persistent Storage: Saves contacts in JSON format within categorized .txt files under the contacts/ folder.

 Linked List Backend: Manages contacts in a sorted (alphabetical) linked list for efficient operations.

 User-Friendly GUI: Built with tkinter using custom styles for an intuitive interface.

 Technologies Used
Python 3.x

Tkinter (GUI library)

JSON (for file storage)

OOP (Object-Oriented Programming)

Linked List Data Structure

Project Structure
bash
Copy
Edit
├── contact list.py      # Main application file with all logic and GUI
├── contacts/            # Directory where contact files are stored
│   ├── college.txt
│   ├── family.txt
│   ├── ...
 GUI Preview
The GUI features:

Left panel: Add/Edit form + Search & Filter tools

Right panel: Treeview listing all contacts

Bottom: Status bar for messages

 How to Run
Ensure you have Python 3 installed.

Clone the repository or download the .py file:

bash
Copy
Edit
git clone https://github.com/yourusername/contact-management-system.git
cd contact-management-system
Run the app:

bash
Copy
Edit
python "contact list.py"
Usage
Required fields: Name, Phone Number, Contact Type

Phone numbers must be exactly 10 digits.

Email must include the @ symbol if provided.

Contacts are saved in separate files based on their type.

Double-click a contact to load it into the edit form.

File Saving Logic
Each contact is saved in a JSON line format in a file named:

php-template
Copy
Edit
contacts/<contact_type>.txt
Example entry in contacts/friend.txt:

json
Copy
Edit
{"name": "Alice", "phone": "9876543210", "email": "alice@example.com", "type": "friend"}
Developer Info
Designed with modular, object-oriented structure.

Uses ContactNode and ContactLinkedList classes for backend logic.

GUI is encapsulated in the ContactManager class.

