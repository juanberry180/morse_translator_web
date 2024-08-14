import smtplib

my_email = "juanberry180@gmail.com"
password = "ammu gtdv xngr nfve"

class MessageSend:
    def __init__(self, receiver_email, message_text, name):
        self.receiver_email = receiver_email
        self.message_text = message_text
        self.name = name
        self.sending_email()


    def sending_email(self):
        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs=self.receiver_email, msg=f"Subject:Morse code feedback from {self.name}.\n\n{self.message_text}")