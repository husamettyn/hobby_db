import tkinter as tk
import customtkinter as ctk
from tkcalendar import Calendar
from datetime import datetime, timedelta

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
        self.login_screen.pack_forget()  # Hide the login screen
        self.homepage = Homepage(self)
        self.homepage.pack()

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

        self.hata_label = ctk.CTkLabel(self, text="", font=("Helvetica", 12), text_color="#FF0000")
        self.hata_label.pack(pady=(0,10))

        login_button = ctk.CTkButton(self, text="Giriş Yap",  command=lambda: self.on_login_click(self.hata_label))
        login_button.pack()

        register_button = ctk.CTkButton(self, text="Üye Ol", fg_color="transparent", border_color="#FFFFFF", border_width=2, command=self.on_register_click)
        register_button.pack(pady=(20, 20))

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
        self.on_login_success()  # Call the method to switch to the homepage
        # if self.username_entry.get() == "admin" and self.password_entry.get() == "admin":
        #     self.on_login_success()  # Call the method to switch to the homepage
        # else:
        #     hata.configure(text="Geçersiz Kullanıcı Adı ve Şifre")

    

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

        mainlabel = ctk.CTkLabel(self, text="Kayıt Ol", font=("Helvetica", 30, "bold"))
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

        # buraya SQL sorgusu gelecek. 
        print("Kullanıcı Adı:", username)
        print("Şifre:", password)
        print("Ad:", name)
        print("Soyad:", surname)
        print("E-posta:", mail)
        print("Telefon:", phone)
        print("Adres:", address)
        print("Doğum Tarihi:", selected_date)

        self.destroy()

class Homepage(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        user_name = ctk.CTkLabel(self, width=100, text="Kullanıcı Adı", font=("Helvetica", 20, "bold"))
        user_name.pack(pady=10)

        search_bar = ctk.CTkEntry(self, width=200, placeholder_text="Ara")
        search_bar.pack(pady=10)

        # Scrollable container setup
        product_boxes = ctk.CTkScrollableFrame(self, 
                                               border_width=1, 
                                               border_color="#242424", 
                                               height=300,
                                               width=300,
                                               label_text="Ürünler",
                                               label_anchor="center",
                                               label_font=("Helvetica", 20, "bold"))
        product_boxes.pack(pady=10, padx=20)

        # Example product data - you would load this from a database or some other data source
        products = [
            {"name": "Product 1", "info": "Info 1", "price": "10$"},
            {"name": "Product 2", "info": "Info 2", "price": "20$"},
            {"name": "Product 1", "info": "Info 1", "price": "10$"},
            {"name": "Product 2", "info": "Info 2", "price": "20$"},
            {"name": "Product 1", "info": "Info 1", "price": "10$"},
            {"name": "Product 2", "info": "Info 2", "price": "20$"},
            {"name": "Product 1", "info": "Info 1", "price": "10$"},
            {"name": "Product 2", "info": "Info 2", "price": "20$"},
        ]

        # Add product boxes to the grid
        for i, product in enumerate(products):
            ProductBox(product_boxes, product['name'], product['info'], product['price'], self.update_sepet_label).pack(pady=10)

        self.counter = 0
        self.product_list = []
        self.sepet = ctk.CTkButton(self, text="Sepet", command=self.open_sepet)
        self.sepet.pack(pady=10, padx=10, side="right")

    def open_sepet():
        print("sepet açıldı")

        # new_window = ctk.CTkToplevel(self)
        # new_window.title("Sepet")
        # new_window.geometry("500x200")
        
        # for product_name in self.product_list:
        #     ctk.CTkLabel(self, text=product_name).pack()

        # # Close button
        # close_button = ctk.CTkButton(self, text="Close", command=self.destroy)
        # close_button.pack(pady=10)

    def update_sepet_label(self, product_id):
        self.counter += 1
        self.product_list.append(product_id)
        self.sepet.configure(text=f"Sepet: {self.counter}")
        # basılan tuştan gelen veriye göre product isimleri bir listede saklanmalı

# yorumlar kısmını eklemek lazım.
        

                
class ProductBox(ctk.CTkFrame):
    def __init__(self, parent, product_name, information, price, update_sepet_label, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.update_sepet_label = update_sepet_label

        self.pack_propagate(False)  # Prevents the frame from shrinking to fit its contents
        self.configure(width=200, height=200)  # Set the size for each product box

        ctk.CTkLabel(self, text=product_name, font=("Helvetica", 14, "bold")).pack(pady=(10, 5))
        ctk.CTkLabel(self, text=information, font=("Helvetica", 10)).pack(pady=(0, 5))
        ctk.CTkLabel(self, text=f"Price: {price}", font=("Helvetica", 12, "bold")).pack(pady=(5, 10))
        ctk.CTkButton(self, text="Add to Basket", command=self.add_to_basket).pack(pady=(0, 10))
        ctk.CTkButton(self, text="Yorumlıar", bg_color="transparent").pack(pady=(0, 10))

    def add_to_basket(self):
        product_name = self.children['!ctklabel'].cget("text")  # Get the product name
        self.update_sepet_label(product_name)


# Run the application
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
