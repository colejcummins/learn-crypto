# Auth: Cole Cummins

# ---Enigma Machine---
# Consists of three rotors and a reflector, settings can be entered manually

# The starting rotors and their step settings as tuples
alpha = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Enigma 1 Rotors 1, 2, 3
rotor_1_list = (list("EKMFLGDQVZNTOWYHXUSPAIBRCJ"), 17)
rotor_2_list = (list("AJDKSIRUXBLHWTMCQGZNPYFVOE"), 5)
rotor_3_list = (list("BDFHJLCPRTXVZNYEIWGAKMUSQO"), 22)

# Enigma Navy Reflector B
refl_b_list = list("YRUHQSLDPXNGOKMIEBFZCWVJAT")


# The rotor class represents a single rotor in the enigma machine
# The constructor takes an array representing the starting settings, a step, and
# a current count
class rotor:
    def __init__(self, inner_rotor, step, count=0):
        self.count = count
        self.step = step
        self.inner_map = dict(zip(alpha, inner_rotor))
        self.refl_map = dict(zip(inner_rotor, alpha))
        self.input_map = dict(zip(alpha, rotate(alpha, self.count)))
        self.output_map = dict(zip(alpha, rotate(alpha, -self.count)))

    def __repr__(self):
        return "Count: {!r}\nInner Map: {!r}\n".format(self.count, self.inner_map)

    # Increments the rotor count by one and updates the input and output maps
    def update(self):
        self.count = (self.count % 26) + 1
        self.input_map = dict(zip(alpha, rotate(alpha, self.count)))
        self.output_map = dict(zip(alpha, rotate(alpha, -self.count)))

    # Passes a single letter through the input map, inner ring, and output map
    def rotor_enc(self, let, reflected=False):
        let = self.input_map[let]

        # if the letter has been reflected, use the reflector ring
        if reflected:
            let = self.refl_map[let]
        else:
            let = self.inner_map[let]
        return self.output_map[let]


# The enigma class represents the enigma machine
# The enigma constructor initializes all three rotors and the reflector
class enigma:
    def __init__(self, settings=[0, 0, 0]):
        self.r1 = rotor(rotor_1_list[0], rotor_1_list[1], settings[0])
        self.r2 = rotor(rotor_2_list[0], rotor_2_list[1], settings[1])
        self.r3 = rotor(rotor_3_list[0], rotor_3_list[1], settings[2])
        self.refl = refl_b_list

    def __repr__(self):
        return "---Rotor1---\n{!r}\n---Rotor2---\n{!r}\n---Rotor3---\n{!r}\n".format(
                self.r1, self.r2, self.r3
        )

    # Updates the enigma machine and rotors accordingly, then encrypts a single
    # letter
    def enc_letter(self, let):

        # always updates rotor three
        self.r3.update()

        if self.r2.count == self.r2.step: self.r1.update()
        if self.r3.count == self.r3.step + 1 and self.r2.count == self.r2.step:
            self.r2.update()
        # rotors 1 and 2 are updated if the count equals the step 
        if self.r3.count == self.r3.step: self.r2.update()
        
        # The letter passes through rotor 3 -> rotor 2 -> rotor 1 -> reflector
        # rotor 1 -> rotor 2 -> rotor 3
        let = self.r1.rotor_enc(self.r2.rotor_enc(self.r3.rotor_enc(let)))
        let = alpha[self.refl.index(let)]

        # letter passes through 1 -> 2 -> 3 after hitting the reflector
        let = self.r3.rotor_enc(self.r2.rotor_enc(self.r1.rotor_enc(let, True), True), True)
        return let


# Main method, deals with user IO and initializing the enigma machine
def main():
    set = input("------ENIGMA------\nInput start settings (ex. 5, 26, 12): ")

    # checks if valid start settings have been entered 
    while not set.replace(", ", "").isnumeric() or len(set.split(",")) != 3:
        set = input("NOT VALID\nInupt start settings (ex. 5, 26, 12): ")
    set = set.split(",")
    enig_ma = enigma([int(set[i]) for i in range(3)])

    # initializes the plugboard 
    in_board, out_board = plugboard()

    # loops until the user inputs "quit"
    while True:
        print("\nSETTINGS: {!r}, {!r}, {!r}".format(enig_ma.r1.count,
                    enig_ma.r2.count, enig_ma.r3.count))
        inp = input("Input a word to be encoded: ")
        while not inp.replace(" ", "").isalpha():
            inp = input("NOT VALID\nInput a word to be encoded: ")
        if inp == "quit": 
            print("EXITING ENIGMA....")
            break
        if inp == "reset":
            print("RESETTING") 
            enig_ma = enigma([int(set[i]) for i in range(3)])
            continue

        dif_inp = translate(inp.upper().replace(" ", ""), in_board)
        print(translate(enigma_enc(enig_ma, dif_inp), out_board))


# translates the input to the plugboard
def translate(inp, board):
    return "".join(board[c] for c in inp)


# deals with the creation of the plugboard
def plugboard():  
    in_list = []
    out_list = [] 
    while True:
        inp = input("Enter plugboard settings (ex. W, M): ")

        while valid(inp):
            inp = input("NOT VALID\nEnter plugboard settings (ex. W, M): ")

        if inp == "start":
            break
        temp = inp.split(", ") 
        in_list += temp[0]
        out_list += temp[1]

    return (dict(zip(in_list, out_list)), dict(zip(out_list, in_list)))


# checks to see if the plugboard input is valid
def valid(inp):
    if len(inp.split(", ")) == 1 and inp == "start":
        return False
    for c in inp.split(", "):
        if len(c) > 1:
            return True
    return not inp.replace(", ", "").isalpha() or len(inp.split(", ")) != 2


# encodes all the letters in a given input
def enigma_enc(enig_ma, inp):
    return "".join(enig_ma.enc_letter(c) for c in inp)


# rotates a list by an amount n
def rotate(list, n):
    return list[n:] + list[:n]


if __name__ == "__main__":
    main()