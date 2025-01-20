from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import pandas as pd

# Configuración de la clave de cifrado
key = b'HALAMADRIDJOSELU'  # La clave debe tener 16, 24 o 32 bytes para AES

# Función para encriptar datos
def encrypt_data(data: str) -> str:
    """Cifra los datos con AES y los codifica en base64."""
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(encrypted).decode()

# Función para desencriptar datos
def decrypt_data(encrypted_data: str) -> str:
    """Desencripta los datos codificados en base64 y devuelve un string."""
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_bytes = base64.b64decode(encrypted_data)
    decrypted = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
    return decrypted.decode()

# Variables globales
global_email = "user@example.com"
password = "securepassword123"

# Cifrado de las variables
encrypted_email = encrypt_data(global_email)
encrypted_password = encrypt_data(password)

# Guardar los datos cifrados en un archivo CSV
df = pd.DataFrame(data={"User": [encrypted_email], "Password": [encrypted_password]})
df.to_csv("users.csv", mode="a", index=False, header=False, encoding="utf-8")

print("Datos encriptados y guardados correctamente en 'users.csv'.")

# Leer los datos del archivo CSV y desencriptar
df_read = pd.read_csv("users.csv", header=None, names=["User", "Password"])
for index, row in df_read.iterrows():
    try:
        decrypted_email = decrypt_data(row["User"])
        decrypted_password = decrypt_data(row["Password"])
        print(f"Fila {index + 1}:")
        print(f"  Email desencriptado: {decrypted_email}")
        print(f"  Contraseña desencriptada: {decrypted_password}")
    except Exception as e:
        print(f"Error al descifrar la fila {index + 1}: {e}")
