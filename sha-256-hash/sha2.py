# Auth: Cole Cummins

# ---SHA 2 Hashing Algorithm---
# Modern hashing algorithm, generates a 256 bit hash out of 512 bit chunks. 
# Initially converts original message into binary and extends it to a multiple
# of 512, divides chunk into 32 bit words. 


k = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 
          0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 
          0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 
          0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 
          0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 
          0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 
          0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b, 
          0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 
          0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 
          0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 
          0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

add_v = 4294967296

def main():
    inp = input("Enter an input to generate a hash: ")
    while inp != "quit":
        m_int, num_chunks = padding(inp)
        print("\n---HASH---")
        print(hex(shacipher(m_int, num_chunks)))
        inp = input("Enter an input to generate a hash: ")
    print("Exiting SHA2...")

#pads the original message out with '0' bits until it is a multiple of 512
def padding(message):
    l = len(message)
    final = 0

    #convert the message into bytes and append
    for i in range(l):  
        final <<= 8
        final += ord(message[i])
    l *= 8

    #append a '1' bit
    final <<= 1
    final += 1

    #pad the final message with K '0' bits such that (L + 1 + K + 64) % 512 == 0
    pad_l = 0
    while (pad_l + 1 + l + 64) % 512 != 0:
        pad_l += 1
        final <<= 1

    #append L as a 64 bit integer 
    final <<= 64
    final += l

    #return the final number and number of 512 bit chunks
    num_chunks = (((pad_l + 1 + l + 64)//512) + 1)
    return final, num_chunks

def shacipher(m_int, num_chunks):
    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h4 = 0x510e527f
    h5 = 0x9b05688c
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19
        
    chunk = 0
    for i in range(num_chunks):
        chunk = m_int >> (512 * (num_chunks - i - 1))
        w = get_words(chunk)

        # assign working values for each chunk 
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7

        # compression function loop
        for i in range(64):
            s1 = ri_r(e, 32, 6) ^ ri_r(e, 32, 11) ^ ri_r(e, 32, 25)
            ch = (e & f) ^ (((add_v - 1) ^ e) & g)
            temp1 = (h + s1 + ch + k[i] + w[i]) % add_v 
            s0 = ri_r(a, 32, 2) ^ ri_r(a, 32, 13) ^ ri_r(a, 32, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (s0 + maj) % add_v

            # variable reassignments
            h = g
            g = f
            f = e
            e = (d + temp1) % add_v
            d = c
            c = b
            b = a
            a = (temp1 + temp2) % add_v

        # add the working values to the current hash values for this chunk
        h0 = (h0 + a) % add_v
        h1 = (h1 + b) % add_v
        h2 = (h2 + c) % add_v
        h3 = (h3 + d) % add_v
        h4 = (h4 + e) % add_v
        h5 = (h5 + f) % add_v
        h6 = (h6 + g) % add_v
        h7 = (h7 + h) % add_v

    # append all hash values to generate the digest
    digest = (h0 << 224) + (h1 << 192) + (h2 << 160) + (h3 << 128) + (h4 << 96
             ) + (h5 << 64) + (h6 << 32) + h7

    return digest

    
# returns 64 32-bit number array of words including original message
def get_words(chunk):
    mask = 4294967295 << (15 * 32) 
    ws = [0x00000000] * 64

    # copy chunk into the first 16 indexs of the words array
    for i in range(16):
        ws[i] = (mask & chunk) >> (32 * (15 - i))
        mask >>= 32

    # Extends the first 16 words into the remaining 48 words
    for i in range(16, 64):
        s0 = ri_r(ws[i - 15], 32, 7) ^ ri_r(ws[i - 15], 32, 18) ^ (ws[i - 15] >> 3)
        s1 = ri_r(ws[i - 2], 32, 17) ^ ri_r(ws[i - 2], 32, 19) ^ (ws[i - 2] >> 10)
        ws[i] = (ws[i - 16] + s0 + ws[i - 7] + s1) % add_v
    return ws

# Rotates a number of a given length right once
def rotate_r1(num, bits):
    num &= (2 ** bits-1)
    bit = num & 1
    num >>= 1
    if(bit):
        num |= (1 << (bits - 1))
    return num

# Rotates a number right a given number of times
def ri_r(num, bits, rot):
    for _ in range(rot):
        num = rotate_r1(num, bits)
    return num 

if __name__ == "__main__":
    main()