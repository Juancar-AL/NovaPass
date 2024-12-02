import classes_interface as cl
import csv


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
