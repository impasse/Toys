#!/bin/python3
import sys

oper = {'(':')','[':']','{':'}'}
def main(filename):
    file = open(filename,'r')
    lines = file.readlines()
    for line in lines:
        stack = []
        quoted = False
        MatchError = False
        for c in line:
            if c=='"':
                quoted = not quoted
            if  quoted:
                continue
            else:
                if c in oper.keys():
                    stack.append(c)
                if c in oper.values():
                    if not tryFetch(stack,c):
                        MatchError = True
        if len(stack)==0 and MatchError == False:
            print("True")
        else:
            print("False")

def tryFetch(stack,c):
    try:
        if oper[stack.pop()]==c:
            return True
        else:
            return False
    except:
        return False


if __name__=="__main__":
    main(sys.argv[1])
