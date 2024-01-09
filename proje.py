import psycopg2

conn = psycopg2.connect(host = "localhost", port = "5432", database = "proje", user = "postgres", password = "123")

cur = conn.cursor()

usrnm = input("Kullanici Adi: ")
passw = input("Sifre: ")

cur.execute(""" SELECT username, password FROM users WHERE username = %s AND password = %s""", (usrnm,passw))


if cur.fetchone() != None:
    print(cur.fetchone)
else:
    print("Kullanici bulunamadi")




conn.commit()

cur.close()
conn.close()

