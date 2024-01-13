import customtkinter as ctk
from tkcalendar import Calendar
from datetime import datetime, timedelta
import psycopg2

# Connect to PostgreSQL database
conn = psycopg2.connect(host = "localhost", port = "5432", database = "hobby_db_1", user = "postgres", password = "123")
cur = conn.cursor()

global_username = ""        # Holds username globally for preventing too much argument passing or querying
global_userid = 0           # Holds userid globally for preventing too much argument passing or querying
global_productname = ""     # This is for search function in the main screen

ctk.deactivate_automatic_dpi_awareness()
ctk.set_widget_scaling(1.3)

class MainApplication(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Hobi Pazarı")

        self.center_window(1000, 800)

        self.login_screen = LoginScreen(self, self.show_homepage)
        self.login_screen.pack()

    def center_window(self, width=1000, height=680):
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate x and y coordinates
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        # Set the window's position
        self.geometry(f'{width}x{height}+{x}+{y}')

    def show_homepage(self):
        self.homepage = Homepage(self, self.logout)
        self.homepage.pack()
        self.login_screen.destroy()
    
    def logout(self):
        self.homepage.destroy()
        self.login_screen = LoginScreen(self, self.show_homepage)
        self.login_screen.pack()

class Homepage(ctk.CTkFrame):
    def __init__(self, parent, logout, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        global global_username
        
        self.parent = parent        
        self.logout = logout
        
        # Create a new frame for buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10, padx=10)  # or use grid() to place this frame

        # Place buttons inside the button_frame using grid layout
        self.profile = ctk.CTkButton(button_frame, text=global_username, fg_color="transparent", border_width=2, border_color="#454545", hover_color="#595959", command=self.on_update_click)
        self.profile.grid(row=0, column=1, pady=5, padx=5)

        self.cikis = ctk.CTkButton(button_frame, text="Çıkış Yap", fg_color="#CC2222", hover_color="#992222", command=self.logout_buttton)
        self.cikis.grid(row=1, column=1, pady=5, padx=5)

        self.sepet = ctk.CTkButton(button_frame, text="Sepet", font=("Helvetica", 14, "bold"), command=self.open_sepet)
        self.sepet.grid(row=0, column=0, pady=5, padx=5)

        self.satin_alinan = ctk.CTkButton(button_frame, text="Satın Alınanlar", command=self.open_satin_alinanlar)
        self.satin_alinan.grid(row=1, column=0, pady=5, padx=5)
        
        search_frame = ctk.CTkFrame(self)
        search_bar = ctk.CTkEntry(search_frame, width=200, placeholder_text="Ara")
        search_bar.pack(pady=6, padx=6, side="left")
        
        search_but = ctk.CTkButton(search_frame, text="Ara", width=50, command= lambda: self.search_ref(search_bar.get()))
        search_but.pack(pady=6, padx=6, side="right")
        
        search_frame.pack()
        
        # Scrollable container setup
        self.product_boxes = ctk.CTkScrollableFrame(self,
                                               height=350,
                                               width=300,
                                               label_text="Ürünler",
                                               label_anchor="center",
                                               label_font=("Helvetica", 20, "bold"))
        self.product_boxes.pack(pady=5, padx=20)

        # Product data
        global global_productname
        
        product_table = self.search(global_productname)
        
        # Add product boxes to the grid
        for product in product_table:
            ProductBox(self.product_boxes, product[0], product[2], product[3], product[5], product[4], product[6], product[1], self.update_sepet_label).pack(pady=10)
                                      #product_id, product_name, information, price, category, stock, seller_id,

        self.counter = 0
        self.product_list = []
    
        self.sepet_hata = ctk.CTkLabel(self, text="", text_color="#FF0000")
        self.sepet_hata.pack()
        
        self.sepet_win = None
        self.satin_alinan_win = None
        self.update_window = None

    def search(self, product_name):
        if product_name == "":
            cur.execute("""SELECT * FROM get_products_by_name(' ');""")
        else:
            cur.execute("""SELECT * FROM get_products_by_name(%s);""", (product_name,))
        return cur.fetchall()
    
    def search_ref(self, product_name):
        global global_productname
        global_productname = product_name
        
        # Clear existing product boxes
        for widget in self.product_boxes.winfo_children():
            widget.destroy()

        # Fetch and display new product data
        product_table = self.search(global_productname)
        print(product_table)
        for product in product_table:
            ProductBox(self.product_boxes, product[0], product[2], product[3], product[5], product[4], product[6], product[1], self.update_sepet_label).pack(pady=10)
        
        if product_table == []:
            self.sepet_hata.configure(text="Ürün bulunamadı")
        else:
            self.sepet_hata.configure(text="")
        
    def logout_buttton(self):
        global global_username
        global global_userid
        global_username = ""
        global_userid = 0
        self.logout()
      
    def open_satin_alinanlar(self):
        if self.sepet_win is None or not self.sepet_win.winfo_exists():
            self.sepet_win = satin_alinan_window(self)  # create window if its None or destroyed
            self.sepet_win.focus_set()  # Force focus on the new window
            self.sepet_win.grab_set()
            self.wait_window(self.sepet_win)
        else:
            self.sepet_win.focus()  # if window exists focus it
    
    def open_sepet(self):
        if self.product_list == []:
            self.sepet.configure(text="Sepet Boş ಥ_ಥ",)
            
        else:
            if self.sepet_win is None or not self.sepet_win.winfo_exists():
                self.sepet_win = sepet_window(self, self.product_list, self.refresh_homepage)
                self.sepet_win.focus_set() 
                self.sepet_win.grab_set()
                self.wait_window(self.sepet_win)
            else:
                self.sepet_win.focus()

    def update_sepet_label(self, product_id):
        self.counter += 1
        self.product_list.append(product_id)
        self.sepet.configure(text=f"Sepet: {self.counter}", fg_color="#2f7bb6")
        
    def refresh_homepage(self):
        # Reset the product list and the basket counter.
        self.product_list = []
        self.counter = 0
        self.sepet.configure(text="Satın Alındı", fg_color="#007700")
        
    def on_update_click(self):
        if self.update_window is None or not self.update_window.winfo_exists():
            self.update_window = update_user(self)  # create window if its None or destroyed
            self.update_window.focus_set()   # Force focus on the new window
            self.update_window.grab_set()
            self.wait_window(self.update_window)
        else:
            self.update_window.focus()  # if window exists focus it

class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, on_login_success, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.on_login_success = on_login_success

        mainlabel = ctk.CTkLabel(self, text="Hobi Pazarı", font=("Helvetica", 30, "bold"))
        mainlabel.pack(pady=(50, 20), padx=(100,100))

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Kullanıcı Adı")
        self.username_entry.pack(pady=(20, 20))

        self.password_entry = ctk.CTkEntry(self, show="*", placeholder_text="Şifre")
        self.password_entry.pack(pady=(0, 20))

        # Error label for login related messages
        login_button = ctk.CTkButton(self, text="Giriş Yap", hover_color="#2f7bb6",  command=lambda: self.on_login_click())
        login_button.pack()

        register_button = ctk.CTkButton(self, text="Kaydol", fg_color="transparent", border_color="#565b5e", hover_color="#343a3c", border_width=2, command=self.on_register_click)
        register_button.pack(pady=(20, 20))

        self.hata_label = ctk.CTkLabel(self, text="", font=("Helvetica", 12), text_color="#FF0000")
        self.hata_label.pack(pady=(0,10))
        
        self.register_window = None
    
    def on_register_click(self):
        if self.register_window is None or not self.register_window.winfo_exists():
            self.register_window = register(self)  # create window if its None or destroyed
            self.register_window.focus_set()  # Force focus on the new window
            self.register_window.grab_set()
            self.wait_window(self.register_window)
        else:
            self.register_window.focus()  # if window exists focus it

    def on_login_click(self):
        global global_username
        global global_userid
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # SQL query to fetch user information
        cur.execute("""SELECT username, userid, password FROM users WHERE username = %s
                       UNION
                       SELECT NULL, NULL, password FROM users WHERE username = %s
                       LIMIT 1""", (username, username))

        
        info = cur.fetchone()
        
        # Check login credentials
        if info == None:
            self.hata_label.configure(text="(￣﹃￣) Geçersiz Kullanıcı Adı veya Şifre (￣﹃￣)")
        elif(info[0] != username and info[2] != password):
            self.hata_label.configure(text="(￣﹃￣) Geçersiz Kullanıcı Adı veya Şifre (￣﹃￣)")
        elif(info[0] == username and info[2] == password):
            global_username = username
            global_userid = info[1]
            self.on_login_success()

class register(ctk.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # screen adjustments and geometry set
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 800
        height = 800
        
        # Calculate x and y coordinates
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        
        # Set the window's position
        self.geometry(f'{width}x{height}+{x}+{y}')

        mainlabel = ctk.CTkLabel(self, text="Kaydol", font=("Helvetica", 30, "bold"))
        mainlabel.pack(pady=(10, 20))
        
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Kullanıcı Adınız")
        self.username_entry.pack(pady=5)

        self.pass_entry = ctk.CTkEntry(self, placeholder_text="Şifreniz")
        self.pass_entry.pack(pady=5)

        self.name_entry = ctk.CTkEntry(self, placeholder_text="Adınız")
        self.name_entry.pack(pady=5)

        self.surname_entry = ctk.CTkEntry(self, placeholder_text="Soyadınız")
        self.surname_entry.pack(pady=5)

        self.mail_entry = ctk.CTkEntry(self, placeholder_text="E-posta Adresiniz")
        self.mail_entry.pack(pady=5)

        self.phone_entry = ctk.CTkEntry(self, placeholder_text="Telefon Numaranız")
        self.phone_entry.pack(pady=5)

        self.address_entry = ctk.CTkEntry(self, placeholder_text="Adresiniz")
        self.address_entry.pack(pady=5)

        # Calendar for selecting birthdate
        cal_label = ctk.CTkLabel(self, text="Doğum Tarihinizi Seçiniz")
        cal_label.pack(pady=5)
        bugun = datetime.now()
        onsekiz_yil_once = bugun - timedelta(days=18*365)
        max_tarih = onsekiz_yil_once.date()   # Maximum selectable date
        self.cal = Calendar(self, selectmode='day', year=max_tarih.year, month=max_tarih.month, day=max_tarih.day, maxdate=max_tarih, background="#2B2B2B", headersbackground="#3C3F41", headersforeground="#D3D3D3", normalbackground="#414141", normalforeground="#FFFFFF", weekendbackground="#414141", weekendforeground="#FFFFFF", othermonthbackground="#4F4F4F", othermonthforeground="#E0E0E0", selectbackground="#4E92F9", selectforeground="#FFFFFF", disableddaybackground="#343434",disableddayforeground="#6F6F6F")
        self.cal.pack(pady=5)

        self.feedback_label = ctk.CTkLabel(self, text="", text_color="#FF0000")
        self.feedback_label.pack(pady=5)

        register_button = ctk.CTkButton(self, text="Kayıt Ol", command=self.register_user)
        register_button.pack(pady=10)

    def register_user(self):
        # Get values from input fields
        username = self.username_entry.get()
        password = self.pass_entry.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        mail = self.mail_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()
        selected_date = self.cal.get_date()  # Selected date from the calendar

        # Check input fields, none of them can be empty.
        if not all([username, password, name, surname, mail, phone, address, selected_date]):
            print("Hata")
            self.feedback_label.configure(text="╰（‵□′）╯ Herhangi Bir Alan Boş Bırakılamaz ╰（‵□′）╯")
            return

        # SQL query to insert user
        query = """INSERT INTO users VALUES (nextval('users_seq'), %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        record = (username,password,name,surname,selected_date,mail,phone,address)

        cur.execute(query,record)
        conn.commit()

        # Close the registration window 
        self.destroy()

class update_user(ctk.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        global global_userid
        
        self.user_id = global_userid
        cur.execute("""SELECT email, phonenumber, address
                       FROM users WHERE userid = %s""",(global_userid,))
        
        self.personal_info = cur.fetchone()
        
        # screen adjustments and geometry set
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 800
        height = 800
        
        # Calculate x and y coordinates
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        
        # Set the window's position
        self.geometry(f'{width}x{height}+{x}+{y}')

        mainlabel = ctk.CTkLabel(self, text="Profil Güncelle", font=("Helvetica", 30, "bold"))
        mainlabel.pack(pady=(10, 20))
        
        # Frame for updating password
        pass_frame = ctk.CTkFrame(self)
        self.pass_entry = ctk.CTkEntry(pass_frame, placeholder_text="Şifreniz")
        self.pass_entry.pack(pady=5, side = "left")
        ctk.CTkButton(pass_frame, text="Güncelle", width=70, command=self.update_pass).pack(side = "right", padx=5)
        pass_frame.pack()
        
        # Frame for updating email
        mail_frame = ctk.CTkFrame(self)
        self.mail_entry = ctk.CTkEntry(mail_frame, placeholder_text=f"{self.personal_info[0]}")
        self.mail_entry.pack(pady=5, side = "left")
        ctk.CTkButton(mail_frame, text="Güncelle", width=70, command=self.update_mail).pack(side = "right", padx=5)
        mail_frame.pack()
        
        # Frame for updating phone number
        phone_frame = ctk.CTkFrame(self)
        self.phone_entry = ctk.CTkEntry(phone_frame, placeholder_text=f"{self.personal_info[1]}")
        self.phone_entry.pack(pady=5, side = "left")
        ctk.CTkButton(phone_frame, text="Güncelle", width=70, command=self.update_phone).pack(side = "right", padx=5)
        phone_frame.pack()
        
        # Frame for updating address
        address_frame = ctk.CTkFrame(self)
        self.address_entry = ctk.CTkEntry(address_frame, placeholder_text=f"{self.personal_info[2]}")
        self.address_entry.pack(pady=5, side = "left")
        ctk.CTkButton(address_frame, text="Güncelle", width=70, command=self.update_address).pack(side = "right", padx=5)
        address_frame.pack()
        
        self.feedback_label = ctk.CTkLabel(self, text="", text_color="#FF0000")
        self.feedback_label.pack(pady=5)
        
        # Button for adding a new product
        ctk.CTkButton(self, text=" + Ürün Ekle \^o^/", width=70).pack(pady=10)
        
        self.urun_ekle_window = None 
     

    def urun_eklerim(self):
        # Open the window for adding a product
        if self.urun_ekle_window is None or not self.urun_ekle_window.winfo_exists():
            self.urun_ekle_window = urun_eklerim_window(self)
            self.urun_ekle_window.focus_set() 
            self.urun_ekle_window.grab_set()
            self.wait_window(self.urun_ekle_window)
        else:
            self.urun_ekle_window.focus()
        pass
    
    # Update the user's password
    def update_pass(self):
        password = self.pass_entry.get()
        if not password:
            self.feedback_label.configure(text="╰（‵□′）╯ Alan Boş Bırakılamaz ╰（‵□′）╯")
            return
        
        cur.execute("""UPDATE users SET password = %s where users.userid = %s""",(password, self.user_id))
        conn.commit()
        self.feedback_label.configure(text="Şifre Güncellendi")
    
    # Update the user's phone number
    def update_phone(self):
        phone = self.phone_entry.get()
        if not phone:
            self.feedback_label.configure(text="╰（‵□′）╯ Alan Boş Bırakılamaz ╰（‵□′）╯")
            return
        
        cur.execute("""UPDATE users SET phonenumber = %s where users.userid = %s""",(phone, self.user_id))
        conn.commit()
        self.feedback_label.configure(text="Telefon No. Güncellendi")
    
    # Update the user's email
    def update_mail(self):
        mail = self.mail_entry.get()
        if not mail:
            self.feedback_label.configure(text="╰（‵□′）╯ Alan Boş Bırakılamaz ╰（‵□′）╯")
            return
        
        cur.execute("""UPDATE users SET email = %s where users.userid = %s""",(mail, self.user_id))
        conn.commit()
        self.feedback_label.configure(text="Mail Güncellendi")
    
    # Update the user's address
    def update_address(self):
        address = self.address_entry.get()
        if not address:
            self.feedback_label.configure(text="╰（‵□′）╯ Alan Boş Bırakılamaz ╰（‵□′）╯")
            return
        
        cur.execute("""UPDATE users SET address = %s where users.userid = %s""",(address, self.user_id))
        conn.commit()
        self.feedback_label.configure(text="Adres Güncellendi")

class sepet_window(ctk.CTkToplevel):
    def __init__(self, parent, product_list, refresh, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.refresh = refresh
        # screen adjustments and geometry set
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 800
        height = 800
        
        # Calculate x and y coordinates
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        
        # Set the window's position
        self.geometry(f'{width}x{height}+{x}+{y}')

        # product = [prod_name, prod_id, price, quantity, total]
        product_list_all = []

        #Lists the products added to the basket in the product list
        for prod_id in product_list:
            flag = False
            for i, product in enumerate(product_list_all):
                if product[1] == prod_id:
                    flag = True
                    new_product = list(product)
                    new_product[3] += 1

                    cur.execute("""SELECT calculatetotalamount(%s,%s)""",(new_product[1], new_product[3]))
                    total_price = cur.fetchone()
                    
                    new_product[4] = total_price[0]

                    product_list_all[i] = new_product
                    break
            if not flag:
                cur.execute("""SELECT p.productname, p.productid, p.price FROM products p WHERE %s = p.productid""", (prod_id,))
                new_prod = cur.fetchone()
                if new_prod:
                    new_prod = list(new_prod) + [1] + [new_prod[2]]
                    product_list_all.append(new_prod)        

        # Create a scrollable frame for displaying the products
        main = ctk.CTkScrollableFrame(self, 
                                               border_width=0, 
                                               border_color="#242424", 
                                               height=450,
                                               width=1000,
                                               label_text="Sepet",
                                               label_anchor="center",
                                               label_font=("Helvetica", 20, "bold"))
        main.pack()
        
        # Display each product in the scrollable frame
        for i, product in enumerate(product_list_all):
            ctk.CTkLabel(main, text="-" + " "
                         + str(product[3]) + "x | " 
                         + str(product[0]) + " - " 
                         + str(product[4]),
                         font=("Helvetica", 16), anchor='w').pack(pady=10)
        self.buy_button = ctk.CTkButton(self, text="Alışverişi Tamamla", command = lambda: self.buy_products(product_list_all))
        self.buy_button.pack(pady=10, padx=10, side="right")
        info_label = ctk.CTkLabel(self, text="Alışverişleriniz Otomatik Olarak Kaydedilmektedir.")
        info_label.pack(padx=10, side="left")
        
        self.info_pop = None    
        
    def buy_products(self, product_list_all):
        global global_userid
        
        # Save the purchase in the database
        for product in product_list_all:
            cur.execute("""INSERT INTO sales (saleid, userid, productid, quantity, totalamount) 
                                        VALUES (nextval('sales_seq'), %s, %s, %s, %s)""",
                                        (global_userid, product[1], product[3], product[4]))
            
            cur.execute("""UPDATE products 
                           SET stockquantity = stockquantity - %s 
                           WHERE productid = %s""",(product[3], product[1],))
        
        if self.info_pop is None or not self.info_pop.winfo_exists():
            self.info_pop = info_popup(self)
            self.info_pop.focus_set() 
            self.info_pop.grab_set()
            self.wait_window(self.info_pop)
        else:
            self.info_pop.focus()
            
        # Save database changes
        conn.commit()
        self.refresh()
        self.destroy()
        
class info_popup(ctk.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Screen adjustments and geometry set
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 400
        height = 100
        
        # Calculate x and y coordinates
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        
        # Set the window's position
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Display label indicating that the purchase trigger is working
        ctk.CTkLabel(self, text="Satın Alıma Ait Trigger Çalışmıştır.").pack()

class urun_eklerim_window(ctk.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 200
        height = 200
        
        # Calculate x and y coordinates
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        
        # Set the window's position
        self.geometry(f'{width}x{height}+{x}+{y}')
    
class satin_alinan_window(ctk.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        
        # screen adjustments and geometry set
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 1000
        height = 800
        
        # Calculate x and y coordinates
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        
        # Set the window's position
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both")
        
        self.hata_label = ctk.CTkLabel(self.main_frame, text="", text_color="#FF0000")
        self.hata_label.pack()
        
        # SQL query to fetch user's purchases
        global global_userid
        cur.execute("""SELECT p.productname, s.purchasedate, s.quantity, s.totalamount, s.saleid
                       FROM sales s, products p 
                       WHERE p.productid = s.productid AND %s = s.userid""", (global_userid,))
        
        
        sales_list = cur.fetchall()
        
        if sales_list == []:
            self.hata_label.configure(text="＞﹏＜ Alışveriş Listeniz Boş.. ＞﹏＜")
        else:
             # Scrollable frame for displaying purchases
            self.main = ctk.CTkScrollableFrame(self.main_frame, 
                                               border_width=1, 
                                               border_color="#242424", 
                                               height=450,
                                               width=1000,
                                               label_text="Satın Alınan Ürünler",
                                               label_anchor="w",
                                               label_font=("Helvetica", 20, "bold"))
            self.main.pack()
            
            # Iterate over each purchased product
            for product in sales_list:
                label_frame = ctk.CTkFrame(self.main)
                label_frame.pack(pady=10, padx=10, fill="x")
                p_saleid = product[4]
                
                # Delete button for removing the purchase
                ctk.CTkButton(label_frame, width=27, text="X", fg_color="#AA0000", command= lambda sale_id=p_saleid: self.delete_kayit(sale_id)).pack(side = "left", padx=4)
                
                # Label displaying purchase details 
                ctk.CTkLabel(label_frame, text="-" + " "
                         + str(product[1]) + " | " 
                         + str(product[0]) + " x" 
                         + str(product[2]) + " = "
                         + str(product[3]) + "TL",
                         font=("Helvetica", 12, "bold"), anchor='w').pack(pady=10, side="left")
                
                # Combobox to select a rating
                self.combobox = ctk.CTkComboBox(label_frame, width=70, values=["1", "2", "3", "4", "5"])
                self.combobox.pack(side = "right", padx=4)
                
                # Rating button
                rate_button = ctk.CTkButton(label_frame, width=70, text="Değerlendir", fg_color="#007700", 
                                            command=lambda cb=self.combobox: self.insert_rate(p_saleid, cb.get()))
                rate_button.pack(side="right", padx=4)
                
        buy_button = ctk.CTkButton(self, text="Kapat", command=self.close_win)
        buy_button.pack(pady=10, padx=10, side="bottom")

    def close_win(self):
        self.destroy()
                
    def delete_kayit(self, sale_id):
        #Delete a purchase record.
        cur.execute("""DELETE FROM sales 
                    WHERE saleid = %s""", (sale_id,))
        conn.commit()
        
        # Refresh the window to update the display
        self.destroy()
        self.__init__(self.parent)
        self.hata_label.configure(text="Ürüne ait yorum silindi (Trigger)\n")
    
    def insert_rate(self, sale_id, rate):
        print(str(rate) + " " + str(sale_id))
        
        # Call the 'update_or_insert_comment' function in the database
        cur.callproc('update_or_insert_comment',(sale_id,int(rate)))

        conn.commit()
    
class ProductBox(ctk.CTkFrame):
    def __init__(self, parent, product_id, product_name, information, price, category, stock, seller_id, update_sepet_label, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.update_sepet_label = update_sepet_label
        self.stock = stock
        
        cur.execute(""" SELECT u.name, u.surname
                        FROM users u
                        WHERE %s = u.userid""", (seller_id,))

        seller_name = cur.fetchone()
        
        self.pack_propagate(False)  # Prevents the frame from shrinking to fit its contents
        self.configure(width=300, height=280)  # Set the size for each product box
        self.pd_id = product_id
        
        cur.execute("""SELECT s.productid, avg(rate)
                       FROM sales s,comments c
                       WHERE s.saleid = c.saleid AND s.productid = %s
                       GROUP BY s.productid""",(product_id,))
        
        avg_rate_table = cur.fetchone()

        if avg_rate_table == None:
            avg_rate = 0
        else:
            avg_rate = avg_rate_table[1]
            
        rate_str = self.adjust_rate(avg_rate)

        ctk.CTkLabel(self, text=product_name, font=("Helvetica", 14, "bold"), wraplength=280).pack(pady=(1), fill="x")
        ctk.CTkLabel(self, text=information, font=("Helvetica", 10, "bold"), anchor="w", wraplength=280).pack(pady=(1), padx=7, fill="x")
        ctk.CTkLabel(self, text=f"Kategori: {category}", font=("Helvetica", 10), anchor="w").pack(pady=(1), padx=7, fill="x")
        
        self.stock_label = ctk.CTkLabel(self, text=f"Stok: {stock}", font=("Helvetica", 10), anchor="w")
        self.stock_label.pack(pady=(1), padx=7, fill="x")
        
        ctk.CTkLabel(self, text=f"Satıcı: {seller_name[0]} {seller_name[1]}", font=("Helvetica", 10), anchor="w").pack(pady=(1), padx=7, fill="x")
        ctk.CTkLabel(self, text=f"{price} ₺", font=("Helvetica", 18, "bold"), anchor="w").pack(pady=(5), padx=7, fill="x")
      
        ctk.CTkLabel(self, text=rate_str, font=("Helvetica", 14, "bold")).pack(pady=(5), padx=7, fill="x")
        self.sepete_ekle_button = ctk.CTkButton(self, text="Sepete Ekle", font=("Helvetica", 14, "bold"), command=self.add_to_basket)
        self.sepete_ekle_button.pack(pady=(0, 10))
        
        if stock == 0:
            self.stock_label.configure(text="Stok Yok.")
            self.sepete_ekle_button.configure(state = "disabled")
            
    def adjust_rate(self, avg_rate):
        # Adjust the displayed rating based on the average rate
        avg_rate_rounded = round(avg_rate)
        
        if avg_rate == 0:
            return "☆☆☆☆☆ | 0/5"
        else:
            avg_str = ""
            for i in range(0, avg_rate_rounded):
                avg_str += "★"
            for i in range(0, 5-avg_rate_rounded):
                avg_str += "☆"
            
            if avg_rate % 1 == 0:
                avg_rate = int(avg_rate)

            avg_str += " | " + str(round(avg_rate, 1)) + "/5"
            return avg_str


    def add_to_basket(self):
        # Function to handle adding the product to the basket
        if self.stock > 0 :
            # If there is stock available
            self.stock -= 1 # Decrease the stock count
            self.stock_label.configure(text=f"Stok: {self.stock}") # Update the stock label
            self.update_sepet_label(self.pd_id) # Update the basket label
            if self.stock==0:
                # If stock is now zero, disable the button and update its text
                self.sepete_ekle_button.configure(state = "disabled", text="Stok Yok")
        else:
            self.stock_label.configure(text="Stok = 0")      

# Run the application
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
