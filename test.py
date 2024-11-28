from Crypto.Cipher import AES


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


texto = b'valen calvo'
clave = b'1640975914205316'
texto_encriptado = encrypt(clave, texto)
texto_original = decrypt(clave, texto_encriptado)
print(texto_encriptado, texto_original)
