import numpy as np
import cv2
from PIL import Image
import matplotlib.image as img
from os import system as bas


moder = int(256)

#Image to matrix converter
def img_to_colvecls(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
    rows = img.shape[0]
    cols = img.shape[1]
    col_vecls = []
    for i in range(0,rows):
        for j in range(0,cols):
            col_vecls.append(np.array([img[i][j][0], img[i][j][1], img[i][j][2]]))
    
    # impng = Image.fromarray(img, 'RGBA')
    # impng.save("New.png")
    # print(img.shape) #tuple
    # print(type(img[0][0][0]))
    # print(type(img[0][0][1]))
    # print(type(img[0][0][2]))
    # print(type(img[0][0][3]))
    # print(img[150][150])
    return col_vecls

def colvecls_to_img(colvecls, path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
    rows = img.shape[0]
    cols = img.shape[1]
    k = 0
    for i in range(0,rows):
        for j in range(0,cols):
            img[i][j][0] = colvecls[k][0]
            img[i][j][1] = colvecls[k][1]
            img[i][j][2] = colvecls[k][2]
            # img[i][j][3] = 255
            k+=1
    
    return Image.fromarray(img,'RGBA')



def conv_ascii(elm):
    if type(elm) == int:
        return chr(elm+129)
    elif type(elm) == str:
        return ord(elm)-129
    else:
        print("Wierd data type found: ", type(elm))
        bas("pause")

def Key_Generator():
    key_str = "Xenoblast"
    return np.array([conv_ascii(s) for s in key_str]).reshape(3,3)

Key = Key_Generator()


def does_inverse_exist():
    det_key = int(np.linalg.det(Key))%moder
    try:
        inv_mod = pow(det_key, -1, moder)
        # print("Det: ",det_key)
        # print("inv_mod: ",pow(det_key, -1, moder))
    except:
        # print("Det: ",det_key)
        # print("inv_mod: ",pow(det_key, -1, moder))
        return False
    return True


def verify_key_inv(key_inv): #Verify if the result is identity matrix. Then good to go!
    if np.array_equal((Key@key_inv)%moder,np.identity(3)):
        return True
    else:
        return False



def adjointer(matrix):
    mtrx = matrix.ravel()  #ravel() converts 2d array to 1d
    A= +((mtrx[4]*mtrx[8])-(mtrx[5]*mtrx[7]))
    B= -((mtrx[3]*mtrx[8])-(mtrx[5]*mtrx[6]))
    C= +((mtrx[3]*mtrx[7])-(mtrx[6]*mtrx[4]))
    D= -((mtrx[1]*mtrx[8])-(mtrx[2]*mtrx[7]))
    E= +((mtrx[0]*mtrx[8])-(mtrx[2]*mtrx[6]))
    F= -((mtrx[0]*mtrx[7])-(mtrx[1]*mtrx[6]))
    G= +((mtrx[1]*mtrx[5])-(mtrx[2]*mtrx[4]))
    H= -((mtrx[0]*mtrx[5])-(mtrx[2]*mtrx[3]))
    I= +((mtrx[0]*mtrx[4])-(mtrx[1]*mtrx[3]))
    cofactor = np.array([[A, B, C], 
                         [D, E, F], 
                         [G, H, I]])
    adjnt = cofactor.T
    return adjnt #convert back to 2d array + transpose


    
def Key_Inverse():
    det_key = int(np.linalg.det(Key))%moder
    det_inv_mod = pow(det_key, -1, moder)
    adj_key = adjointer(Key)%moder
    key_inv = (det_inv_mod*adj_key)%moder
    return key_inv


def is_key_valid():
    mod_inv = does_inverse_exist()
    key_inv = False #Default value
    if mod_inv:
        key_inv = verify_key_inv(Key_Inverse())
        if key_inv:
            print("Key Verified Successfully!")
            return True
    print("Error: Key failed to get verified :(")
    print("--> Inverse_Mod_Exists: ",mod_inv)
    print("--> Key_Inverse_Exists: ",key_inv)
    print("\nYour Key is not compatible. Please change the key!\n")
    return False


def encrypt(path): #Takes an image and returns an encrypted image
    col_vecls = img_to_colvecls(path)

    encrypted_vecls = []
    for i in col_vecls:
        encrypted_vecls.append((i @ Key)%moder)

    encrypted_img = colvecls_to_img(encrypted_vecls, path)
    encrypted_img.save("encrypted.png")


def decrypt(path):
    col_vecls = img_to_colvecls(path)

    key_inv = Key_Inverse()
    decrypted_vecls = []
    for colvec in col_vecls:
        decrypted_vecls.append((colvec @ key_inv)%moder)

    decrypted_img = colvecls_to_img(decrypted_vecls, path)
    decrypted_img.save("decrypted.png")



if __name__ == "__main__":
    if not is_key_valid():
        pass
    else:
        key_str = ""
        for i in Key.ravel():
            key_str += conv_ascii(int(i))
        print("Key:",key_str)
        def Menu():
            print("-----------Menu----------")
            print("1. Encript image")
            print("2. Decript image")
            print("3. Exit")
            ch= eval(input("Enter choice "))
            return ch
        while True:
            ch = Menu()
            if ch==1:
                encrypt(str(input("Enter Image path: ")))
                print("Encryption Done!")
            elif ch==2:
                decrypt(str(input("Enter Image path: ")))
                print("Decryption Done!")
            else:
                print("exit")
                break