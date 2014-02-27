# Zach Arnold
# sm.py
# LAB8 


""" description: My program passed all the tests, beyond that I am not
sure of any special cases that I handled. I did, however, write all of my
own functions (for eg: conversion to bitstring etc). also my program handles
various errors such as: typos with mnemonics, using incorect labels as
operands, aswell as general syntax errors with the operand. one cool thing
is that these produce the line numbers of the syntax errors. Also I have added
error detection to extended operands to make sure they can only be used on
3/4 instructions. This scenario will prompt the user with the mnemonic
or directive they inadvertantly tried to extend. I also handle duplicate labels
 and invalid hex chars (the latter with line numbers)"""
import sys

# globals:
BASE_BOOL = False
BASE = 0

Mnemonics = {'START': ['D',0],
    'BASE': ['D',0],
    'END':  ['D',0],
    'BYTE': ['D',3],
    'WORD': ['D',3],
    'RESB': ['D',3],
    'RESW': ['D',3],
    'STL': ['I',3,0x14,['m']],
    'RMO': ['I',2,0xAC,['r','r']],
    'ADD': ['I',3,0x18,['m']],   
    'ADDF': ['I',3,0x58,['m']],
    'ADDR': ['I',2,0x90,['r','r']],  
    'AND': ['I',3,0x40,['m']],
    'CLEAR': ['I',2,0xB4,['r']],
    'COMP': ['I',3,0x28,['m']],
    'COMPF': [ 'I',3,0x88,['m']],
    'COMPR': ['I',2,0xA0,['r','r']],
    'DIV': ['I',3,0x24,['m']],
    'DIVF': ['I',3,0x64,['m']],
    'DIVR': ['I',2,0x9C,['r','r']], 
    'FIX': ['I',1,0xC4,"none"],
    'HIO': ['I',1,0xF4,"none"],
    'J': ['I',3,0x3C,['m']],
    'JEQ': ['I',3,0x30,['m']],
    'JGT': ['I',3,0x34,['m']],
    'JLT': ['I',3,0x38,['m']],
    'JSUB': ['I',3,0x48,['m']],  
    'LDA': ['I',3,0x00,['m']], 
    'LDB': ['I',3,0x68,['m']],
    'LDCH': ['I',3,0x50,['m']],   
    'LDF': ['I',3,0x70,['m']],
    'LDL': ['I',3,0x08,['m']], 
    'LDS': ['I',3,0x6C,['m']],
    'LDT': ['I',3,0x74,['m']],
    'LDX': ['I',3,0x04,['m']],
    'LPS': ['I',3,0xD0,['m']],
    'MUL': ['I',3,0x20,['m']],
    'MULF': ['I',3,0x60,['m']],
    'MULR': ['I',2,0x98,['r','r']],
    'NORM': ['I',1,0xC8],
    'OR': ['I',3,0x44,['m']],
    'RD': ['I',3,0xD8,['m']],
    'RMO': ['I',2,0xAC,['r','r']],
    'RSUB':['I',3,0x4C,"none"],
    'SHIFTL': ['I',2,0xA4,['r','n']],
    'SHIFTR': ['I',2,0xA8,['r','n']], 
    'SIO': ['I',1,0xF0, "none"],
    'SSK': ['I',3,0xEC,['m']], 
    'STA': ['I',3,0x0C,['m']],
    'STB': ['I',3,0x78,['m']],
    'STCH': ['I',3,0x54,['m']],
    'STF': ['I',3,0x80,['m']], 
    'STI': ['I',3,0xD4,['m']],
    'STL': ['I',3,0x14,['m']],
    'STS': ['I',3,0x7C,['m']],
    'STSW': ['I',3,0xE8,['m']],
    'STT': ['I',3,0x84,['m']],
    'STX': ['I',3,0x10,['m']],
    'SUB': ['I',3,0x1C,['m']],
    'SUBF': ['I',3,0x5C,['m']],
    'SUBR': ['I',2,0x94,['r','r']],
    'SVC': ['I',2,0xB0,['n']],
    'TD': ['I',3,0xE0,['m']],
    'TIO': ['I',1,0xF8,"none"],
    'TIX': ['I',3,0x2C,['m']],
    'TIXR': ['I',2,0xB8,['r']],
    'WD': ['I',3,0xDC,['m']]}

symtab ={}

MnemonicOffsets = []

RegisterNumbers = {'A' : 0, 
                   'X' : 1,
                   'L' : 2,
                   'B' : 3,
                   'S' : 4,
                   'T' : 5,
                   'PC' : 8, 
                   'SW' : 9}
                              

def isspace(c):
    return c==' ' or c=='\t' or c== '\n'

def isExtended(mnemonic):
    """ return true iff this mnemonic begins with a '+' """
    return (mnemonic[0] == '+')
def error(msg):
    """ print msg and abort the program """
    print msg
    sys.exit(-1)

def parseLine(line, count):
    lineWords = line.split()
    periodList = [".",".","."]
    
    label = " "
    mnemonic = " "
    arguments = " "
    if line[0] == '.':
        temp = []
        temp.append('.')
        lineStr = ""
        for thing in lineWords:
            if thing != '.':
                lineStr = lineStr + ' ' + thing
        temp.append(lineStr)
        return temp
    if (not isspace(line[0]) and len(lineWords) >= 3):
        label = lineWords[0]
        mnemonic = lineWords[1]
        arguments = lineWords[2]
    elif (not isspace(line[0]) and len(lineWords) == 2):
        label = lineWords[0]
        mnemonic = lineWords[1]   
    else:
        mnemonic = lineWords[0]
        if (len(lineWords) > 1):
            arguments = lineWords[1]
        else:
            arguments = " "
    list = []
    list.append(label)
    count = str(count)
    if (not (mnemonic in Mnemonics) and not(mnemonic[1:] in Mnemonics)):
        error("Error with syntax invovling '"+ mnemonic + "' on line: "
              + count)
    list.append(mnemonic)
    list.append(arguments)
    return list

def makeLiteral(string):
    """ string is C'CCCCCC...' or (hex) X'HHHHHH....'.
        Return a list of bytes that this represents """
    return string[2:len(string) - 1]

def toBaseTen(string):
    """ string looks like an unsigned number, as a sequence of decimal 
        numerals, or as X'HHH...' or as C'C' where H is a hex digit, C
        is a character.  Returns the number represented by the string."""
    # note:  for now only base 10 can be converted.  Make this better later!
    return int(string)

def ReplaceExtended(str):
    if(str[0] == '+'):
       return str
    return '+' + str

def handleExtended(oldStr):
    newStr = ""
    for i in range(len(oldStr)):
        if ( i != 0):
            newStr += oldStr[i]
    return newStr

def assLength(mnemonic, operands):
    """ returns the assembled length of a mnemonic"""
    if (mnemonic == "BYTE"):
        if operands[0:2] == "C'":
            length = makeLiteral(operands)
            return len(length)
        elif  operands[0:2] == "X'":
            length = makeLiteral(operands)
            return len(length) / 2
        else:
            return 1
            
    if (mnemonic == "WORD"):
        if operands[0:2] == "C'":
            length = makeLiteral(operands)
            return 3 * len(length)
        elif operands[0:2] == "X'":
            length = makeLiteral(operands)
            return 3 * (len(length)/2)
        else:
            return 3
        
    if (mnemonic == "RESW"or mnemonic == "RESB"):
        if operands[0:2] == "C'":
            if(mnemonic == "RESB"):
                return len(makeLiteral(operands))
            else:
                return 3 * len(makeLiteral(operands))
        elif operands[0:2] == "X'":
            if(mnemonic == "RESB"):
                return len(makeLiteral(operands)) / 2
            else:
                return 3 * (len(makeLiteral(operands))/2)
            
        else:
            if(mnemonic == "RESB"):
                return int(operands)
            else:
                return 3 * int(operands)
    return Mnemonics[mnemonic][1]

def getBase(menmonic, operand):
    """ figures out where the base is"""
    if (operand in symtab):
        return symtab[operand]
    elif operand[0:2] == "X'":
        temp = operand[2:len(operand) - 1]
        return 5
        
    else:
        return int(operand[1:])

        

def getOffsetList(THE_LIST):
    offsetList = []
    count = 0
        
    extendedBool = False
    for thing in THE_LIST:
                
        if (thing[0][0] != '.'):
            label = thing[0]
            mnemonic = thing[1]
            operand = thing[2]
            if (mnemonic[0] == '+'):
                extendedBool = True
                mnemonic = handleExtended(mnemonic)
                if Mnemonics[mnemonic][0] == "D":
                    error("Directives can't be extended.(" + mnemonic + ")")
                if Mnemonics[mnemonic][1] != 3:
                    error("Mnemonic '" + mnemonic + "' can't be extended.")
            temp = []
            if(mnemonic == "BASE"):
                BASE_BOOL = True
                temp.append(" ")
                temp.append("BASE")
                temp.append(thing[2])
                
            else:
                temp.append(thing[0])
                temp.append(count)
                temp.append(thing[1])
            if(extendedBool):
                count += 1
            count += assLength(mnemonic, operand)
            if(extendedBool):
                extendedBool = False
            offsetList.append(temp)
    last = []
    last.append('')
    last.append(count)
    offsetList.append(last)
    
    return offsetList
def getLen(list):
    count =0
    for element in list:
        
        if (element[0] != '.'):
            count += 1
    return count
def oppositeBit(b):
    """ b is a single char, 0 or 1.  return the other. """
    if (b == '0'):
        return '1'
    else:
        return '0'
       
def bitStr2Comp(bitstring):
    """ compute and return the 2's complement of bitstring """
    bitList = []
    result = ""
        
    #put the string into a list and perform two's compliment...
    for i in range(len(bitstring)):
        bitChar = oppositeBit(bitstring[i])
        bitList.append(bitChar)
        #...by adding 1 at the end
    
    size = len(bitList) - 1
    for j in range(size):
        
        if bitList[size-j] == '1':
            bitList[size-j] = oppositeBit(bitList[size-j])
        else:
            bitList[size-j] = oppositeBit(bitList[size-j])
            break
    
        
    #now put it back into a string...
    for thing in bitList:
        result += thing
    return result
    

def toBitString(val,length=24):
    """Build and return a bit string of the given length.  
       val is a signed integer"""
    bitStr = ""
    if val >= 0:
        for i in range(length):
            pow = (length - 1) - i
            if (val >= 2**pow):
                bitStr += '1'
                val -= 2**pow
            else:
                bitStr += '0'
        return bitStr
    else:
        val = val * (-1)
        for i in range(length):
            pow = (length - 1) - i
            if (val >= 2**pow):
                bitStr += '1'
                val -= 2**pow
            else:
                bitStr += '0'
        answerList = []
        for i in range(len(bitStr)):
            answerList.append(oppositeBit(bitStr[i]))
        answer = ""
        size = len(answerList) - 1
        for i in range(len(answerList)):
            if answerList[size - i] == '1':
                answerList[size - i] = '0'
            else:
                answerList[size - i] = '1'
                break
        for part in answerList:
            answer = answer + part
            
        if answer[0] == '0':
            answer = answer[1:]
            answer = '1' + answer
        size = len(answer) - 1
        finalAns = ""
        
                
            
        return answer
    
def createSymTab(offsetList):
    count = 0
    for element in offsetList:
        if element[0] in symtab:
            error("The label '" + element[0] + "' is already used.")
        if element[0] != ' ':
            symtab[element[0]] = element[1]
            count += 1
    return
def makeDec(bitstring):
    """returns a Decimal string"""
    Val = 0
    pow = len(bitstring) - 1
    i = 0
    while(pow >= 0):
        if bitstring[i] == '1':
            Val = Val + 2**pow
        pow = pow - 1
        i = i + 1
    return Val
def adjustNum(num):
    """returns the proper hex char"""
    if (num == 10):
        return 'A'
    if (num == 11):
        return 'B'
    if (num == 12):
        return 'C'
    if (num == 13):
        return 'D'
    if (num == 14):
        return 'E'
    if (num == 15):
        return 'F'
    return str(num)
        

def makeHex(bitstring,length):
    """returns a hex string"""
    HexString = ""
    dec = makeDec(bitstring)
    pow = length - 1
    while (pow >= 0):
        if dec >= 16**pow :
            num = dec/(16**pow)
            dec -= num * (16**pow)
            num = adjustNum(num)
            HexString = HexString + num
        else:
            HexString = HexString + '0'
        pow -= 1
    return padHex(HexString, length)

def padWithZeros(instruction):
    """pads with zeros to make a bit string of length 24"""
    if (len(instruction) < 24):
        needed = 24 - len(instruction)
        for i in range(needed):
            instruction = '0' + instruction
    return instruction

def padHex(hex, leng):
     """pads with zeros to make a bit string of length 24"""
     if (len(hex) < leng):
         needed = leng - len(hex)
         for i in range(needed):
             hex = '0' + hex
     return hex
 
def parseOperand(operands):
     """ eg: in: #5 out: the string 5"""
     charList = []
     key = ""

     #----- get rid of the #
     for i in range(len(operands)):
         if i != 0:
             charList.append(operands[i])
     for char in charList:
         key += char
     return key
def containsCX(string):
    """ returns true if ,X is in string"""
    count = 0
    for i in range(len(string)):
        if string[i] == ",":
            count = 1
        elif string[i] == 'X' and count == 1:
            return True
        else:
            count == 0
    return False
def handleIndexed(operands):
    return operands[:len(operands) - 2]

def isHex(char):
    """returns true id char is a valid Hex char"""
    if (char == '1' or char == '2' or char == '3' or char == '4' or
        char == '5' or char == '6' or char == '7' or char == '8' or
        char == '9' or char == 'A' or char == 'B' or char == 'C' or
        char == 'D' or char == 'E' or char == 'F' or char == '0'):
        return True
    return False
    
      
             
def handleDisplacement(mnemonic, operands, nixbpeList, r, lenStr, lC):
    """ returns the displacement depending on the operands used"""
  
    #--- handle the begining of the operand
    if (operands[0] == '#'):
        operands = parseOperand(operands)
        nixbpeList[1] = True
    elif (operands[0] == '@'):
        operands = parseOperand(operands)
        nixbpeList[0] = True
    elif (containsCX(operands)):
        operands = handleIndexed(operands)
        nixbpeList[2] = True
        nixbpeList[0] = True
        nixbpeList[1] = True
    else:
        nixbpeList[0] = True
        nixbpeList[1] = True
    
    #--- handle the rest
    if (operands in symtab):
        
        if nixbpeList[5] == False: # not extended
            num = ((symtab[operands])- (MnemonicOffsets[r][1] +
                                       assLength(mnemonic, operands)))

            if (num < -2048 or num > 2047):
                #Base Relative!
                num = (symtab[operands] - BASE)
                num = toBitString(num,lenStr)
                nixbpeList[3] = True
            else:
                nixbpeList[4] = True
                num = toBitString(num,lenStr)
        else:
            # absolute adressing
            num = symtab[operands]
            num = toBitString(num, lenStr)
         
        return num
    elif (Mnemonics[mnemonic][3] == "none"):
          return toBitString(0, lenStr)
    
    else:
        if (operands[0:2] == "C'"):
            temp = operands[2:len(operands)-1]
            return operands[operands2]
        elif (operands[0:2] == "X'"):
            temp = operands[2:len(operands)-1]
            return operands[operands2]
            
        else:
            try:
                result = int(operands)
                result = toBitString(result,lenStr)
                return result
            except ValueError:
                error("Invalid operand syntax. line: " + str(lC))

def handleDir(dir, operand, lC):
    """ returns the instruction of the supplied directive"""
    ansList = []
    answer = ""
    if dir == "BYTE":
        if operand[0:2] == "C'":
            temp = operand[2:len(operand) - 1]
            for i in range(len(temp)):
                ansList.append(makeHex(toBitString(ord(temp[i]),8),2))
            for part in ansList:
                answer = answer + part
            return answer
        elif operand[0:2] == "X'":
            for i in range(2, len(operand) - 1):
                if not(isHex(operand[i])):
                    error("invalid hex char on line: " + str(lC))
                    
            return padHex(operand[2:len(operand)-1], 2)
        else:
            num = int(operand)
            num = toBitString(num)
            return makeHex(num,6)
                
      
    else:
        if operand[0:2] == "X'":
            for i in range(2, len(operand) - 1):
                if not(isHex(operand(i))):
                    error("invalid hex char on line: " + str(lC))
            return padHex(operand[2:len(operand)-1], 6)
        else:
            num = int(operand)
            num = toBitString(num)
            return makeHex(num,6)
        
    
def makeInstruction(mnemonic,operands,r, lC):
    """ return the proper hexadecimal string, a machine code instruction """
    instruction = ""
    nixbpe = ""
    instrType = 0
    nixbpeList = [False, False, False, False, False, False]
            
                 
    if mnemonic != '.':

        #--- handleDirectives
        if mnemonic == "RESW":
            if operands[0:2] == "X'":
                for i in range(2, len(operands) - 1):
                    if not(isHex(operands[i])):
                        error("invalid hex char on line: " + str(lC))
                             
            return " "
        if mnemonic == "RESB":
            return " "
            if operands[0:2] == "X'":
                for i in range(2,len(operands) - 1):
                    if not(isHex(operands[i])):
                        error("invalid hex char on line: " + str(lC))
             
            return " "
        if mnemonic == "WORD":
            return handleDir("WORD", operands, lC)
        if mnemonic == "BYTE":
            return handleDir("BYTE", operands, lC)
        
        instrType = 0
        #-- extended?        
        if mnemonic[0] == '+':
            mnemonic = handleExtended(mnemonic)
            instrType += 1
            nixbpeList[5] = True
        instrType += Mnemonics[mnemonic][1]
            
        #-- directive?
        if Mnemonics[mnemonic][0] == 'D':
            return " "
                        
        if instrType == 1:
            #-- get opcode
            return makeHex(toBitString(Mnemonics[mnemonic][2],8), 2)
        if instrType == 2:
            #-- get opcode
            opcode = toBitString(Mnemonics[mnemonic][2],8)
            #-- handle the operands
            if (len(Mnemonics[mnemonic][3]) > 1):
                if Mnemonics[mnemonic][3] == ['r','n']:
                    op1,op2 = operands.split(',')
                    operand1 = toBitString(RegisterNumbers[op1],4)
                    operand2 = toBitString(int(op2))
                    if mnemonic == "SHIFTL" or mnemonic == "SHIFTR":
                        operand2 = toBitString(int(op2) - 1, 4)
                    instruction = opcode + operand1 + operand2
                    
                else:
                    op1,op2 = operands.split(',')
                    operand1 = toBitString(RegisterNumbers[op1],4)
                    operand2 = toBitString(RegisterNumbers[op2],4)
                    instruction = opcode + operand1 + operand2
            else:
                if Mnemonics[mnemonic][3] == ['r']:
                    operand = toBitString(RegisterNumbers[operands],4)
                    instruction = opcode + operand + "0000"
                else:
                    answer = parseOperand(operands[0])
                    answer = toBitString(answer,4)
                    instruction = opcode + answer
            return makeHex(instruction, 4)
    
        #----- get opcode
        opcode = toBitString(Mnemonics[mnemonic][2],8)
                
        #----- handle displacement
            
        if instrType == 3:
                displacement = handleDisplacement(mnemonic,operands,
                                                  nixbpeList, r, 12, lC)
        else:
                displacement = handleDisplacement(mnemonic,operands,
                                                  nixbpeList, r, 20, lC)
        #----- handle NIXBPE
        if (nixbpeList[0]): #N
            nixbpe += '1'
        else:
            nixbpe += '0'
        if (nixbpeList[1]): #I
            nixbpe += '1'
        else:
            nixbpe += '0'
        if (nixbpeList[2]): #X
            nixbpe += '1'
        else:
            nixbpe += '0'
        if (nixbpeList[3]): #B
            nixbpe += '1'
        else:
            nixbpe += '0'
        if (nixbpeList[4]): #P
            nixbpe += '1'
        else:
            nixbpe += '0'
        if (nixbpeList[5]): #E
            nixbpe += '1'
        else:
            nixbpe += '0'

        #--- account for NI
        opcode = opcode[:6]
        
        instruction = opcode + nixbpe + displacement
                
        if instrType == 3:
            dLen = 6
        else:
            dLen = 8

        return makeHex(instruction,dLen)
    return " "
    
def makeMnemonicOffsets(offsetList):
    for line in offsetList:
        if line[0] != '':
            temp = []
            temp.append(line[2])
            temp.append(line[1])
            MnemonicOffsets.append(temp)
        else:
            last = []
            last.append("Total")
            last.append(line[1])
            MnemonicOffsets.append(last)
                       
    return

def main():
    
    THE_LIST = []
    offsetList=[]
    InstructionList = []
    file = open(sys.argv[1])
    #file = open("assemble2.asm")
    lines = file.readlines()

    countLines = 1 #keep track of line count for errors

    #--- PASS 1 ---
    for line in lines:
        line = line + "\n"
        THE_LIST.append(parseLine(line[:-1], countLines))
        countLines += 1

    offsetList = getOffsetList(THE_LIST)
    createSymTab(offsetList)
    #--------------

    makeMnemonicOffsets(offsetList)

    #--- PASS 2 ---
    r = 0 # iterations
    lC = 1 # line count
    for segment in THE_LIST:
        if segment[0] != '' and segment[0] != '.':
            mnemonic = segment[1]
            operands = segment[2]
            if mnemonic == "BASE":
                global BASE
                segment[0] == " "
                BASE = getBase(mnemonic, operands)
            instr = makeInstruction(mnemonic, operands, r, lC)
            segment.append(instr)
            if segment[0] != '.':
                r += 1
        lC += 1
    #---- output!
    for symbol in symtab:
        if symbol != '':
            print "\t%s\t: %06X"%(symbol, symtab[symbol]) 
       
    count = 0
    for thing in THE_LIST:
        if thing[0] != '.' and thing[1] != "END":
            if thing[1] == "BASE":
                print "%s\t%s\t%s\t%s\t%s"% (" ",
                                      thing[0],thing[1],thing[2]," ")
                
            else:
                print "%06X\t%s\t%s\t%s\t%s"% (offsetList[count][1],
                                      thing[0],thing[1],thing[2],thing[3])
        elif thing[0] == '.':
            print "\t" + thing[0] + ' ' + thing[1]
        else:
            print "\t%s\t%s\t%s\t%s"% (thing[0],thing[1],thing[2],thing[3])
            
        if (thing[0] != '.'):
            count += 1
main()
