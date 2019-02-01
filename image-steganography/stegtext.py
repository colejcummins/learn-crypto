# Auth: Cole Cummins

import Image

# ---Image to Text Encoder---
# Saves one bit of a letter in each r, g, b value sequencially, meaning that
# it takes 8 bytes of an image to save one byte of text, very little information
# is lost

# main method, parses user input and redirects to encode or decode
def main():
    cmd = input("Please enter a function (d)ecrypt or (e)ncrypt: ")
    while cmd not in ["d", "e", "decrypt", "encrypt"]:
        cmd = input("Not a valid input\nPlease enter a function: ")
    fname = input("Please enter the full name of an image: ")
    im_arr = get_bit_arr(fname)
    if cmd in ["e", "encrypt"]:
        steg_enc(fname, im_arr)
    else:
        print(steg_dec(im_arr))


# Encrypts a message into an image one bit at a time. Uses a mask and clears
# the LSB of each byte, ORing that with one bit in the message, stores character
# from MSB to LSB
def steg_enc(fname, im_arr):
    msg = input("Input a message to be encrypted into the image: ")
    mask = 0
    for i in range(len(msg) * 8):
        if mask == 0:
            mask = 128
        stor = mask & ord(msg[i // 8])
        stor = stor >> (7 - (i % 8))
        im_arr[i + 54] = (im_arr[i + 54] & 254) | stor
        mask = mask >> 1
    with open(fname[0:-4] + "2" + fname[-4:], "wb") as wf:
        wf.write(im_arr)


# decodes a file by starting at the first pixel and stopping when a character
# is read that is no longer printable, ie random noise
def steg_dec(im_arr):
    msg = ""
    c = 0
    for i in range(54, len(im_arr)):
        c = c << 1
        c += im_arr[i] % 2
        if (i - 54) % 8 == 7: 
            if c < 32 or c > 126: 
                break
            msg += chr(c)
            c = 0
    return msg


# checks if valid file name was entered by the user, asks for file again if not
def get_bit_arr(fname):
    try:
        with open(fname, "rb") as in_im:
            im_dat = in_im.read()
        bit_arr = bytearray(im_dat)
    except FileNotFoundError:
        fname = input("***FILE NOT FOUND***\nPlease enter an image: ")
        return get_bit_arr(fname)
    else:
        return bit_arr

if __name__ == "__main__":
    main()