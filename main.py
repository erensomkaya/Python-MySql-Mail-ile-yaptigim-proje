import pymysql
import shutil
from datetime import datetime
from smtplib import SMTP_SSL, SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Applikasyon:
    def __init__(self):
        self.myEmail = "" #kendi mail adresin
        self.myPassword = "" #mail şifren
        self.sendTo = "" #göndereceğin mail
        self.dbName= "python" #database adın
        self.dbUsername = "root" #db username
        self.dbPassword = ""#db password
        
        self.conn = pymysql.connect(
            host='localhost', user=self.dbUsername, password=self.dbPassword, db=self.dbName,  charset='utf8mb4') 
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS disk (
            id INT(11) UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL, 
            toplam_alan VARCHAR(30) NOT NULL, 
            kullanilmis_alan VARCHAR(30) NOT NULL, 
            kalan_alan VARCHAR(30) NOT NULL, 
            tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )""")
        self.conn.commit()
        

    def degerleriKaydet(self):
        values = shutil.disk_usage("/")
        toplamAlan = values[0]//(2**30)
        kullanilmisAlan = values[1]//(2**30)
        kalanAlan = values[2]//(2**30)

        sorgu = "INSERT INTO disk (toplam_alan, kullanilmis_alan, kalan_alan) VALUES (%s, %s, %s)"
        degerler = (toplamAlan, kullanilmisAlan, kalanAlan)
        self.cursor.execute(sorgu, degerler)
        self.conn.commit()

    def mailGonder(self):
        self.cursor.execute("SELECT * FROM disk ORDER BY id DESC LIMIT 1")
        datas = self.cursor.fetchall()
        bos = ""

        for data in datas:
            bos += f"<b>{data[4]}</b> Tarihine ait disk verileri <br>"
            bos += f"Toplam: {data[1]} GB <br>"
            bos += f"Kullanılmış: {data[2]} GB <br>"
            bos += f"Kalan: {data[3]} GB <br>"

        message = MIMEMultipart("alternative")
        message["Subject"] = "DİSK DEĞERLERİ" #Mail başlığı
        message["From"] = self.myEmail
        message["To"] = self.sendTo

        html = f"""\
        <html>
        <body>
            <p>{bos}</p>
        </body>
        </html>
        """

        nkasdfgvj = MIMEText(html, "html")
        message.attach(nkasdfgvj)

        #mail = SMTP_SSL("smtp.yandex.com", 465) # yandex için
        mail = SMTP("smtp-mail.outlook.com",587) # outlook için
        mail.ehlo()
        mail.starttls() 
        mail.login(self.myEmail, self.myPassword)
        mail.sendmail(self.myEmail, self.sendTo, f"{message.as_string()}")
        print("BAŞARIYLA GÖNDERİLDİ")


app = Applikasyon()
app.degerleriKaydet()
app.mailGonder()