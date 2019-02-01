# Auth: Cole Cummins

from string import ascii_lowercase

# --- Shift Cipher ---
# Basic ceasar cipher or shift cipher, "shifts" the alphabet by a specified 
# number, extremely insecure, used primarily for historic/teaching purposes

def main():
    a_list = list(ascii_lowercase) 

    ans = input("Please enter a sentence: ")
    while not check_valid(ans):
        ans = input("Not a valid sentence!\nPlease enter a sentence: ")

    rot = input("Please enter the number of times to rotate: ")
    while not rot.isnumeric():
        rot = input("Not a valid number!\nPlease enter a number: ")

    r_list = a_list[int(rot % 26):] + a_list[:int(rot % 26)]
    f_dict = dict(zip(a_list, r_list))
    f_str = final_string(f_dict, ans)
    print(f_str)


def final_string(dict, ans):
    f_str = ""
    for c in ans:
        if c == ' ':
            f_str += " "
            continue
        if ord(c) > 64 and ord(c) < 91:
            f_str += chr(ord(dict[chr(ord(c) + 32)]) - 32)
        else:
            f_str += dict[c]
    return f_str


def check_valid(word):
    for c in word:
        if ord(c) < 97 or ord(c) > 122:
            if ord(c) == 32 or ord(c) > 64 or ord(c) < 91:
                continue
            return False
    return True


if __name__ == "__main__":
    main()