import csv
from IPython.display import clear_output


class Password:
    def __init__(self, value, app, user):
        self.value = value
        self.app = app
        self.user = user


class User:
    def __init__(self, mail, user_password, username):
        self.mail = mail
        self.user_password = user_password
        self.username = username


def RegisterUser():
    with open("users.csv", mode="a", newline="") as f:
        writer = csv.writer(f, delimiter=",")

        print("Para registrarte, introduce tus datos: ")
        email = input("Email: ")
        password = input("Contraseña: ")
        password2 = input("Confirmación de contraseña: ")

        clear_output()

        if password == password2:
            writer.writerow([encrypt(email), encrypt(password)])
            print("Te has registrado exitosamente. ¡Bienvenido!")
        else:
            print("Por favor, inténtelo de nuevo.")


def LoginUser():
    print("Para iniciar sesión introduce tus datos")
    email = input("Email: ")
    password = input("Password: ")

    clear_output()

    with open("users.csv", mode="r") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            if row == [encrypt(email), encrypt(password)]:
                print("Has iniciado sesión exitosamente")
                return True
    print("Por favor, revise su correo y contraseña e inténtelo de nuevo.")
    return False


def encrypt(key, data):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    return cipher.nonce + tag + ciphertext


def decrypt(key, data):
    nonce = data[:AES.block_size]
    tag = data[AES.block_size:AES.block_size * 2]
    ciphertext = data[AES.block_size * 2:]

    cipher = AES.new(key, AES.MODE_EAX, nonce)

    return cipher.decrypt_and_verify(ciphertext, tag)


active = True
logged_in = False

while active:
    if logged_in:
        print("1. Cerrar sesión\n2. Cerrar ")
    else:
        print("1. Iniciar sesión\n2. Registrarse\n3. Cerar")

    choice = input("¿Que querrías hacer? ").lower()

    clear_output()

    if choice == "registrarse" and logged_in == False:
        RegisterUser()
    elif choice == "iniciar sesión" and logged_in == False:
        LoginUser()
    elif choice == "cerrar":
        active = False
    elif choice == "cerrar sesión" and logged_in == True:
        logged_in = False
    else:
        print("Por favor, inténtelo de nuevo.")
