

def sim(program):
    # Machine Code to Simulation

    finished = False  # Is the simulation finished?
    PC = 0  # Program Counter
    register = [0] * 4  # Let's initialize 4 empty registers
    mem = [0] * 259  # Let's initialize 259 spots in memory

    DIC = 0  # Dynamic Instr Count
    while (not (finished)):

        if PC == len(program) - 4:
            finished = True
            register[26] = PC + 4  # accounting for first/last instruction

        fetch = program[PC]
        DIC += 1

        # ADDI  - Sim
        if fetch[0:3] == '000':
            PC += 4
            r1 = int(fetch[4],2)
            imm = -(16 - int(fetch[5:], 2)) if fetch[5] == '1' else int(fetch[5:], 2)


        # mult  - Sim
        elif fetch[0:3] == '100':
            PC += 4



        # Store2bit - Sim
        elif fetch[0:3] == '111':
            PC += 4


        # SRL
        elif fetch[0:3] == '011' :
            PC += 4


        # ANDI (I) - Sim
        elif fetch[0:3] == '001':
            PC += 4

        # XOR  - Sim
        elif fetch[0:3] == '101':
            PC += 4

        # BNE  - Sim
        elif fetch[0:3] == '110':
            PC += 4

    # Finished simulations. Let's print out some stats
    print('***Simulation finished***')

    print('')

    print('Dynamic Instr Count: ', DIC)


    input()


# Remember where each of the jump label is, and the target location
def saveJumpLabel(asm, labelIndex, labelName):
    lineCount = 0
    countWithoutLabels = 0

    for line in asm:
        line = line.replace(" ", "")

        if (line.count(":")):
            labelName.append(line[0:line.index(":")])  # append the label name
            labelIndex.append(countWithoutLabels)  # append the label's index
            asm[lineCount] = line[line.index(":") + 1:]
            countWithoutLabels -= 1

        lineCount += 1
        countWithoutLabels += 1

    for item in range(asm.count('\n')):  # Remove all empty lines '\n'
        asm.remove('\n')


def main():
    # HW 4 (ASM to MC Instructions)
    labelIndex = []
    labelName = []

    f = open("mc.txt", "w+")
    h = open("testcase.asm", "r")

    asm = h.readlines()
    currentline = 0

    for item in range(asm.count('\n')):  # Remove all empty lines '\n'
        asm.remove('\n')

    saveJumpLabel(asm, labelIndex, labelName)  # Save all jump's destinations

    for line in asm:

        line = line.replace("\n", "")  # Removes extra chars
        line = line.replace("$", "")
        line = line.replace(" ", "")
        line = line.replace("zero", "0")  # assembly can also use both $zero and $0

        # = = = = ADDI = = = = = = = = (I)
        if (line[0:4] == "addi"):
            line = line.replace("addi", "")
            line = line.split(",")

            imm = format(int(line[1]), '04b') if (int(line[2]) >= 0) else format(16 + int(line[2]), '04b')
            r1 = format(int(line[0]), '02b')

            f.write(str('000') + str(r1) + str(imm) + '\n')
            currentline += 1

        # = = = = MULT = = = = = = = = (R)
        elif (line[0:4] == "mult"):
            line = line.replace("mult", "")
            line = line.split(",")

            r1 = format(int(line[0]), '02b')  # make element 1 in the set, 'line' an int of 2 bits. (r1)
            r2 = format(int(line[1]), '03b')  # make element 2 in the set, 'line' an int of 3 bits. (r2)

            f.write(str('100') + str(r1) + str(r2) + '\n')

        # = = = = SRL = = = = = = = = (R)
        elif (line[0:3] == "srl"):
            line = line.replace("srl", "")
            line = line.split(",")

            r1 = format(int(line[0]), '02b')  # make element 0 in the set, 'line' an int of 2 bits. (r1)
            r2 = format(int(line[1]), '02b')  # make element 2 in the set, 'line' an int of 2 bits. (r2)
            two_or_four = format(int(line[2]), '01b')  # make element 3 in the set, 'line' an int of 1 bits. (sh)

            f.write(str('011')  + str(r1) + str(r2) + str(two_or_four) + '\n')
            currentline += 1

        elif (line[0:3] == "sll"):
            line = line.replace("sll", "")
            line = line.split(",")

            r1 = format(int(line[0]), '02b')  # make element 0 in the set, 'line' an int of 2 bits. (r1)
            r2 = format(int(line[1]), '02b')  # make element 2 in the set, 'line' an int of 2 bits. (r2)
            two_or_four = format(int(line[2]), '01b')  # make element 3 in the set, 'line' an int of 1 bits. (sh)

            f.write(str('010') + str(r1) + str(r2) + str(two_or_four) + '\n')
            currentline += 1

        # STORE2bit
        elif (line[0:9] == "store2bit"):
            line = line.replace(")", "")  # remove the ) paran entirely.
            line = line.replace("(", ",")  # replace ( left paren with comma
            line = line.replace("store2bit", "")
            line = line.split(
                ",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.

            r1 = format(int(line[0]), '01b')  # make element 0 in the set, 'line' an int of 1 bits. (r1)
            imm = format(int(line[1]), '03b') if (int(line[1]) >= 0) else format(8 + int(line[1]), '03b')
            r2 = format(int(line[2]), '01b')  # make element 1 in the set, 'line' an int of 1 bits. (r2)

            f.write(str('111') + str(r1) + str(imm) + str(r2) + '\n')
            currentline += 1

        # = = = = ANDI = = = = = = = = = (I)
        elif (line[0:4] == "andi"):
            line = line.replace("andi", "")
            line = line.split(
                ",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.

            r1 = format(int(line[0]), '01b')  # make element 0 in the set, 'line' an int of 1 bits. (r1)
            imm = format(int(line[1]), '04b') if (int(line[1]) >= 0) else format(16 + int(line[1]), '04b')


            f.write(str('001') + str(r1) + str(imm) + '\n')
            currentline += 1

        # = = = = XOR = = = = = = = =
        elif (line[0:3] == "xor"):
            line = line.replace("xor", "")
            line = line.split(",")

            r1 = format(int(line[0]), '02b')  # make element 1 in the set, 'line' an int of 2 bits. (r1)
            r2 = format(int(line[1]), '03b')  # make element 2 in the set, 'line' an int of 3 bits. (r2)

            f.write(str('101') + str(r1) + str(r2) + '\n')

            currentline += 1

            # = = = = BNE = = = = = = = = = (I)
        elif (line[0:3] == "bne"):
            line = line.replace("bne", "")
            line = line.split(",")

            r1 = format(int(line[0]), '01b')
            r2 = format(int(line[1]), '01b')

            imm = format(int(line[2]), '03b') if (int(line[2]) >= 0) else format(8 + int(line[1]), '03b')

            f.write(str('110') + str(r1) + str(r2) + str(imm) + '\n')
            currentline += 1


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
        program.append(0)  # let's align the program code by every
        program.append(0)  # 4 lines
        program.append(0)

    # We SHALL start the simulation!
    sim(program)


if __name__ == '__main__':
    main()
