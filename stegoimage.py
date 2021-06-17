"""
Project by:
Mor Gajer - ID: 208394700
Yarin Sagiv - ID: 209502251
Noa Dahan - ID: 208375709
Ofir Ben Zaken - ID: 208839712
"""


import ast
import sys
import numpy as np
import random
from PIL import Image
import rsa

np.set_printoptions(threshold=sys.maxsize)

def Encode(src, message, dest, option, publicKey=None):
    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size // n

    message2 = message
    message += "$t3g0"
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    if req_pixels > total_pixels:
        print("error!!! Need larger file size")
    else:
        index = 0
        if option == '1' or option == '3':
            num_random = random.sample(range(5, 9), 2)
        else:
            num_random = random.sample(range(6, 9), 2)
        if option == '2' or option == '3':
            b_message = rsa.encrypt(message2.encode(), publicKey)
            b_message = str(b_message) + "$t3g0"
            b_message = ''.join([format(ord(i), "08b") for i in b_message])
            req_pixels = len(str(b_message))
            if req_pixels > total_pixels:
                print("error!!! Need larger file size")

        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[num_random[0]:num_random[1]] + b_message[index], 2)
                    index += 1

        array = array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("Image Encoded Successfully")


# decoding function
def Decode(src, option, privateKey):
    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size // n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i + 8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    for i in range(len(hidden_bits)):
        if message[-5:] == "$t3g0":
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if "$t3g0" in message:
        if option == '2' or option == '3':
            privateKey = eval(privateKey)
            message = rsa.decrypt( ast.literal_eval(message[:-5]), privateKey).decode()
            print("Hidden Message:", message)
        else:
            print("Hidden Message:", message[:-5])
    else:
        print("No Hidden Message Found")


if __name__ == "__main__":

    choice = input("""Enter your choice option:
     1 Encode.
     2 Decode.
    """)

    if choice == '1':
        option = input("""Enter your choice what you prefer: 
  1 hide message in two bits from five.
  2 RSA encryption and hide message in two bits from four.
  3 both 1+2 options
""")

        if option != '1' and option != '2' and option != '3':
            print("error!!! Invalid option chosen")
            exit(1)

        src = input("Please enter the name of image (including type, inside your project folder):")
        message = input("Please enter the message that you want to hide:")
        dest = input("enter the new name picture after the encoding")
        dest = dest + ".png"
        print("Encoding...")
        if option != '1':
            publicKey, privateKey = rsa.newkeys(512)
            print("This is your private key:\n" + privateKey.__repr__() + "\nPlease save it for decoding")
            Encode(src, message, dest, option, publicKey)
        else:
            Encode(src, message, dest, option)


    elif choice == '2':
        option = input("""Enter your choice what you prefer: 
    1 message hid without RSA.
    2 message hid with RSA.\n""")
        if option != '1' and option != '2':
            print("error!!! Invalid option chosen")
            exit(1)
        privateKey = ""
        if option == '2':
            privateKey = input("Please enter the private key: ")
        src = input("Please enter the new image name (without type): ")
        src = src + ".png"
        print("Decoding...")
        Decode(src, option, privateKey)

    else:
        print("error!!! Invalid option chosen")
        exit(1)
