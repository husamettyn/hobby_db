import tkinter as tk
import customtkinter as ctk
from tkcalendar import Calendar
from datetime import datetime, timedelta
import psycopg2

conn = psycopg2.connect(host = "localhost", port = "5432", database = "hobby_db", user = "postgres", password = "123")
cur = conn.cursor()

global_username = ""
global_userid = 0

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
        self.homepage = Homepage(self)
        self.homepage.pack()
        self.login_screen.destroy()

class Homepage(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        global global_username
        
        user_name = ctk.CTkLabel(self, width=100, text="Hoşgeldin " + global_username, font=("Helvetica", 20, "bold"))
        user_name.pack(pady=10)

        search_bar = ctk.CTkEntry(self, width=200, placeholder_text="Ara")
        search_bar.pack(pady=10)

        # Scrollable container setup
        product_boxes = ctk.CTkScrollableFrame(self, 
                                               border_width=1, 
                                               border_color="#242424", 
                                               height=350,
                                               width=300,
                                               label_text="Ürünler",
                                               label_anchor="center",
                                               label_font=("Helvetica", 20, "bold"))
        product_boxes.pack(pady=10, padx=20)

        # Example product data - you would load this from a database or some other data source
        cur.execute(""" SELECT * FROM products""")
        product_table = cur.fetchall()
        
        # Add product boxes to the grid
        for product in product_table:
            ProductBox(product_boxes, product[0], product[2], product[3], product[5], product[4], product[6], product[1], self.update_sepet_label).pack(pady=10)
                                      #product_id, product_name, information, price, category, stock, seller_id,

        self.counter = 0
        self.product_list = []
        
        self.sepet_hata = ctk.CTkLabel(self, text="", text_color="#FF0000").pack()
        
        self.sepet = ctk.CTkButton(self, text="Sepet", command=self.open_sepet)
        self.sepet.pack(pady=10, padx=10, side="right")
        
        self.satin_alinan = ctk.CTkButton(self, text="Satın Alınanlar", command=self.open_satin_alinanlar)
        self.satin_alinan.pack(pady=10, padx=10, side="left")
        
        self.sepet_win = None
        self.satin_alinan_win = None

    def open_satin_alinanlar(self):
        if self.sepet_win is None or not self.sepet_win.winfo_exists():
            self.sepet_win = satin_alinan_window(self)  # create window if its None or destroyed
            self.sepet_win.focus_set()  # Yeni pencereye odaklanmayı zorla
            self.sepet_win.grab_set()
            self.wait_window(self.sepet_win)
        else:
            self.sepet_win.focus()  # if window exists focus it
    
    def open_sepet(self):
        if self.product_list == []:
            self.sepet.configure(text="Sepetiniz Boş")
            
        else:
            if self.sepet_win is None or not self.sepet_win.winfo_exists():
                self.sepet_win = sepet_window(self, self.product_list, self.refresh_homepage)
                self.sepet_win.focus_set() 
                self.sepet_win.grab_set()
                self.wait_window(self.sepet_win)
            else:
                self.sepet_win.focus()

    def update_sepet_label(self, product):
        self.counter += 1
        self.product_list.append(product)
        self.sepet.configure(text=f"Sepet: {self.counter}")
        # basılan tuştan gelen veriye göre product isimleri bir listede saklanmalı
        
    def refresh_homepage(self):
        # Ürün listesini ve sepet sayacını sıfırla
        self.product_list = []
        self.counter = 0
        self.sepet.configure(text="Sepet")

class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, on_login_success, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.on_login_success = on_login_success

        mainlabel = ctk.CTkLabel(self, text="Hobi Pazarı", font=("Helvetica", 30, "bold"))
        mainlabel.pack(pady=(50, 20), padx=(100,100))

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Kullanıcı Adı")
        self.username_entry.pack(pady=(20, 20))

        self.password_entry = ctk.CTkEntry(self, show="*", placeholder_text="Şifre")
        self.password_entry.pack(pady=(0, 10))


        login_button = ctk.CTkButton(self, text="Giriş Yap",  command=lambda: self.on_login_click(self.hata_label))
        login_button.pack()

        register_button = ctk.CTkButton(self, text="Kaydol", fg_color="transparent", border_color="#565b5e", border_width=2, command=self.on_register_click)
        register_button.pack(pady=(20, 20))

        self.hata_label = ctk.CTkLabel(self, text="", font=("Helvetica", 12), text_color="#FF0000")
        self.hata_label.pack(pady=(0,10))
        
        self.register_window = None

    def on_register_click(self):
        if self.register_window is None or not self.register_window.winfo_exists():
            self.register_window = register(self)  # create window if its None or destroyed
            self.register_window.focus_set()  # Yeni pencereye odaklanmayı zorla
            self.register_window.grab_set()
            self.wait_window(self.register_window)
        else:
            self.register_window.focus()  # if window exists focus it

    def on_login_click(self, hata):
        # Here, add the actual login logic
        global global_username
        global global_userid
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        cur.execute(""" SELECT username, password, userid FROM users 
                        WHERE username = %s AND password = %s""", (username,password))
        
        info = cur.fetchone()
        
        print(info)
        if info == None:
            hata.configure(text="Geçersiz Kullanıcı Adı veya Şifre")
        else:
            global_username = username
            global_userid = info[2]
            self.on_login_success()  # Call the method to switch to the homepage

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

        self.phone_entry = ctk.CTkEntry(self, placeholder_text="Telefon Numaranız (+905XXxxxXXXxxXX)", width=250)
        self.phone_entry.pack(pady=5)

        self.address_entry = ctk.CTkEntry(self, placeholder_text="Adresiniz")
        self.address_entry.pack(pady=5)

        cal_label = ctk.CTkLabel(self, text="Doğum Tarihinizi Seçiniz")
        cal_label.pack(pady=5)
        bugun = datetime.now()
        onsekiz_yil_once = bugun - timedelta(days=18*365)
        max_tarih = onsekiz_yil_once.date()  # Maksimum seçilebilecek tarih
        self.cal = Calendar(self, 
               selectmode='day',
               year=max_tarih.year,
               month=max_tarih.month,
               day=max_tarih.day,
               maxdate=max_tarih,
               background="#2B2B2B",  # Koyu arka plan
               headersbackground="#3C3F41",  # Başlık arka planı
               headersforeground="#D3D3D3",  # Başlık yazı rengi
               normalbackground="#414141",  # Normal günlerin arka planı
               normalforeground="#FFFFFF",  # Normal günlerin yazı rengi
               weekendbackground="#414141",  # Hafta sonu arka planı
               weekendforeground="#FFFFFF",  # Hafta sonu yazı rengi
               othermonthbackground="#4F4F4F",
               othermonthforeground="#E0E0E0",
               selectbackground="#4E92F9",  # Seçilen günün arka planı
               selectforeground="#FFFFFF",  # Seçilen günün yazı rengi
               disableddaybackground="#343434",  # Engellenmiş günlerin arka planı
               disableddayforeground="#6F6F6F")  # Engellenmiş günlerin yazı rengi
        self.cal.pack(pady=5)

        self.feedback_label = ctk.CTkLabel(self, text="", text_color="#FF0000")
        self.feedback_label.pack(pady=5)

        register_button = ctk.CTkButton(self, text="Kayıt Ol", command=self.register_user)
        register_button.pack(pady=10)

    def register_user(self):
        # Giriş alanlarının değerlerini al
        username = self.username_entry.get()
        password = self.pass_entry.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        mail = self.mail_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()
        selected_date = self.cal.get_date()  # Takvimden seçilen tarih

        # Giriş alanlarını kontrol et, herhangi birisi boş olamaz.
        if not all([username, password, name, surname, mail, phone, address, selected_date]):
            print("Hata")
            self.feedback_label.configure(text="Herhangi Bir Alan Boş Bırakılamaz")
            return

        # Eğer tüm alanlar doluysa, bilgileri yazdır

        # DONE buraya SQL sorgusu geldi.
        query = """INSERT INTO users VALUES (DEFAULT, 
                                                %s, 
                                                %s, 
                                                %s, 
                                                %s, 
                                                %s, 
                                                %s, 
                                                %s, 
                                                %s) """
        
        record = (username,password,name,surname,selected_date,mail,phone,address)

        cur.execute(query,record)
        conn.commit()

        self.destroy()
        
# yorumlar kısmını eklemek lazım.
class sepet_window(ctk.CTkToplevel):
    def __init__(self, parent, product_list, refresh, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.refreh = refresh
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

        ## yusuf burayı hallet
        # product = [prod_name, prod_id, price, quantity, total]
        product_list_all = []

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

        for i, product in enumerate(product_list_all):
            ctk.CTkLabel(self, text="-" + " "
                         + str(product[3]) + "x | " 
                         + str(product[0]) + " - " 
                         + str(product[4]),
                         font=("Helvetica", 16), anchor='w').pack(pady=10)
        buy_button = ctk.CTkButton(self, text="Alışverişi Tamamla", command = lambda: self.buy_products(product_list_all))
        buy_button.pack(pady=10, padx=10, side="right")
            
    def buy_products(self, product_list_all):
        global global_userid
        # Satın alma işlemini veritabanında kaydetme
    
        for product in product_list_all:
            # Örnek bir SQL sorgusu, burada 'purchases' tablosu ve sütunlar varsayılan olarak belirlenmiştir.
            cur.execute("""INSERT INTO sales (userid, productid, quantity, totalamount) VALUES (%s, %s, %s, %s)""",
                        (global_userid, product[1], product[3], product[4]))
        
        # Veritabanı değişikliklerini kaydet
        conn.commit()
        self.refreh()
        self.destroy()
        

class satin_alinan_window(ctk.CTkToplevel):
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
        
        # TODO product_list'e SQL'den satin alinan ürünler çekilecek.
        # if else yapısıyla 
        hata_label = ctk.CTkLabel(self, text="", text_color="#FF0000")
        hata_label.pack(pady=10, padx=10)
        
        product_list = []
        if product_list == []:
            hata_label.configure(text="Boş Liste")
        else:
            for i, product in enumerate(product_list):
                ctk.CTkLabel(self, text=str(i) + ". " + str(product), font=("Helvetica", 16)).pack(pady=10)
                
        buy_button = ctk.CTkButton(self, text="Kapat", command=self.close_win)
        buy_button.pack(pady=10, padx=10, side="bottom")
    def close_win(self):
        self.destroy()
                
class ProductBox(ctk.CTkFrame):
    def __init__(self, parent, product_id, product_name, information, price, category, stock, seller_id, update_sepet_label, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.update_sepet_label = update_sepet_label

        
        cur.execute(""" SELECT u.name, u.surname
                        FROM users u
                        WHERE %s = u.userid""", (seller_id,))

        seller_name = cur.fetchone()
        
        self.pack_propagate(False)  # Prevents the frame from shrinking to fit its contents
        self.configure(width=300, height=300)  # Set the size for each product box
        self.pd_id = product_id
        
        ctk.CTkLabel(self, text=product_name, font=("Helvetica", 14, "bold")).pack(pady=(1))
        ctk.CTkLabel(self, text=information, font=("Helvetica", 10, "bold")).pack(pady=(1))
        ctk.CTkLabel(self, text=f"Category: {category}", font=("Helvetica", 10)).pack(pady=(1))
        ctk.CTkLabel(self, text=f"Stock: {stock}", font=("Helvetica", 10)).pack(pady=(1))
        ctk.CTkLabel(self, text=f"Seller: {seller_name[0]} {seller_name[1]}", font=("Helvetica", 10)).pack(pady=(1))
        ctk.CTkLabel(self, text=f"Price: {price}", font=("Helvetica", 12, "bold")).pack(pady=(10))
        
        # stock yoksa alttaki butonu disable et
        ctk.CTkButton(self, text="Add to Basket", command=self.add_to_basket).pack(pady=(0, 10))
        ctk.CTkButton(self, text="Yorumlar", fg_color="transparent", border_color="#565b5e", border_width=2).pack(pady=(0, 10))

    def add_to_basket(self):
        self.update_sepet_label(self.pd_id)


# Run the application
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
