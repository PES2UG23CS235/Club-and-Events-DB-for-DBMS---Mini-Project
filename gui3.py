import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import mysql.connector
from datetime import datetime

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login - Club & Event Management System")
        self.root.geometry("500x600")
        self.root.configure(bg='#1a1a2e')
        
        # Database connection config
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'MySQLjadenspassword',  # CHANGE THIS
            'database': 'club_and_event'
        }
        
        self.current_user = None
        self.user_role = None
        self.user_id = None
        
        self.create_login_ui()
        
    def create_login_ui(self):
        # Header
        header = tk.Frame(self.root, bg='#16213e', height=100)
        header.pack(fill='x', padx=20, pady=20)
        
        tk.Label(header, text="Club & Event Management", 
                font=('Arial', 20, 'bold'), fg='#00fff5', bg='#16213e').pack(pady=5)
        tk.Label(header, text="Login to Continue", 
                font=('Arial', 12), fg='#95a5a6', bg='#16213e').pack()
        
        # Login form
        form_frame = tk.Frame(self.root, bg='#16213e', padx=40, pady=40)
        form_frame.pack(pady=30, padx=40, fill='both', expand=True)
        
        # User Type Selection
        tk.Label(form_frame, text="Login As:", font=('Arial', 12, 'bold'),
                fg='#00fff5', bg='#16213e').pack(pady=(0, 10))
        
        self.user_type_var = tk.StringVar(value='faculty')
        
        type_frame = tk.Frame(form_frame, bg='#16213e')
        type_frame.pack(pady=10)
        
        tk.Radiobutton(type_frame, text="Faculty Advisor", 
                      variable=self.user_type_var, value='faculty',
                      font=('Arial', 11), bg='#16213e', fg='white',
                      selectcolor='#0f3460', activebackground='#16213e',
                      activeforeground='#00fff5').pack(side='left', padx=20)
        
        tk.Radiobutton(type_frame, text="Student", 
                      variable=self.user_type_var, value='student',
                      font=('Arial', 11), bg='#16213e', fg='white',
                      selectcolor='#0f3460', activebackground='#16213e',
                      activeforeground='#00fff5').pack(side='left', padx=20)
        
        # User ID
        tk.Label(form_frame, text="User ID:", font=('Arial', 12, 'bold'),
                fg='#00fff5', bg='#16213e').pack(pady=(20, 5), anchor='w')
        
        self.user_id_entry = tk.Entry(form_frame, font=('Arial', 12), width=30)
        self.user_id_entry.pack(pady=5)
        self.user_id_entry.insert(0, "Enter Faculty ID or Student ID")
        self.user_id_entry.bind('<FocusIn>', lambda e: self.user_id_entry.delete(0, 'end'))
        
        # Password
        tk.Label(form_frame, text="Password:", font=('Arial', 12, 'bold'),
                fg='#00fff5', bg='#16213e').pack(pady=(20, 5), anchor='w')
        
        self.password_entry = tk.Entry(form_frame, font=('Arial', 12), width=30, show='*')
        self.password_entry.pack(pady=5)
        
        # Show password checkbox
        self.show_pass_var = tk.BooleanVar()
        tk.Checkbutton(form_frame, text="Show Password", variable=self.show_pass_var,
                      font=('Arial', 9), bg='#16213e', fg='#95a5a6',
                      selectcolor='#0f3460', activebackground='#16213e',
                      command=self.toggle_password).pack(pady=5, anchor='w')
        
        # Login button
        tk.Button(form_frame, text="Login", font=('Arial', 14, 'bold'),
                 bg='#27ae60', fg='white', padx=50, pady=15, cursor='hand2',
                 command=self.login).pack(pady=30)
        
        # Info section
        info_frame = tk.Frame(self.root, bg='#16213e', padx=20, pady=20)
        info_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(info_frame, text="Default Credentials:", 
                font=('Arial', 10, 'bold'), fg='#ffd700', bg='#16213e').pack()
        tk.Label(info_frame, text="Faculty: ID=1, Password=default123\nStudent: ID=1, Password=default123", 
                font=('Arial', 9), fg='#95a5a6', bg='#16213e').pack()
        
    def toggle_password(self):
        if self.show_pass_var.get():
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')
    
    def get_db_connection(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return None
    
    def login(self):
        user_id = self.user_id_entry.get().strip()
        password = self.password_entry.get()
        user_type = self.user_type_var.get()
        
        if not user_id or user_id == "Enter Faculty ID or Student ID" or not password:
            messagebox.showwarning("Missing Info", "Please enter both User ID and Password!")
            return
        
        conn = self.get_db_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            if user_type == 'faculty':
                query = """
                    SELECT faculty_id, first_name, last_name, department, password 
                    FROM facultyadvisor 
                    WHERE faculty_id = %s
                """
            else:
                query = """
                    SELECT student_id, first_name, last_name, semester, password 
                    FROM student 
                    WHERE student_id = %s
                """
            
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            
            if result:
                stored_password = result[4]
                
                if password == stored_password:
                    # Successful login
                    self.user_id = result[0]
                    self.current_user = f"{result[1]} {result[2]}"
                    self.user_role = user_type
                    
                    messagebox.showinfo("Login Successful", 
                                       f"Welcome, {self.current_user}!\n"
                                       f"Role: {user_type.capitalize()}")
                    
                    # Close login window and open main application
                    self.root.destroy()
                    self.open_main_application()
                else:
                    messagebox.showerror("Login Failed", "Incorrect password!")
            else:
                messagebox.showerror("Login Failed", f"No {user_type} found with ID: {user_id}")
            
            cursor.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Login error: {err}")
        finally:
            conn.close()
    
    def open_main_application(self):
        root = tk.Tk()
        app = ClubEventManagementGUI(root, self.user_id, self.current_user, 
                                     self.user_role, self.db_config)
        root.mainloop()
    
    def run(self):
        self.root.mainloop()


class ClubEventManagementGUI:
    def __init__(self, root, user_id, user_name, user_role, db_config):
        self.root = root
        self.user_id = user_id
        self.user_name = user_name
        self.user_role = user_role  # 'faculty' or 'student'
        self.db_config = db_config
        
        self.root.title(f"Club & Event Management - {user_name} ({user_role.capitalize()})")
        self.root.geometry("1100x750")
        self.root.configure(bg='#1a1a2e')
        
        # Create main container
        self.create_header()
        self.create_notebook()
        
    def get_db_connection(self):
        """Create database connection"""
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return None
    
    def check_permission(self, operation):
        """Check if user has permission for operation"""
        if self.user_role == 'faculty':
            return True  # Faculty has all permissions
        elif self.user_role == 'student':
            if operation in ['read', 'view']:
                return True  # Students can only view
            else:
                messagebox.showwarning("Permission Denied", 
                                      f"Students can only VIEW data.\n"
                                      f"Only Faculty Advisors can {operation.upper()} records.")
                return False
        return False
    
    def create_header(self):
        """Create header section with user info"""
        header = tk.Frame(self.root, bg='#16213e', height=100)
        header.pack(fill='x', padx=10, pady=10)
        
        title = tk.Label(header, text="Club & Event Management System", 
                        font=('Arial', 22, 'bold'), fg='#00fff5', bg='#16213e')
        title.pack(pady=10)
        
        # User info bar
        user_frame = tk.Frame(header, bg='#0f3460')
        user_frame.pack(fill='x', padx=20, pady=5)
        
        role_color = '#27ae60' if self.user_role == 'faculty' else '#3498db'
        role_icon = '👨‍🏫' if self.user_role == 'faculty' else '👨‍🎓'
        
        tk.Label(user_frame, text=f"{role_icon} Logged in as: {self.user_name}", 
                font=('Arial', 11, 'bold'), fg='white', bg='#0f3460').pack(side='left', padx=20, pady=5)
        
        tk.Label(user_frame, text=f"Role: {self.user_role.upper()}", 
                font=('Arial', 11, 'bold'), fg=role_color, bg='#0f3460').pack(side='left', padx=10)
        
        tk.Label(user_frame, text=f"ID: {self.user_id}", 
                font=('Arial', 10), fg='#95a5a6', bg='#0f3460').pack(side='left', padx=10)
        
        # Logout button
        tk.Button(user_frame, text="🚪 Logout", font=('Arial', 10, 'bold'),
                 bg='#e74c3c', fg='white', padx=20, pady=5, cursor='hand2',
                 command=self.logout).pack(side='right', padx=20)
    
    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.root.destroy()
            # Restart login window
            login = LoginWindow()
            login.run()
    
    def create_notebook(self):
        """Create tabbed interface"""
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background='#1a1a2e', borderwidth=0)
        style.configure('TNotebook.Tab', background='#0f3460', foreground='white', 
                       padding=[15, 8], font=('Arial', 10, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', '#e94560')],
                 foreground=[('selected', 'white')])
        
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tabs based on user role
        self.tab1 = tk.Frame(notebook, bg='#1a1a2e')
        self.tab2 = tk.Frame(notebook, bg='#1a1a2e')
        self.tab3 = tk.Frame(notebook, bg='#1a1a2e')
        
        notebook.add(self.tab1, text='Event Reports')
        notebook.add(self.tab2, text='Student Info')
        notebook.add(self.tab3, text='CRUD Operations')
        
        # Faculty-only tabs
        if self.user_role == 'faculty':
            self.tab4 = tk.Frame(notebook, bg='#1a1a2e')
            self.tab5 = tk.Frame(notebook, bg='#1a1a2e')
            self.tab6 = tk.Frame(notebook, bg='#1a1a2e')
            self.tab7 = tk.Frame(notebook, bg='#1a1a2e')
            
            notebook.add(self.tab4, text='Register Student')
            notebook.add(self.tab5, text='Update Payment')
            notebook.add(self.tab6, text='Add Student')
            notebook.add(self.tab7, text='Manage Registrations')
            
            self.create_registration_tab()
            self.create_payment_tab()
            self.create_add_student_tab()
            self.create_manage_registrations_tab()
        
        self.create_reports_tab()
        self.create_student_info_tab()
        self.create_crud_tab()
    
    def create_reports_tab(self):
        """Tab: Event Reports (Read-only for all)"""
        title = tk.Label(self.tab1, text="Event Reports & Analytics", 
                        font=('Arial', 18, 'bold'), fg='#00fff5', bg='#1a1a2e')
        title.pack(pady=20)
        
        # Buttons frame
        btn_frame = tk.Frame(self.tab1, bg='#1a1a2e')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Generate Full Report", 
                 font=('Arial', 12, 'bold'), bg='#e94560', fg='white',
                 padx=20, pady=10, cursor='hand2',
                 command=self.generate_report).pack(side='left', padx=10)
        
        tk.Button(btn_frame, text="Get Event Registrations", 
                 font=('Arial', 12, 'bold'), bg='#0f3460', fg='white',
                 padx=20, pady=10, cursor='hand2',
                 command=self.get_event_registrations).pack(side='left', padx=10)
        
        tk.Button(btn_frame, text="Get Event Revenue", 
                 font=('Arial', 12, 'bold'), bg='#533483', fg='white',
                 padx=20, pady=10, cursor='hand2',
                 command=self.get_event_revenue).pack(side='left', padx=10)
        
        # Event selection
        selection_frame = tk.Frame(self.tab1, bg='#16213e', padx=20, pady=15)
        selection_frame.pack(fill='x', padx=20)
        
        tk.Label(selection_frame, text="Select Event:", font=('Arial', 11, 'bold'),
                fg='#00fff5', bg='#16213e').pack(side='left', padx=10)
        
        self.event_var = tk.StringVar()
        self.event_dropdown = ttk.Combobox(selection_frame, textvariable=self.event_var,
                                          font=('Arial', 10), width=40, state='readonly')
        self.event_dropdown.pack(side='left', padx=10)
        self.load_events()
        
        # Results area
        result_frame = tk.Frame(self.tab1, bg='#16213e', padx=20, pady=20)
        result_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.report_text = scrolledtext.ScrolledText(result_frame, font=('Courier', 10),
                                                     bg='#0f1419', fg='#00fff5',
                                                     height=18, wrap='word')
        self.report_text.pack(fill='both', expand=True)
    
    def create_student_info_tab(self):
        """Tab: Student Information (Read-only for all)"""
        title = tk.Label(self.tab2, text="Student Event Participation", 
                        font=('Arial', 18, 'bold'), fg='#00fff5', bg='#1a1a2e')
        title.pack(pady=20)
        
        # Search frame
        search_frame = tk.Frame(self.tab2, bg='#16213e', padx=30, pady=30)
        search_frame.pack(pady=10, padx=50)
        
        tk.Label(search_frame, text="Select Student:", font=('Arial', 12, 'bold'),
                fg='#00fff5', bg='#16213e').grid(row=0, column=0, pady=10, padx=10)
        
        self.search_student_var = tk.StringVar()
        search_dropdown = ttk.Combobox(search_frame, textvariable=self.search_student_var,
                                      font=('Arial', 11), width=35, state='readonly')
        search_dropdown.grid(row=0, column=1, pady=10, padx=10)
        
        # Load students
        conn = self.get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT student_id, first_name, last_name FROM student")
            students = cursor.fetchall()
            search_dropdown['values'] = [f"{s[0]} - {s[1]} {s[2]}" for s in students]
            cursor.close()
            conn.close()
        
        tk.Button(search_frame, text="🔍 Get Event Count", 
                 font=('Arial', 12, 'bold'), bg='#e94560', fg='white',
                 padx=30, pady=12, cursor='hand2',
                 command=self.get_student_event_count).grid(row=1, column=0, 
                                                            columnspan=2, pady=20)
        
        # Result display
        self.student_info_frame = tk.Frame(self.tab2, bg='#16213e', padx=30, pady=30)
        self.student_info_frame.pack(fill='both', expand=True, padx=50, pady=10)
        
        self.student_result_label = tk.Label(self.student_info_frame, 
                                            text="Select a student and click search",
                                            font=('Arial', 13), fg='#ffd700', 
                                            bg='#16213e', justify='left')
        self.student_result_label.pack()
    
    def create_crud_tab(self):
        """Tab: CRUD Operations with role-based permissions"""
        title = tk.Label(self.tab3, text="CRUD Operations - Database Tables", 
                        font=('Arial', 18, 'bold'), fg='#00fff5', bg='#1a1a2e')
        title.pack(pady=15)
        
        # Permission indicator
        perm_color = '#27ae60' if self.user_role == 'faculty' else '#e74c3c'
        perm_text = "✅ Full Access (Create, Read, Update, Delete)" if self.user_role == 'faculty' else "View Only (Read access only)"
        
        tk.Label(self.tab3, text=f"Your Permissions: {perm_text}", 
                font=('Arial', 10, 'bold'), fg=perm_color, bg='#1a1a2e').pack()
        
        # Main frame
        main_frame = tk.Frame(self.tab3, bg='#16213e', padx=30, pady=20)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Table selection
        tk.Label(main_frame, text="Select Table:", font=('Arial', 12, 'bold'),
                fg='#00fff5', bg='#16213e').pack(pady=10)
        
        self.crud_table_var = tk.StringVar()
        tables = [
            "facultyadvisor", "student", "venue", "sponsor",
            "club", "event", "membership", "eventregistration",
            "payment", "sponsoredby"
        ]
        
        self.crud_table_dropdown = ttk.Combobox(main_frame, textvariable=self.crud_table_var,
                                               values=tables, font=('Arial', 11),
                                               width=40, state='readonly')
        self.crud_table_dropdown.pack(pady=10)
        
        # Operations buttons
        btn_frame = tk.Frame(main_frame, bg='#16213e')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="VIEW (Read)", font=('Arial', 11, 'bold'),
                 bg='#3498db', fg='white', padx=20, pady=10, cursor='hand2',
                 command=self.crud_read).grid(row=0, column=0, padx=5, pady=5)
        
        if self.user_role == 'faculty':
            tk.Button(btn_frame, text="CREATE", font=('Arial', 11, 'bold'),
                     bg='#27ae60', fg='white', padx=20, pady=10, cursor='hand2',
                     command=self.crud_create_wrapper).grid(row=0, column=1, padx=5, pady=5)
            
            tk.Button(btn_frame, text="UPDATE", font=('Arial', 11, 'bold'),
                     bg='#f39c12', fg='white', padx=20, pady=10, cursor='hand2',
                     command=self.crud_update_wrapper).grid(row=1, column=0, padx=5, pady=5)
            
            tk.Button(btn_frame, text="DELETE", font=('Arial', 11, 'bold'),
                     bg='#e74c3c', fg='white', padx=20, pady=10, cursor='hand2',
                     command=self.crud_delete_wrapper).grid(row=1, column=1, padx=5, pady=5)
        else:
            # Show disabled buttons for students
            tk.Button(btn_frame, text="CREATE (Faculty Only)", font=('Arial', 10),
                     bg='#7f8c8d', fg='white', padx=15, pady=8, state='disabled').grid(row=0, column=1, padx=5, pady=5)
            
            tk.Button(btn_frame, text="UPDATE (Faculty Only)", font=('Arial', 10),
                     bg='#7f8c8d', fg='white', padx=15, pady=8, state='disabled').grid(row=1, column=0, padx=5, pady=5)
            
            tk.Button(btn_frame, text="DELETE (Faculty Only)", font=('Arial', 10),
                     bg='#7f8c8d', fg='white', padx=15, pady=8, state='disabled').grid(row=1, column=1, padx=5, pady=5)
        
        # Results display
        self.crud_result_text = scrolledtext.ScrolledText(main_frame, font=('Courier', 9),
                                                         bg='#0f1419', fg='#00fff5',
                                                         height=20, wrap='word')
        self.crud_result_text.pack(fill='both', expand=True, pady=10)
    
    # CRUD wrappers with permission checks
    def crud_create_wrapper(self):
        if self.check_permission('create'):
            self.crud_create()
    
    def crud_update_wrapper(self):
        if self.check_permission('update'):
            self.crud_update()
    
    def crud_delete_wrapper(self):
        if self.check_permission('delete'):
            self.crud_delete()
    
    def crud_read(self):
        """READ operation - Available to all users"""
        if not self.crud_table_var.get():
            messagebox.showwarning("No Table", "Please select a table!")
            return
        
        table_name = self.crud_table_var.get()
        
        conn = self.get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            records = cursor.fetchall()
            
            cursor.execute(f"DESCRIBE {table_name}")
            columns = [col[0] for col in cursor.fetchall()]
            
            self.crud_result_text.delete(1.0, tk.END)
            self.crud_result_text.insert(tk.END, "=" * 100 + "\n")
            self.crud_result_text.insert(tk.END, f"VIEWING: {table_name.upper()}\n")
            self.crud_result_text.insert(tk.END, "=" * 100 + "\n\n")
            
            if records:
                header = " | ".join([f"{col:15}" for col in columns])
                self.crud_result_text.insert(tk.END, header + "\n")
                self.crud_result_text.insert(tk.END, "-" * len(header) + "\n")
                
                for record in records:
                    row = " | ".join([f"{str(val):15}" for val in record])
                    self.crud_result_text.insert(tk.END, row + "\n")
                
                self.crud_result_text.insert(tk.END, f"\nTotal Records: {len(records)}\n")
            else:
                self.crud_result_text.insert(tk.END, "No records found.\n")
            
            cursor.close()
            conn.close()
    
    def crud_create(self):
        """CREATE - Faculty only"""
        if not self.crud_table_var.get():
            messagebox.showwarning("No Table", "Please select a table!")
            return
        
        table_name = self.crud_table_var.get()
        
        conn = self.get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            cursor.close()
            conn.close()
        else:
            return
        
        # Create simplified insert dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Insert into {table_name}")
        dialog.geometry("500x600")
        dialog.configure(bg='#16213e')
        
        tk.Label(dialog, text=f"Insert New Record - {table_name.upper()}", 
                font=('Arial', 14, 'bold'), fg='#00fff5', bg='#16213e').pack(pady=20)
        
        canvas = tk.Canvas(dialog, bg='#16213e', highlightthickness=0)
        scrollbar = tk.Scrollbar(dialog, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#16213e')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        entries = {}
        for col in columns:
            frame = tk.Frame(scrollable_frame, bg='#16213e')
            frame.pack(pady=5, padx=20, fill='x')
            
            label_text = f"{col[0]}"
            if col[3] == 'PRI':
                label_text += " 🔑"
            if col[2] == 'NO':
                label_text += " *"
            
            tk.Label(frame, text=label_text, font=('Arial', 10),
                    fg='#00fff5', bg='#16213e', width=20, anchor='w').pack(side='left')
            
            entry = tk.Entry(frame, font=('Arial', 10), width=30)
            entry.pack(side='left', padx=10)
            entries[col[0]] = entry
        
        canvas.pack(side='left', fill='both', expand=True, padx=20)
        scrollbar.pack(side='right', fill='y')
        
        def insert():
            values = []
            cols_list = []
            for col_name, entry in entries.items():
                val = entry.get().strip()
                if val:
                    cols_list.append(col_name)
                    values.append(val if val.upper() != 'NULL' else None)
            
            if not values:
                messagebox.showwarning("No Data", "Enter at least one value!")
                return
            
            conn = self.get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    placeholders = ', '.join(['%s'] * len(values))
                    cols_str = ', '.join(cols_list)
                    cursor.execute(f"INSERT INTO {table_name} ({cols_str}) VALUES ({placeholders})", values)
                    conn.commit()
                    messagebox.showinfo("Success", f"Record inserted into {table_name}!")
                    dialog.destroy()
                    self.crud_read()
                    cursor.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Insert failed: {err}")
                finally:
                    conn.close()
        
        btn_frame = tk.Frame(dialog, bg='#16213e')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Insert", font=('Arial', 12, 'bold'),
                 bg='#27ae60', fg='white', padx=30, pady=10,
                 command=insert).pack(side='left', padx=10)
        
        tk.Button(btn_frame, text="Cancel", font=('Arial', 12, 'bold'),
                 bg='#e74c3c', fg='white', padx=30, pady=10,
                 command=dialog.destroy).pack(side='left', padx=10)
    
    def crud_update(self):
        """UPDATE - Faculty only"""
        if not self.crud_table_var.get():
            messagebox.showwarning("No Table", "Please select a table!")
            return
        
        table_name = self.crud_table_var.get()
        
        conn = self.get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            primary_key = next((col[0] for col in columns if col[3] == 'PRI'), None)
            
            if not primary_key:
                messagebox.showerror("Error", "No primary key found!")
                cursor.close()
                conn.close()
                return
            
            cursor.execute(f"SELECT * FROM {table_name}")
            records = cursor.fetchall()
            cursor.close()
            conn.close()
        else:
            return
        
        if not records:
            messagebox.showinfo("No Records", "No records to update!")
            return
        
        # Create update dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Update {table_name}")
        dialog.geometry("600x700")
        dialog.configure(bg='#16213e')
        
        tk.Label(dialog, text=f"Update Record - {table_name.upper()}", 
                font=('Arial', 14, 'bold'), fg='#00fff5', bg='#16213e').pack(pady=20)
        
        # Record selection
        tk.Label(dialog, text=f"Select record by {primary_key}:", 
                font=('Arial', 11, 'bold'), fg='#00fff5', bg='#16213e').pack(pady=10)
        
        record_var = tk.StringVar()
        pk_index = next(i for i, col in enumerate(columns) if col[0] == primary_key)
        record_options = [f"{record[pk_index]}" for record in records]
        
        record_dropdown = ttk.Combobox(dialog, textvariable=record_var,
                                      values=record_options, font=('Arial', 11),
                                      width=50, state='readonly')
        record_dropdown.pack(pady=10)
        
        # Fields container with scrollbar
        fields_container = tk.Frame(dialog, bg='#16213e')
        fields_container.pack(fill='both', expand=True, pady=10, padx=20)
        
        canvas = tk.Canvas(fields_container, bg='#16213e', highlightthickness=0)
        scrollbar = tk.Scrollbar(fields_container, orient='vertical', command=canvas.yview)
        fields_frame = tk.Frame(canvas, bg='#16213e')
        
        fields_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=fields_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        entries = {}
        
        def load_record_data(event=None):
            """Load selected record data into form"""
            if not record_var.get():
                return
            
            # Clear previous entries
            for widget in fields_frame.winfo_children():
                widget.destroy()
            entries.clear()
            
            pk_value = record_var.get()
            
            # Fetch the selected record
            conn = self.get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table_name} WHERE {primary_key} = %s", (pk_value,))
                record = cursor.fetchone()
                cursor.close()
                conn.close()
                
                if record:
                    # Create input fields for each column
                    for i, col in enumerate(columns):
                        field_frame = tk.Frame(fields_frame, bg='#16213e')
                        field_frame.pack(pady=5, fill='x', padx=10)
                        
                        label_text = f"{col[0]}"
                        if col[3] == 'PRI':
                            label_text += "(Cannot modify)"
                        
                        tk.Label(field_frame, text=label_text, font=('Arial', 10),
                                fg='#00fff5', bg='#16213e', width=20, anchor='w').pack(side='left')
                        
                        entry = tk.Entry(field_frame, font=('Arial', 10), width=35)
                        entry.pack(side='left', padx=10)
                        
                        # Insert current value
                        current_value = record[i] if record[i] is not None else ''
                        entry.insert(0, str(current_value))
                        
                        # Disable primary key field
                        if col[3] == 'PRI':
                            entry.config(state='disabled', bg='#2c3e50')
                        
                        entries[col[0]] = entry
        
        # Bind record selection to load data
        record_dropdown.bind('<<ComboboxSelected>>', load_record_data)
        
        def update_record():
            """Execute UPDATE query"""
            if not record_var.get():
                messagebox.showwarning("No Selection", "Please select a record!")
                return
            
            if not entries:
                messagebox.showwarning("No Data", "Please load a record first!")
                return
            
            pk_value = record_var.get()
            
            # Build UPDATE query
            updates = []
            values = []
            
            for col_name, entry in entries.items():
                if entry['state'] != 'disabled':  # Skip primary key
                    val = entry.get().strip()
                    updates.append(f"{col_name} = %s")
                    values.append(val if val else None)
            
            if not updates:
                messagebox.showwarning("No Changes", "No fields to update!")
                return
            
            values.append(pk_value)  # Add PK value for WHERE clause
            
            conn = self.get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    query = f"UPDATE {table_name} SET {', '.join(updates)} WHERE {primary_key} = %s"
                    cursor.execute(query, values)
                    conn.commit()
                    
                    messagebox.showinfo("Success", f"Record updated in {table_name}!")
                    dialog.destroy()
                    self.crud_read()  # Refresh the main display
                    
                    cursor.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Update failed: {err}")
                finally:
                    conn.close()
        
        # Button frame at bottom
        btn_frame = tk.Frame(dialog, bg='#16213e')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Update Record", font=('Arial', 12, 'bold'),
                 bg='#f39c12', fg='white', padx=30, pady=10,
                 command=update_record).pack(side='left', padx=10)
        
        tk.Button(btn_frame, text="Cancel", font=('Arial', 12, 'bold'),
                 bg='#e74c3c', fg='white', padx=30, pady=10,
                 command=dialog.destroy).pack(side='left', padx=10)
    
    def crud_delete(self):
        """DELETE - Faculty only"""
        if not self.crud_table_var.get():
            messagebox.showwarning("No Table", "Please select a table!")
            return
        
        table_name = self.crud_table_var.get()
        
        conn = self.get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            primary_key = next((col[0] for col in columns if col[3] == 'PRI'), None)
            
            cursor.execute(f"SELECT * FROM {table_name}")
            records = cursor.fetchall()
            cursor.close()
            conn.close()
        else:
            return
        
        if not records:
            messagebox.showinfo("No Records", "No records to delete!")
            return
        
        # Create delete dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Delete from {table_name}")
        dialog.geometry("600x400")
        dialog.configure(bg='#16213e')
        
        tk.Label(dialog, text=f"DELETE Record - {table_name.upper()}", 
                font=('Arial', 14, 'bold'), fg='#ff6b6b', bg='#16213e').pack(pady=20)
        
        tk.Label(dialog, text=f"Select record by {primary_key}:", 
                font=('Arial', 11, 'bold'), fg='#00fff5', bg='#16213e').pack()
        
        record_var = tk.StringVar()
        pk_index = next(i for i, col in enumerate(columns) if col[0] == primary_key)
        record_options = [f"{record[pk_index]}" for record in records]
        
        record_dropdown = ttk.Combobox(dialog, textvariable=record_var,
                                      values=record_options, font=('Arial', 11),
                                      width=50, state='readonly')
        record_dropdown.pack(pady=10)
        
        tk.Label(dialog, text="This cannot be undone!", 
                font=('Arial', 10, 'italic'), fg='#ffd700', bg='#16213e').pack(pady=20)
        
        def delete():
            if not record_var.get():
                messagebox.showwarning("No Selection", "Select a record!")
                return
            
            pk_value = record_var.get()
            confirm = messagebox.askyesno("Confirm", f"Delete record with {primary_key} = {pk_value}?")
            
            if not confirm:
                return
            
            conn = self.get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(f"DELETE FROM {table_name} WHERE {primary_key} = %s", (pk_value,))
                    conn.commit()
                    messagebox.showinfo("Success", "Record deleted!")
                    dialog.destroy()
                    self.crud_read()
                    cursor.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Delete failed: {err}")
                finally:
                    conn.close()
        
        btn_frame = tk.Frame(dialog, bg='#16213e')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Delete", font=('Arial', 12, 'bold'),
                 bg='#e74c3c', fg='white', padx=30, pady=10,
                 command=delete).pack(side='left', padx=10)
        
        tk.Button(btn_frame, text="Cancel", font=('Arial', 12, 'bold'),
                 bg='#95a5a6', fg='white', padx=30, pady=10,
                 command=dialog.destroy).pack(side='left', padx=10)
    
    # Faculty-only tabs
    def create_registration_tab(self):
        """Faculty only: Register students"""
        title = tk.Label(self.tab4, text="Register Student for Event", 
                        font=('Arial', 18, 'bold'), fg='#00fff5', bg='#1a1a2e')
        title.pack(pady=20)
        
        form_frame = tk.Frame(self.tab4, bg='#16213e', padx=30, pady=30)
        form_frame.pack(pady=10, padx=50, fill='both', expand=True)
        
        tk.Label(form_frame, text="Select Student:", font=('Arial', 12, 'bold'),
                fg='#00fff5', bg='#16213e').grid(row=0, column=0, sticky='w', pady=10)
        
        self.student_var = tk.StringVar()
        self.student_dropdown = ttk.Combobox(form_frame, textvariable=self.student_var,
                                            font=('Arial', 11), width=35, state='readonly')
        self.student_dropdown.grid(row=0, column=1, pady=10, padx=10)
        self.load_students()
        
        tk.Label(form_frame, text="Select Event:", font=('Arial', 12, 'bold'),
                fg='#00fff5', bg='#16213e').grid(row=1, column=0, sticky='w', pady=10)
        
        self.reg_event_var = tk.StringVar()
        self.reg_event_dropdown = ttk.Combobox(form_frame, textvariable=self.reg_event_var,
                                          font=('Arial', 11), width=35, state='readonly')
        self.reg_event_dropdown.grid(row=1, column=1, pady=10, padx=10)
        self.load_events_for_registration()
        
        tk.Label(form_frame, text="Payment Mode:", font=('Arial', 12, 'bold'),
                fg='#00fff5', bg='#16213e').grid(row=2, column=0, sticky='w', pady=10)
        
        self.payment_mode_var = tk.StringVar(value='UPI')
        payment_dropdown = ttk.Combobox(form_frame, textvariable=self.payment_mode_var,
                                       values=['UPI', 'Card', 'Cash', 'Net Banking'], 
                                       font=('Arial', 11), width=35, state='readonly')
        payment_dropdown.grid(row=2, column=1, pady=10, padx=10)
        
        tk.Button(form_frame, text="Register Student", 
                font=('Arial', 14, 'bold'), bg='#e94560', fg='white',
                padx=30, pady=15, cursor='hand2',
                command=self.register_student).grid(row=3, column=0, columnspan=2, pady=30)
        
        tk.Label(form_frame, text="Uses stored procedure 'register_student_for_event'",
                font=('Arial', 10, 'italic'), fg='#ffd700', bg='#16213e').grid(row=4, column=0, columnspan=2)
    
    def create_payment_tab(self):
        """Faculty only: Update payments"""
        title = tk.Label(self.tab5, text="Update Payment Status", 
                        font=('Arial', 18, 'bold'), fg='#00fff5', bg='#1a1a2e')
        title.pack(pady=20)
        
        form_frame = tk.Frame(self.tab5, bg='#16213e', padx=30, pady=30)
        form_frame.pack(pady=10, padx=50)
        
        tk.Label(form_frame, text="Select Registration:", font=('Arial', 12, 'bold'),
                fg='#00fff5', bg='#16213e').grid(row=0, column=0, sticky='w', pady=10)
        
        self.payment_reg_var = tk.StringVar()
        self.payment_dropdown = ttk.Combobox(form_frame, textvariable=self.payment_reg_var,
                                            font=('Arial', 11), width=50, state='readonly')
        self.payment_dropdown.grid(row=0, column=1, pady=10, padx=10)
        self.load_pending_payments()
        
        tk.Button(form_frame, text="Mark Payment as Completed", 
                 font=('Arial', 14, 'bold'), bg='#27ae60', fg='white',
                 padx=30, pady=15, cursor='hand2',
                 command=self.update_payment_status).grid(row=1, column=0, columnspan=2, pady=20)
        
        tk.Button(form_frame, text="Refresh List", 
                 font=('Arial', 12, 'bold'), bg='#0f3460', fg='white',
                 padx=20, pady=10, cursor='hand2',
                 command=self.load_pending_payments).grid(row=2, column=0, columnspan=2, pady=10)
        
        tk.Label(form_frame, text="Auto-confirms attendance via trigger",
                font=('Arial', 10, 'italic'), fg='#ffd700', bg='#16213e').grid(row=3, column=0, columnspan=2, pady=20)
        
        self.payment_status_text = scrolledtext.ScrolledText(self.tab5, font=('Courier', 11),
                                                            bg='#0f1419', fg='#00fff5',
                                                            height=12, wrap='word')
        self.payment_status_text.pack(fill='both', expand=True, padx=50, pady=10)
    
    def create_add_student_tab(self):
        """Faculty only: Add new students"""
        title = tk.Label(self.tab6, text="Add New Student", 
                        font=('Arial', 18, 'bold'), fg='#00fff5', bg='#1a1a2e')
        title.pack(pady=20)
        
        form_frame = tk.Frame(self.tab6, bg='#16213e', padx=40, pady=30)
        form_frame.pack(pady=10, padx=50)
        
        fields = [
            ("Student ID:", "new_student_id"),
            ("First Name:", "new_first_name"),
            ("Last Name:", "new_last_name"),
            ("Date of Birth (YYYY-MM-DD):", "new_dob"),
            ("Phone:", "new_phone"),
            ("Semester:", "new_semester"),
            ("Email:", "new_email"),
            ("Password:", "new_password")
        ]
        
        self.student_entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(form_frame, text=label, font=('Arial', 11, 'bold'),
                    fg='#00fff5', bg='#16213e').grid(row=i, column=0, sticky='w', pady=8, padx=10)
            
            entry = tk.Entry(form_frame, font=('Arial', 11), width=35)
            entry.grid(row=i, column=1, pady=8, padx=10)
            self.student_entries[key] = entry
            
            if key == "new_dob":
                entry.insert(0, "2003-01-15")
            elif key == "new_password":
                entry.insert(0, "default123")
        
        tk.Button(form_frame, text="Add Student", 
                 font=('Arial', 14, 'bold'), bg='#27ae60', fg='white',
                 padx=30, pady=15, cursor='hand2',
                 command=self.add_new_student).grid(row=len(fields), column=0, columnspan=2, pady=25)
        
        tk.Label(form_frame, text="Age calculated automatically by trigger!",
                font=('Arial', 10, 'italic'), fg='#ffd700', bg='#16213e').grid(row=len(fields)+1, column=0, columnspan=2)
    
    def create_manage_registrations_tab(self):
        """Faculty only: Manage registrations"""
        title = tk.Label(self.tab7, text="Manage Event Registrations", 
                        font=('Arial', 18, 'bold'), fg='#00fff5', bg='#1a1a2e')
        title.pack(pady=20)
        
        tk.Label(self.tab7, text="Faculty Only - Manage and Delete Registrations", 
                font=('Arial', 11, 'bold'), fg='#ffd700', bg='#1a1a2e').pack()
        
        form_frame = tk.Frame(self.tab7, bg='#16213e', padx=40, pady=30)
        form_frame.pack(pady=10, padx=50)
        
        tk.Label(form_frame, text="Select Event:", font=('Arial', 12, 'bold'),
                fg='#00fff5', bg='#16213e').grid(row=0, column=0, sticky='w', pady=10)
        
        self.delete_event_var = tk.StringVar()
        self.delete_event_dropdown = ttk.Combobox(form_frame, textvariable=self.delete_event_var,
                                                 font=('Arial', 11), width=40, state='readonly')
        self.delete_event_dropdown.grid(row=0, column=1, pady=10, padx=10)
        self.load_events_for_delete()
        
        btn_frame = tk.Frame(form_frame, bg='#16213e')
        btn_frame.grid(row=1, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="View Registrations", 
                 font=('Arial', 11, 'bold'), bg='#0f3460', fg='white',
                 padx=15, pady=10, cursor='hand2',
                 command=self.view_event_registrations).pack(side='left', padx=10)
        
        tk.Button(btn_frame, text="Delete All for Event", 
                 font=('Arial', 11, 'bold'), bg='#c0392b', fg='white',
                 padx=15, pady=10, cursor='hand2',
                 command=self.delete_event_registrations).pack(side='left', padx=10)
        
        self.manage_reg_text = scrolledtext.ScrolledText(self.tab7, font=('Courier', 10),
                                                         bg='#0f1419', fg='#00fff5',
                                                         height=18, wrap='word')
        self.manage_reg_text.pack(fill='both', expand=True, padx=50, pady=10)
    
    # Data loading methods
    def load_students(self):
        conn = self.get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT student_id, first_name, last_name FROM student")
            students = cursor.fetchall()
            self.student_dropdown['values'] = [f"{s[0]} - {s[1]} {s[2]}" for s in students]
            cursor.close()
            conn.close()
    
    def load_events(self):
        conn = self.get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT event_id, event_name, event_date FROM event")
            events = cursor.fetchall()
            self.event_dropdown['values'] = [f"{e[0]} - {e[1]} ({e[2]})" for e in events]
            cursor.close()
            conn.close()
    
    def load_events_for_registration(self):
        conn = self.get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT event_id, event_name, event_date FROM event")
            events = cursor.fetchall()
            self.reg_event_dropdown['values'] = [f"{e[0]} - {e[1]} ({e[2]})" for e in events]
            cursor.close()
            conn.close()
    
    def load_pending_payments(self):
        conn = self.get_db_connection()
        if conn:
            cursor = conn.cursor()
            query = """
                SELECT p.payment_id, s.first_name, s.last_name, e.event_name, p.amount
                FROM payment p
                JOIN eventregistration er ON p.reg_id = er.reg_id
                JOIN student s ON er.student_id = s.student_id
                JOIN event e ON er.event_id = e.event_id
                WHERE p.status = 'Pending'
            """
            cursor.execute(query)
            payments = cursor.fetchall()
            self.payment_dropdown['values'] = [f"{p[0]} - {p[1]} {p[2]} - {p[3]} - ₹{p[4]}" for p in payments]
            cursor.close()
            conn.close()
    
    def load_events_for_delete(self):
        conn = self.get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.event_id, e.event_name, COUNT(er.reg_id) as reg_count
                FROM event e
                LEFT JOIN eventregistration er ON e.event_id = er.event_id
                GROUP BY e.event_id, e.event_name
            """)
            events = cursor.fetchall()
            self.delete_event_dropdown['values'] = [f"{e[0]} - {e[1]} ({e[2]} regs)" for e in events]
            cursor.close()
            conn.close()
    
    # Action methods
    def register_student(self):
        if not self.student_var.get() or not self.reg_event_var.get():
            messagebox.showwarning("Missing Info", "Select both student and event!")
            return
        
        student_id = int(self.student_var.get().split(' - ')[0])
        event_id = int(self.reg_event_var.get().split(' - ')[0])
        payment_mode = self.payment_mode_var.get()
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.callproc('register_student_for_event', [student_id, event_id, payment_mode])
                conn.commit()
                messagebox.showinfo("Success", "Student registered successfully!")
                cursor.close()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Registration failed: {err}")
            finally:
                conn.close()
    
    def update_payment_status(self):
        if not self.payment_reg_var.get():
            messagebox.showwarning("No Selection", "Select a payment!")
            return
        
        payment_id = int(self.payment_reg_var.get().split(' - ')[0])
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(f"UPDATE payment SET status = 'Completed' WHERE payment_id = {payment_id}")
                conn.commit()
                
                self.payment_status_text.delete(1.0, tk.END)
                self.payment_status_text.insert(tk.END, "PAYMENT UPDATED\n")
                self.payment_status_text.insert(tk.END, f"Payment ID: {payment_id}\n")
                self.payment_status_text.insert(tk.END, "Trigger activated: Attendance auto-confirmed!\n")
                
                messagebox.showinfo("Success", "Payment updated!")
                self.load_pending_payments()
                cursor.close()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Update failed: {err}")
            finally:
                conn.close()
    
    def add_new_student(self):
        entries = self.student_entries
        if not all([entries[k].get() for k in ['new_student_id', 'new_first_name', 'new_last_name', 'new_dob', 'new_phone', 'new_semester', 'new_email']]):
            messagebox.showwarning("Missing Info", "Fill all required fields!")
            return
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    INSERT INTO student (student_id, first_name, last_name, dob, phone, semester, email, password)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    entries['new_student_id'].get(),
                    entries['new_first_name'].get(),
                    entries['new_last_name'].get(),
                    entries['new_dob'].get(),
                    entries['new_phone'].get(),
                    entries['new_semester'].get(),
                    entries['new_email'].get(),
                    entries['new_password'].get()
                )
                cursor.execute(query, values)
                conn.commit()
                messagebox.showinfo("Success", "Student added! Age auto-calculated by trigger!")
                
                # Clear form
                for entry in entries.values():
                    entry.delete(0, tk.END)
                entries['new_dob'].insert(0, "2003-01-15")
                entries['new_password'].insert(0, "default123")
                
                self.load_students()
                cursor.close()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed: {err}")
            finally:
                conn.close()
    
    def view_event_registrations(self):
        if not self.delete_event_var.get():
            messagebox.showwarning("No Event", "Select an event!")
            return
        
        event_id = int(self.delete_event_var.get().split(' - ')[0])
        
        conn = self.get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT er.reg_id, s.first_name, s.last_name, er.attendance_status, p.amount, p.status
                FROM eventregistration er
                JOIN student s ON er.student_id = s.student_id
                LEFT JOIN payment p ON er.reg_id = p.reg_id
                WHERE er.event_id = %s
            """, (event_id,))
            regs = cursor.fetchall()
            
            self.manage_reg_text.delete(1.0, tk.END)
            self.manage_reg_text.insert(tk.END, f"=== Event ID {event_id} Registrations ===\n\n")
            
            if regs:
                for r in regs:
                    self.manage_reg_text.insert(tk.END, f"Reg {r[0]}: {r[1]} {r[2]} | Attend: {r[3]} | Pay: ₹{r[4]} ({r[5]})\n")
                self.manage_reg_text.insert(tk.END, f"\nTotal: {len(regs)}\n")
            else:
                self.manage_reg_text.insert(tk.END, "No registrations.\n")
            
            cursor.close()
            conn.close()
    
    def delete_event_registrations(self):
        if not self.delete_event_var.get():
            messagebox.showwarning("No Event", "Select an event!")
            return
        
        event_id = int(self.delete_event_var.get().split(' - ')[0])
        confirm = messagebox.askyesno("Confirm", f"Delete ALL registrations for event {event_id}?")
        
        if not confirm:
            return
        
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM payment WHERE reg_id IN (SELECT reg_id FROM eventregistration WHERE event_id = %s)", (event_id,))
                cursor.execute("DELETE FROM eventregistration WHERE event_id = %s", (event_id,))
                conn.commit()
                
                messagebox.showinfo("Success", "Registrations deleted!")
                self.load_events_for_delete()
                cursor.close()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed: {err}")
            finally:
                conn.close()
    
    # Report functions
    def generate_report(self):
        conn = self.get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.callproc('generate_event_report')
            
            results = []
            for result in cursor.stored_results():
                results = result.fetchall()
            
            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(tk.END, "=" * 70 + "\n")
            self.report_text.insert(tk.END, "EVENT REPORT\n")
            self.report_text.insert(tk.END, "=" * 70 + "\n\n")
            
            for row in results:
                self.report_text.insert(tk.END, f"Event: {row[0]}\n")
                self.report_text.insert(tk.END, f"  Registrations: {row[1]}\n")
                self.report_text.insert(tk.END, f"  Revenue: ₹{row[2]}\n")
                self.report_text.insert(tk.END, "-" * 70 + "\n")
            
            cursor.close()
            conn.close()
    
    def get_event_registrations(self):
        if not self.event_var.get():
            messagebox.showwarning("No Event", "Select an event!")
            return
        
        event_id = int(self.event_var.get().split(' - ')[0])
        
        conn = self.get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT get_total_registrations({event_id})")
            count = cursor.fetchone()[0]
            
            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(tk.END, f"Event ID {event_id}: {count} registrations\n")
            cursor.close()
            conn.close()
    
    def get_event_revenue(self):
        if not self.event_var.get():
            messagebox.showwarning("No Event", "Select an event!")
            return
        
        event_id = int(self.event_var.get().split(' - ')[0])
        
        conn = self.get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT get_total_revenue({event_id})")
            revenue = cursor.fetchone()[0]
            
            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(tk.END, f"Event ID {event_id}: ₹{revenue} revenue\n")
            cursor.close()
            conn.close()
    
    def get_student_event_count(self):
        if not self.search_student_var.get():
            messagebox.showwarning("No Student", "Select a student!")
            return
        
        student_id = int(self.search_student_var.get().split(' - ')[0])
        
        conn = self.get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT get_event_count_for_student({student_id})")
            count = cursor.fetchone()[0]
            
            cursor.execute(f"SELECT first_name, last_name FROM student WHERE student_id = {student_id}")
            name = cursor.fetchone()
            
            result_text = f"Student: {name[0]} {name[1]} (ID: {student_id})\n\n"
            result_text += f"📅 Total Events Attended: {count}\n"
            
            self.student_result_label.config(text=result_text)
            cursor.close()
            conn.close()


# Run the application
if __name__ == "__main__":
    login = LoginWindow()
    login.run()