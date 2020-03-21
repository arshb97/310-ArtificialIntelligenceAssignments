#!/usr/bin/python3
# CMPT310 A2
#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
"""
num_hours_i_spent_on_this_assignment = 25
"""
#
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
"""
Interesting course
Good assignment

"""
#####################################################
#####################################################
import sys, getopt
import copy
import random
import time
import numpy as np
sys.setrecursionlimit(10000)

class SatInstance:
    def __init__(self):
        pass

    def from_file(self, inputfile):
        self.clauses = list()
        self.VARS = set()
        self.p = 0
        self.cnf = 0
        with open(inputfile, "r") as input_file:
            self.clauses.append(list())
            maxvar = 0
            for line in input_file:
                tokens = line.split()
                if len(tokens) != 0 and tokens[0] not in ("p", "c"):
                    for tok in tokens:
                        lit = int(tok)
                        maxvar = max(maxvar, abs(lit))
                        if lit == 0:
                            self.clauses.append(list())
                        else:
                            self.clauses[-1].append(lit)
                if tokens[0] == "p":
                    self.p = int(tokens[2])
                    self.cnf = int(tokens[3])
            assert len(self.clauses[-1]) == 0
            self.clauses.pop()
            if (maxvar > self.p):
                print("Non-standard CNF encoding!")
                sys.exit(5)
        # Variables are numbered from 1 to p
        for i in range(1, self.p + 1):
            self.VARS.add(i)

    def __str__(self):
        s = ""
        for clause in self.clauses:
            s += str(clause)
            s += "\n"
        return s


def main(argv):
    inputfile = ''
    verbosity = False
    inputflag = False
    try:
        opts, args = getopt.getopt(argv, "hi:v", ["ifile="])
    except getopt.GetoptError:
        print('DPLLsat.py -i <inputCNFfile> [-v] ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('DPLLsat.py -i <inputCNFfile> [-v]')
            sys.exit()
        ##-v sets the verbosity of informational output
        ## (set to true for output veriable assignments, defaults to false)
        elif opt == '-v':
            verbosity = True
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            inputflag = True
    if inputflag:
        instance = SatInstance()
        instance.from_file(inputfile)
        #start_time = time.time()
        solve_dpll(instance, verbosity)
        #print("--- %s seconds ---" % (time.time() - start_time))

    else:
        print("You must have an input file!")
        print('DPLLsat.py -i <inputCNFfile> [-v]')


# Finds a satisfying assignment to a SAT instance,
# using the DPLL algorithm.
# Input: a SAT instance and verbosity flag
# Output: print "UNSAT" or
#    "SAT"
#    list of true literals (if verbosity == True)
#
#  You will need to define your own
#  DPLLsat(), DPLL(), pure-elim(), propagate-units(), and
#  any other auxiliary functions
def solve_dpll(instance, verbosity):
    # print(instance)
    # instance.VARS goes 1 to N in a dict
    # print(instance.VARS)
    # print(verbosity)
    ###########################################
    # Start your code
    clauses = instance.clauses
    variables = instance.VARS

    result = solveDpll(clauses, variables)

    if result:
        print("SAT")
        if verbosity:
            print(sorted([x for x in range(1, instance.p+1) if -x not in result]))
    else:
        print("UNSAT")

    return True

    ###########################################

def pureElim(clauses):
    pureAssigned = list()
    pureUnits = list()
    tempDict = dict()
    for clause in clauses:
        for literal in clause:
            tempDict[literal] = tempDict.get(literal, 0) + 1

    for unit, n in tempDict.items():
        if -unit not in tempDict:
            clauses = selectUn(unit, clauses)
            pureUnits.append(unit) 
    pureAssigned += pureUnits

    return clauses, pureAssigned

def propogateUnits(clauses):
    unitAssigned = list()
    unitClause = list(filter(lambda x: len(x) == 1, clauses))
    while unitClause:
        unit = unitClause[0]
        clauses = selectUn(unit[0], clauses)
        unitAssigned.append(unit[0])
        if clauses == -1:
            return -1, []
        if not clauses:
            return clauses, unitAssigned
        unitClause = list(filter(lambda x: len(x) == 1, clauses))
    return clauses, unitAssigned



def selectVariable(clauses):
    tempDict = dict()
    for clause in clauses:
        for literal in clause:
            tempDict[literal] = tempDict.get(literal, 0) + 1
    return random.choice(list(tempDict.keys()))


def selectUn(unit, clauses):
    tempList = list()
    for clause in clauses:
        if -unit in clause:
            c = list(filter(lambda x: x != -unit, clause))
            if not c:
                return -1
            tempList.append(c)
        elif unit not in clause:
            tempList.append(clause)
    return tempList


def solveDpll(clauses, variables):
    variables = list(variables)
    clauses, pureAssigned = pureElim(clauses)
    clauses, unitAssigned = propogateUnits(clauses)
    variables = variables + unitAssigned + pureAssigned
    
    if clauses == -1:
        return []
    if not clauses:
        return variables

    temp = selectVariable(clauses)
    result = solveDpll(selectUn(temp, clauses), variables+[temp])
    return solveDpll(selectUn(-temp, clauses), variables+[-temp]) if not result else result

if __name__ == "__main__":
    main(sys.argv[1:])
