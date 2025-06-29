import tkinter as tk
from tkinter import ttk, messagebox, font
import os
import json
from typing import Optional, Dict, List

class ContactNode:
    """Node for linked list implementation"""
    def __init__(self, name: str, phone: str, email: str, contact_type: str):
        self.name = name
        self.phone = phone
        self.email = email
        self.contact_type = contact_type
        self.next: Optional['ContactNode'] = None

class ContactLinkedList:
    """Linked list to store contacts in alphabetical order"""
    def __init__(self):
        self.head: Optional[ContactNode] = None
    
    def insert(self, name: str, phone: str, email: str, contact_type: str):
        """Insert contact in alphabetical order"""
        new_node = ContactNode(name, phone, email, contact_type)
        
        if not self.head or self.head.name.lower() > name.lower():
            new_node.next = self.head
            self.head = new_node
            return
        
        current = self.head
        while current.next and current.next.name.lower() < name.lower():
            current = current.next
        
        new_node.next = current.next
        current.next = new_node
    
    def delete(self, name: str, phone: str) -> bool:
        """Delete contact by name and phone"""
        if not self.head:
            return False
        
        # Convert to strings and strip for comparison
        search_name = str(name).strip()
        search_phone = str(phone).strip()
        
        # Check head node
        if (str(self.head.name).strip() == search_name and 
            str(self.head.phone).strip() == search_phone):
            self.head = self.head.next
            return True
        
        current = self.head
        while current.next:
            if (str(current.next.name).strip() == search_name and 
                str(current.next.phone).strip() == search_phone):
                current.next = current.next.next
                return True
            current = current.next
        
        return False
    
    def find(self, name: str, phone: str) -> Optional[ContactNode]:
        """Find contact by name and phone"""
        current = self.head
        while current:
            # Convert to strings and strip for comparison
            if (str(current.name).strip() == str(name).strip() and 
                str(current.phone).strip() == str(phone).strip()):
                return current
            current = current.next
        return None
    
    def get_all_contacts(self) -> List[ContactNode]:
        """Get all contacts as a list"""
        contacts = []
        current = self.head
        while current:
            contacts.append(current)
            current = current.next
        return contacts

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        # Contact types
        self.contact_types = ['college', 'family', 'colleague', 'friend', 'neighbour', 'relatives']
        
        # Linked list for contacts
        self.contact_list = ContactLinkedList()
        
        # Create directories if they don't exist
        self.create_directories()
        
        # Load existing contacts
        self.load_contacts()
        
        # Setup GUI
        self.setup_gui()
        
        # Load contacts into treeview
        self.refresh_contact_display()
    
    def create_directories(self):
        """Create directories for storing contact files"""
        if not os.path.exists('contacts'):
            os.makedirs('contacts')
    
    def setup_gui(self):
        """Setup the main GUI"""
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel', font=('Arial', 20, 'bold'), background='#2c3e50', foreground='#ecf0f1')
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), background='#34495e', foreground='#ecf0f1')
        style.configure('Custom.TFrame', background='#34495e')
        style.configure('Custom.TEntry', fieldbackground='#ecf0f1', font=('Arial', 10))
        style.configure('Custom.TCombobox', fieldbackground='#ecf0f1', font=('Arial', 10))
        style.configure('Custom.TButton', font=('Arial', 10, 'bold'))
        
        # Main title
        title_label = ttk.Label(self.root, text="📞 Contact Management System", style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Main container
        main_frame = ttk.Frame(self.root, style='Custom.TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel for input
        left_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # Input section
        input_frame = ttk.LabelFrame(left_frame, text="Add/Edit Contact", padding=20)
        input_frame.pack(fill='x', pady=(0, 10))
        
        # Name field
        ttk.Label(input_frame, text="Name *", style='Heading.TLabel').pack(anchor='w')
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(input_frame, textvariable=self.name_var, style='Custom.TEntry', width=25)
        self.name_entry.pack(fill='x', pady=(5, 10))
        
        # Phone field
        ttk.Label(input_frame, text="Phone Number *", style='Heading.TLabel').pack(anchor='w')
        self.phone_var = tk.StringVar()
        self.phone_entry = ttk.Entry(input_frame, textvariable=self.phone_var, style='Custom.TEntry', width=25)
        self.phone_entry.pack(fill='x', pady=(5, 10))
        
        # Email field
        ttk.Label(input_frame, text="Email", style='Heading.TLabel').pack(anchor='w')
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(input_frame, textvariable=self.email_var, style='Custom.TEntry', width=25)
        self.email_entry.pack(fill='x', pady=(5, 10))
        
        # Contact type field
        ttk.Label(input_frame, text="Contact Type *", style='Heading.TLabel').pack(anchor='w')
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(input_frame, textvariable=self.type_var, 
                                      values=self.contact_types, style='Custom.TCombobox', width=22)
        self.type_combo.pack(fill='x', pady=(5, 10))
        self.type_combo.state(['readonly'])
        
        # Buttons frame
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        # Add button
        self.add_btn = ttk.Button(button_frame, text="Add Contact", 
                                 command=self.add_contact, style='Custom.TButton')
        self.add_btn.pack(side='left', padx=(0, 5))
        
        # Update button
        self.update_btn = ttk.Button(button_frame, text="Update Contact", 
                                    command=self.update_contact, style='Custom.TButton')
        self.update_btn.pack(side='left', padx=5)
        
        # Clear button
        self.clear_btn = ttk.Button(button_frame, text="Clear", 
                                   command=self.clear_fields, style='Custom.TButton')
        self.clear_btn.pack(side='left', padx=5)
        
        # Search section
        search_frame = ttk.LabelFrame(left_frame, text="Search Contacts", padding=20)
        search_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(search_frame, text="Search by Name", style='Heading.TLabel').pack(anchor='w')
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, style='Custom.TEntry', width=25)
        self.search_entry.pack(fill='x', pady=(5, 10))
        self.search_entry.bind('<KeyRelease>', self.search_contacts)
        
        # Filter by type
        ttk.Label(search_frame, text="Filter by Type", style='Heading.TLabel').pack(anchor='w')
        self.filter_var = tk.StringVar()
        filter_values = ['All'] + self.contact_types
        self.filter_combo = ttk.Combobox(search_frame, textvariable=self.filter_var, 
                                        values=filter_values, style='Custom.TCombobox', width=22)
        self.filter_combo.pack(fill='x', pady=(5, 0))
        self.filter_combo.set('All')
        self.filter_combo.bind('<<ComboboxSelected>>', self.filter_contacts)
        
        # Right panel for contact list
        right_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Contact list
        list_frame = ttk.LabelFrame(right_frame, text="Contact List", padding=10)
        list_frame.pack(fill='both', expand=True)
        
        # Treeview for contacts
        columns = ('Name', 'Phone', 'Email', 'Type')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        
        # Define headings
        for col in columns:
            self.tree.heading(col, text=col, anchor='w')
            self.tree.column(col, width=120, anchor='w')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind double-click to edit
        self.tree.bind('<Double-1>', self.on_item_select)
        
        # Delete button
        delete_frame = ttk.Frame(right_frame)
        delete_frame.pack(fill='x', pady=(10, 0))
        
        self.delete_btn = ttk.Button(delete_frame, text="Delete Selected", 
                                    command=self.delete_contact, style='Custom.TButton')
        self.delete_btn.pack(side='right')
        
        # Debug button (for testing)
        self.debug_btn = ttk.Button(delete_frame, text="Debug Files", 
                                   command=self.debug_files, style='Custom.TButton')
        self.debug_btn.pack(side='right', padx=(0, 10))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief='sunken', anchor='w', background='#34495e', foreground='#ecf0f1')
        status_bar.pack(side='bottom', fill='x')
    
    def validate_input(self) -> bool:
        """Validate input fields"""
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        contact_type = self.type_var.get().strip()
        
        # Check required fields
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return False
        
        if not phone:
            messagebox.showerror("Error", "Phone number is required!")
            return False
        
        if not contact_type:
            messagebox.showerror("Error", "Contact type is required!")
            return False
        
        # Validate phone number
        if len(phone) != 10 or not phone.isdigit():
            messagebox.showerror("Error", "Phone number must be exactly 10 digits!")
            return False
        
        # Validate email if provided
        if email and '@' not in email:
            messagebox.showerror("Error", "Email must contain '@' symbol!")
            return False
        
        return True
    
    def add_contact(self):
        """Add a new contact"""
        if not self.validate_input():
            return
        
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        contact_type = self.type_var.get().strip()
        
        # Check if contact already exists
        if self.contact_list.find(name, phone):
            messagebox.showerror("Error", "Contact with this name and phone number already exists!")
            return
        
        # Add to linked list
        self.contact_list.insert(name, phone, email, contact_type)
        
        # Save to file
        self.save_contact_to_file(name, phone, email, contact_type)
        
        # Refresh display
        self.refresh_contact_display()
        
        # Clear fields
        self.clear_fields()
        
        self.status_var.set(f"Contact '{name}' added successfully!")
    
    def update_contact(self):
        """Update selected contact"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a contact to update!")
            return
        
        if not self.validate_input():
            return
        
        # Get old contact data
        item = self.tree.item(selected[0])
        old_name, old_phone = item['values'][0], item['values'][1]
        old_type = item['values'][3]
        
        # Get new data
        new_name = self.name_var.get().strip()
        new_phone = self.phone_var.get().strip()
        new_email = self.email_var.get().strip()
        new_type = self.type_var.get().strip()
        
        # Delete old contact
        self.contact_list.delete(old_name, old_phone)
        self.delete_contact_from_file(old_name, old_phone, old_type)
        
        # Add updated contact
        self.contact_list.insert(new_name, new_phone, new_email, new_type)
        self.save_contact_to_file(new_name, new_phone, new_email, new_type)
        
        # Refresh display
        self.refresh_contact_display()
        
        # Clear fields
        self.clear_fields()
        
        self.status_var.set(f"Contact updated successfully!")
    
    def delete_contact(self):
        """Delete selected contact"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a contact to delete!")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this contact?"):
            item = self.tree.item(selected[0])
            name, phone, contact_type = item['values'][0], item['values'][1], item['values'][3]
            
            print(f"Attempting to delete: {name}, {phone}, {contact_type}")  # Debug
            
            # Delete from linked list
            deleted_from_list = self.contact_list.delete(name, phone)
            print(f"Deleted from linked list: {deleted_from_list}")  # Debug
            
            # Delete from file
            deleted_from_file = self.delete_contact_from_file(name, phone, contact_type)
            print(f"Deleted from file: {deleted_from_file}")  # Debug
            
            # Refresh display
            self.refresh_contact_display()
            
            if deleted_from_file:
                self.status_var.set(f"Contact '{name}' deleted successfully!")
            else:
                self.status_var.set(f"Contact '{name}' deleted from display but may still exist in file!")
    
    def on_item_select(self, event):
        """Handle item selection for editing"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            
            # Fill form with selected contact data
            self.name_var.set(values[0])
            self.phone_var.set(values[1])
            self.email_var.set(values[2])
            self.type_var.set(values[3])
    
    def clear_fields(self):
        """Clear all input fields"""
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.type_var.set("")
    
    def save_contact_to_file(self, name: str, phone: str, email: str, contact_type: str):
        """Save contact to appropriate file"""
        filename = f"contacts/{contact_type}.txt"
        
        # Read existing contacts
        contacts = []
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    for line in f:
                        if line.strip():
                            try:
                                contacts.append(json.loads(line.strip()))
                            except json.JSONDecodeError:
                                continue
            except Exception as e:
                print(f"Error reading file: {e}")
        
        # Add new contact
        contact_data = {
            'name': name,
            'phone': phone,
            'email': email,
            'type': contact_type
        }
        contacts.append(contact_data)
        
        # Sort contacts by name (case-insensitive)
        contacts.sort(key=lambda x: x['name'].lower())
        
        # Write back to file
        try:
            with open(filename, 'w') as f:
                for contact in contacts:
                    f.write(json.dumps(contact) + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")
            messagebox.showerror("Error", f"Could not save contact to file: {e}")
    
    def delete_contact_from_file(self, name: str, phone: str, contact_type: str):
        """Delete contact from file"""
        filename = f"contacts/{contact_type}.txt"
        print(f"Looking for file: {filename}")  # Debug
        
        if not os.path.exists(filename):
            print(f"File {filename} does not exist!")  # Debug
            return False
        
        # Read existing contacts
        contacts = []
        found = False
        try:
            with open(filename, 'r') as f:
                content = f.read()
                print(f"File content before deletion:\n{content}")  # Debug
                
            # Re-read the file line by line
            with open(filename, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    if line.strip():
                        try:
                            contact = json.loads(line.strip())
                            print(f"Line {line_num}: {contact}")  # Debug
                            
                            # Check if this is the contact to delete
                            # Convert both to strings and strip whitespace for comparison
                            contact_name = str(contact['name']).strip()
                            contact_phone = str(contact['phone']).strip()
                            search_name = str(name).strip()
                            search_phone = str(phone).strip()
                            
                            print(f"Comparing: '{contact_name}' == '{search_name}' and '{contact_phone}' == '{search_phone}'")  # Debug
                            
                            if contact_name == search_name and contact_phone == search_phone:
                                print(f"Found contact to delete: {contact}")  # Debug
                                found = True
                            else:
                                contacts.append(contact)
                        except json.JSONDecodeError as e:
                            print(f"JSON decode error on line {line_num}: {e}")  # Debug
                            continue
            
            print(f"Contact found for deletion: {found}")  # Debug
            print(f"Remaining contacts: {contacts}")  # Debug
            
            # Write back to file only if contact was found
            if found:
                with open(filename, 'w') as f:
                    for contact in contacts:
                        f.write(json.dumps(contact) + '\n')
                
                print(f"File rewritten with {len(contacts)} contacts")  # Debug
                
                # Verify the file was written correctly
                with open(filename, 'r') as f:
                    new_content = f.read()
                    print(f"File content after deletion:\n{new_content}")  # Debug
                
                return True
            else:
                print("Contact not found in file!")  # Debug
                return False
                
        except Exception as e:
            print(f"Error deleting contact from file: {e}")  # Debug
            return False
    
    def load_contacts(self):
        """Load contacts from files into linked list"""
        for contact_type in self.contact_types:
            filename = f"contacts/{contact_type}.txt"
            if os.path.exists(filename):
                try:
                    with open(filename, 'r') as f:
                        for line in f:
                            if line.strip():
                                try:
                                    contact = json.loads(line.strip())
                                    self.contact_list.insert(
                                        contact['name'],
                                        contact['phone'],
                                        contact['email'],
                                        contact['type']
                                    )
                                except json.JSONDecodeError:
                                    continue
                except Exception as e:
                    print(f"Error loading contacts from {filename}: {e}")
    
    def refresh_contact_display(self):
        """Refresh the contact display in treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all contacts
        contacts = self.contact_list.get_all_contacts()
        
        # Add contacts to treeview
        for contact in contacts:
            self.tree.insert('', 'end', values=(
                contact.name,
                contact.phone,
                contact.email,
                contact.contact_type
            ))
        
        # Update status
        self.status_var.set(f"Total contacts: {len(contacts)}")
    
    def search_contacts(self, event):
        """Search contacts by name"""
        search_term = self.search_var.get().lower()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all contacts
        contacts = self.contact_list.get_all_contacts()
        
        # Filter contacts
        filtered_contacts = [
            contact for contact in contacts
            if search_term in contact.name.lower()
        ]
        
        # Add filtered contacts to treeview
        for contact in filtered_contacts:
            self.tree.insert('', 'end', values=(
                contact.name,
                contact.phone,
                contact.email,
                contact.contact_type
            ))
        
        self.status_var.set(f"Found {len(filtered_contacts)} contacts")
    
    def filter_contacts(self, event):
        """Filter contacts by type"""
        filter_type = self.filter_var.get()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all contacts
        contacts = self.contact_list.get_all_contacts()
        
        # Filter contacts
        if filter_type == 'All':
            filtered_contacts = contacts
        else:
            filtered_contacts = [
                contact for contact in contacts
                if contact.contact_type == filter_type
            ]
        
        # Add filtered contacts to treeview
        for contact in filtered_contacts:
            self.tree.insert('', 'end', values=(
                contact.name,
                contact.phone,
                contact.email,
                contact.contact_type
            ))
        
        self.status_var.set(f"Showing {len(filtered_contacts)} contacts")

    def debug_files(self):
        """Debug function to check file contents"""
        print("\n=== DEBUG: File Contents ===")
        for contact_type in self.contact_types:
            filename = f"contacts/{contact_type}.txt"
            if os.path.exists(filename):
                print(f"\n--- {contact_type.upper()} ({filename}) ---")
                try:
                    with open(filename, 'r') as f:
                        content = f.read()
                        if content.strip():
                            for line_num, line in enumerate(content.split('\n'), 1):
                                if line.strip():
                                    try:
                                        contact = json.loads(line.strip())
                                        print(f"Line {line_num}: {contact}")
                                    except json.JSONDecodeError:
                                        print(f"Line {line_num}: Invalid JSON - {line}")
                        else:
                            print("File is empty")
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
            else:
                print(f"\n--- {contact_type.upper()} ---")
                print("File does not exist")
        print("=== END DEBUG ===\n")

def main():
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()