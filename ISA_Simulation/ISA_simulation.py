

def sim(program):
    # Machine Code to Simulation

    finished = False  # Is the simulation finished?
    PC = 0  # Program Counter
    register = [0] * 4  # Let's initialize 4 empty registers #[A,B,Hi,Low]
    #[A,B,Hi,Low]
    mem = [0] * 259  # Let's initialize 259 spots in memory

    DIC = 0  # Dynamic Instr Count
    while (not (finished)):

        if PC == len(program) - 1:
            finished = True


        fetch = program[PC]
        DIC += 1

        # ADDI  - Sim
        if fetch[0:3] == '000':
            PC += 1
            r1 = int(fetch[3], 2)
            imm = int(fetch[4:], 2)
           # imm = -(16 - int(fetch[5:], 2)) if fetch[5] == '1' else int(fetch[5:], 2)
            register[r1] += imm

        # mult  - Sim
        elif fetch[0:3] == '100':
            PC += 1
            r1 = int(fetch[3:5], 2)
            r2 = int(fetch[5:7], 2)

            #UNSURE
            result = register[r1] * register[r2]

            register[3] = result & 0x00FF # LOW
            register[2] = result >> 8 # HI


        # SBU - Sim
        elif fetch[0:3] == '111':
            PC += 1

        # LBU - Sim
        elif fetch[0:3] == '110':
            PC += 1

        # SRL
        elif fetch[0:3] == '011':
            PC += 1

        # SRL
        elif fetch[0:3] == '010':
            PC += 1

        # XOR  - Sim
        elif fetch[0:3] == '101':
            PC += 1

        # BNE  - Sim
        elif fetch[0:3] == '001':
            PC += 1

    # Finished simulations. Let's print out some stats
    print('***Simulation finished***')

    print('')

    print('Dynamic Instr Count: ', DIC)


    input()


def main():

    f = open("mc.txt", "w+")
    h = open("LittleMonsterHash.txt", "r")

    asm = h.readlines()

    for item in range(asm.count('\n')):  # Remove all empty lines '\n'
        asm.remove('\n')

    for line in asm:

        line = line.replace("\n", "")  # Removes extra chars
        line = line.replace("$", "")
        line = line.replace(" ", "")
        line = line.replace("zero", "0")  # assembly can also use both $zero and $0

        # = = = = ADDI = = = = = = = =
        if (line[0:4] == "addi"):
            line = line.replace("addi", "")
            line = line.split(",")

            imm = format(int(line[1]), '04b') if (int(line[1]) >= 0) else format(16 + int(line[1]), '04b')
            r1 = format(0, '01b')  # Assuming its A
            if (line[0] == "B"):
                r1 = format(1, '01b')


            f.write(str('000') + str(r1) + str(imm) + '\n')


        # = = = = MULT = = = = = = = =
        elif (line[0:4] == "mult"):
            line = line.replace("mult", "")
            line = line.split(",")

            r1 = 0
            r2 = 0

            if (line[0] == "B"):
                r1 = 1
            elif (line[0] == "hi"):
                r1 = 2
            elif (line[0] == "lo"):
                r1 = 3

            if (line[1] == "B"):
                r2 = 1
            elif (line[1] == "hi"):
                r2 = 2
            elif (line[1] == "lo"):
                r2 = 3

            r1 = format(r1, '02b')  # make element 1 in the set, 'line' an int of 2 bits. (r1)
            r2 = format(r2, '02b')  # make element 2 in the set, 'line' an int of 3 bits. (r2)

            f.write(str('100') + str(r1) + str(r2) + str('0') + '\n')

        # = = = = SRL = = = = = = = =
        elif (line[0:3] == "srl"):
            line = line.replace("srl", "")
            line = line.split(",")

            r1 = 0
            r2 = 0
            if (line[0] == "B"):
                r1 = 1
            elif (line[0] == "hi"):
                r1 = 2
            elif (line[0] == "lo"):
                r1 = 3

            if (line[1] == "B"):
                r2 = 1
            elif (line[1] == "hi"):
                r2 = 2
            elif (line[1] == "lo"):
                r2 = 3
            r1 = format(r1, '02b')  # make element 0 in the set, 'line' an int of 2 bits. (r1)
            r2 = format(r2, '02b')  # make element 2 in the set, 'line' an int of 2 bits. (r2)
            two_or_four = format(int(line[2]), '01b')  # make element 3 in the set, 'line' an int of 1 bits. (sh)

            f.write(str('011') + str(r1) + str(r2) + str(two_or_four) + '\n')


        elif (line[0:3] == "sll"):
            line = line.replace("sll", "")
            line = line.split(",")
            r1 = 0
            r2 = 0
            if (line[0] == "B"):
                r1 = 1
            elif (line[0] == "hi"):
                r1 = 2
            elif (line[0] == "lo"):
                r1 = 3

            if (line[1] == "B"):
                r2 = 1
            elif (line[1] == "hi"):
                r2 = 2
            elif (line[1] == "lo"):
                r2 = 3
            r1 = format(r1, '02b')  # make element 0 in the set, 'line' an int of 2 bits. (r1)
            r2 = format(r2, '02b')  # make element 2 in the set, 'line' an int of 2 bits. (r2)
            two_or_four = format(int(line[2]), '01b')  # make element 3 in the set, 'line' an int of 1 bits. (sh)

            f.write(str('010') + str(r1) + str(r2) + str(two_or_four) + '\n')


        # SBU
        elif (line[0:3] == "sbu"):
            line = line.replace(")", "")  # remove the ) paran entirely.
            line = line.replace("(", ",")  # replace ( left paren with comma
            line = line.replace("sbu", "")
            line = line.split(
                ",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.

            r1 = 0
            r2 = 0
            if (line[0] == "B"):
                r1 = 1
            elif (line[0] == "hi"):
                r1 = 2
            elif (line[0] == "lo"):
                r1 = 3

            if (line[2] == "B"):
                r2 = 1


            r1 = format(r1, '02b')  # make element 0 in the set, 'line' an int of 1 bits. (r1)
            r2 = format(r2, '01b')  # make element 1 in the set, 'line' an int of 1 bits. (r2)
            imm = format(int(line[1]), '02b')

            f.write(str('111') + str(r1) + str(imm) + str(r2) + '\n')

         # LBU
        elif (line[0:3] == "lbu"):
            line = line.replace(")", "")  # remove the ) paran entirely.
            line = line.replace("(", ",")  # replace ( left paren with comma
            line = line.replace("ulb", "")
            line = line.split(
                ",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.

            r1 = 0
            r2 = 0
            if (line[0] == "B"):
                r1 = 1
            elif (line[0] == "hi"):
                r1 = 2
            elif (line[0] == "lo"):
                r1 = 3

            if (line[2] == "B"):
                r2 = 1

            r1 = format(r1, '02b')  # make element 0 in the set, 'line' an int of 1 bits. (r1)
            r2 = format(r2, '01b')  # make element 1 in the set, 'line' an int of 1 bits. (r2)
            imm = format(int(line[1]), '02b')
            f.write(str('110') + str(r1) + str(imm) + str(r2) + '\n')

        # = = = = XOR = = = = = = = =
        elif (line[0:3] == "xor"):
            line = line.replace("xor", "")
            line = line.split(",")

            r1 = 0
            r2 = 0

            if (line[0] == "B"):
                r1 = 1
            elif (line[0] == "hi"):
                r1 = 2
            elif (line[0] == "lo"):
                r1 = 3

            if (line[1] == "B"):
                r2 = 1
            elif (line[1] == "hi"):
                r2 = 2
            elif (line[1] == "lo"):
                r2 = 3

            r1 = format(r1, '02b')  # make element 1 in the set, 'line' an int of 2 bits. (r1)
            r2 = format(r2, '02b')  # make element 2 in the set, 'line' an int of 3 bits. (r2)

            f.write(str('101') + str(r1) + str(r2) + str('0') + '\n')


            # = = = = BNE = = = = = = = = =
        elif (line[0:3] == "bne"):
            line = line.replace("bne", "")
            line = line.split(",")


            r1 = 0

            if (line[0] == "B"):
                r1 = 1
            elif (line[0] == "hi"):
                r1 = 2
            elif (line[0] == "lo"):
                r1 = 3

            r1 = format(r1, '02b')
            Y = format(int(line[1]), '01b')
            ZZ = format(int(line[2]), '02b')

            f.write(str('001') + str(r1) + str(Y) + str(ZZ) + '\n')



    f.close()

    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    # file opener and reader (Machine Code)

    file = open('mc.txt')

    program = []

    for line in file:

        if line.count('#'):
            line = list(line)
            line[line.index('#'):-1] = ''
            line = ''.join(line)

        if line[0] == '\n':
            continue

        line = line.replace('\n', '')
        instr = line[:]

        program.append(instr)  # since PC increment by 4 every cycle,


    # We SHALL start the simulation!
    sim(program)


if __name__ == '__main__':
    main()
