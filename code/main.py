import sys
import matplotlib.pyplot as plt
import numpy as np
import itertools
import math
import string
import re
import os
import copy
import glob
from a1 import *

def readInput(fileName) :

    with open(fileName, 'r') as f :
        InFile = f.readlines()

    shapes = []
    attributes = []

    for line in InFile :
        split = re.split('\\=|,0,|\\,|\\(|\\)|\\[|\\]|\\:| ', line)
        split = list(filter(None,split))
        shape = []
        if(split[0][0] == 'p') :
            if('+' in split) :
                continue
            shape = split[:]
            del shape[1]
            del shape[-1]
            shapes.append(shape[:])
        elif(split[0] == "scc" or split[0] == "rectangle" or split[0] == "square" or split[0] == "triangle" or split[0] == "circle" or split[0] == "dot") :
            for i in shapes :
                if(i[0] == split[1]) :
                    i.append(split[0][:])
                    break
        elif(split[0][0] == 'c' or split[0][0] == 'd') :
            shape = split[:]
            del shape[-1]
            shapes.append(shape[:])
        elif(split[0] == "vloc") :
            for i in shapes :
                if(i[0] == split[1]) :
                    i.append(split[2][:])
                    break
        elif(split[0] == "hloc") :
            for i in shapes :
                if(i[0] == split[1]) :
                    i.append(split[2][:])
                    break
        elif(split[0] == "left_of") :
            for i in shapes :
                if(i[0] == split[1]) :
                    i.append("left_of")
                    i.append(split[2][:])
                if(i[0] == split[2]) :
                    i.append("right_of")
                    i.append(split[1][:])
        elif(split[0] == "right_of") :
            for i in shapes :
                if(i[0] == split[1]) :
                    i.append("right_of")
                    i.append(split[2][:])
                if(i[0] == split[2]) :
                    i.append("left_of")
                    i.append(split[1][:])
        elif(split[0] == "below") :
            for i in shapes :
                if(i[0] == split[1]) :
                    i.append("below")
                    i.append(split[2][:])
                if(i[0] == split[2]) :
                    i.append("above")
                    i.append(split[1][:])
        elif(split[0] == "above") :
            for i in shapes :
                if(i[0] == split[1]) :
                    i.append("above")
                    i.append(split[2][:])
                if(i[0] == split[2]) :
                    i.append("below")
                    i.append(split[1][:])
        elif(split[0] == "inside") :
            for i in shapes :
                if(i[0] == split[1]) :
                    i.append("inside")
                    i.append(split[2][:])
                if(i[0] == split[2]) :
                    i.append("outside")
                    i.append(split[1][:])
        elif(split[0] == "overlap") :
            for i in shapes :
                if(i[0] == split[1]) :
                    i.append("overlap")
                    i.append(split[2][:])
                if(i[0] == split[2]) :
                    i.append("overlap")
                    i.append(split[1][:])
        elif(split[0] == "small") :
            continue
        elif(split[0] == "large") :
            continue
        elif(split[0] == "area") :
            continue
        else :
            print("there a problem here")
            exit(1)

    for i in shapes :
        if("scc" in i) :
            temp = i.index("scc")
            attributes.append(i[temp:])
            del i[temp:]
        elif("rectangle" in i) :
            temp = i.index("rectangle")
            attributes.append(i[temp:])
            del i[temp:]
        elif("square" in i) :
            temp = i.index("square")
            attributes.append(i[temp:])
            del i[temp:]
        elif("triangle" in i) :
            temp = i.index("triangle")
            attributes.append(i[temp:])
            del i[temp:]
        elif("circle" in i) :
            temp = i.index("circle")
            attributes.append(i[temp:])
            del i[temp:]
        elif("dot" in i) :
            temp = i.index("dot")
            attributes.append(i[temp:])
            del i[temp:]
        else :
            print("wat happen here")
            exit(1)

    return [shapes,attributes]

def makeMatch(A, B) :
    fullMatch = []
    fileA = 0
    for i in A :
        fileB = 0
        for j in B :
            Alist = []
            Blist = []
            for a in i[0] :
                Alist.append(a[0])
            for b in j[0] :
                Blist.append(b[0])

            if(len(Alist) > len(Blist)) :
                Blist.append("del")
            elif(len(Alist) < len(Blist)) :
                Alist.append("add")

            tempMatch = []
            pairs = [zip(x,Blist) for x in itertools.permutations(Alist,len(Blist))]
            for pair in pairs :
                tempMatch.append(list(pair))
            fullMatch.append([fileA,fileB,tempMatch[:]])
            fileB += 1
        fileA += 1
    return fullMatch

def areaCircle(radius) :
    return float(radius)*float(radius)*math.pi

def area(points) :
    runsum = 0

    for i in range(len(points)-1) :
        runsum += ((float(points[i][0])*float(points[i+1][1])) - (float(points[i+1][0])*float(points[i][1])))
    return abs(runsum/2)

def newGetTransformations(Matching, set1, set2) :
    pairs = Matching[:]
    transformationList = []
    thisList = []
    for i in range(len(pairs)) :
        fileA = pairs[i][0]
        fileB = pairs[i][1]
        bigPair = pairs[i][2][:]

        for z in range(len(bigPair)) :
            pair = bigPair[z][:]
            transformPls = []
            for j in range(len(pair)) :
                for k in range(j+1,len(pair),1) :
                    #find index of shapes within sets
                    tempTransformation = []
                    tempTransformation.append(pair)
                    locA = -1
                    locB = -1
                    addDel = False

                    for l in range(len(set1[fileA][0])) :
                        if(pair[j][0] == "add") :
                            tempTransformation.append("addt(" + pair[j][1] + ")")
                            addDel = True
                            break
                        if(pair[j][0] == set1[fileA][0][l][0]) :
                            locA = l
                            break
                    for l in range(len(set2[fileB][0])) :
                        if(pair[j][1] == "del") :
                            tempTransformation.append("delt(" + pair[j][0] + ")")
                            addDel = True
                            break
                        if(pair[j][1] == set2[fileB][0][l][0]) :
                            locB = l
                            break

                    if(addDel == False) :
                        tempTransformation.append(getAttributes(pair[j], pair[k], pair, set1[fileA][1][locA],set2[fileB][1][locB], set1[fileA][0][locA], set2[fileB][0][locB]))

                    addDel = False

                    for l in range(len(set1[fileA][0])) :
                        if(pair[k][0] == "add") :
                            tempTransformation.append("addt(" + pair[k][1] + ")")
                            addDel = True
                            break
                        if(pair[k][0] == set1[fileA][0][l][0]) :
                            locA = l
                            break
                    for l in range(len(set2[fileB][0])) :
                        if(pair[k][1] == "del") :
                            tempTransformation.append("delt(" + pair[k][0] + ")")
                            addDel = True
                            break
                        if(pair[k][1] == set2[fileB][0][l][0]) :
                            locB = l
                            break

                    if(addDel == False) :
                        tempTransformation.append(getAttributes(pair[k], pair[j], pair, set1[fileA][1][locA],set2[fileB][1][locB], set1[fileA][0][locA], set2[fileB][0][locB]))

                    tempFinTransformation = []
                    for l in tempTransformation :
                        if(len(l) == 0) :
                            del l
                            continue
                        if(l[0:4] == "addt" or l[0:4] == "delt" or len(l[0][0]) >= 2) :
                            tempFinTransformation.append(l[:])
                        else :
                            for s in l :
                                tempFinTransformation.append(s[:])
                    transformationList.append(tempFinTransformation[:])
                    transformPls.append(tempFinTransformation)
            newList = []
            for a in transformPls:
                for b in a:
                    if b not in newList:
                        newList.append(b)
            thisList.append(newList)
    return thisList

def getAttributes(currPair, checkPair, pair, Ax, Bx, set1, set2) :
    A = Ax[:]
    B = Bx[:]
    transformations = []
    #calculate areas first
    area1 = 0
    area2 = 0
    if(set1[0][0] == 'c') :
        area1 = areaCircle(set1[3])
    elif(set1[0][0] == 'p') :
        points = []
        for i in range(1,len(set1),2) :
            points.append([set1[i],set1[i+1]])
        area1 = area(points)
    if(set2[0][0] == 'c') :
        area2 = areaCircle(set2[3])
    elif(set2[0][0] == 'p') :
        points = []
        for i in range(1,len(set2),2) :
            points.append([set2[i],set2[i+1]])
        area2 = area(points)

    #now we check for differences
    #shapeType/vloc/hloc/size
    #then left_of/right_of and above/below
    #then inside/outside/overlap/contains
    if (set1[0][0] == set2[0][0]):
        if(area1 > area2) :
            transformations.append("change(large(" + currPair[0] + "),small(" + currPair[1] + "))")
        elif(area2 > area1) :
            transformations.append("change(small(" + currPair[0] + "),large(" + currPair[1] + "))")

    for i in range(len(A)) :
        #shapeType, hloc, vloc
        if(i < 3) :
            if(A[i] != B[i]) :
                if(A[i] == "scc" or A[i] == "rectangle" or A[i] == "square" or A[i] == "triangle" or A[i] == "dot" or A[i] == "circle") :
                    transformations.append("change(" + A[i] + "(" + currPair[0] + ")," + B[i] + "(" + currPair[1] + "))")
                else :
                    transformations.append("move(" + A[i] + "(" + currPair[0] + ")," + B[i] + "(" + currPair[1] + "))")
        else :
            #left_of/right_of and above/below
            matchFound = False
            if(A[i] == "right_of") :
                if(A[i+1] == checkPair[0]) :
                    for j in range(len(B)) :
                        if(len(B) <= 3) :
                            break
                        if(B[j] == "left_of") :
                            if(B[j+1] == checkPair[1]) :
                                transformations.append("pos(" + A[i] + "(" + currPair[0] + "," + A[i+1] + ")," + B[j] + "(" + currPair[1] + "," + B[j+1] + "))")
                                matchFound = True
                                del B[j+1]
                                del B[j]
                                break
                        elif(B[j] == "right_of") :
                            if(B[j+1] == checkPair[1]) :
                                matchFound = True
                                del B[j+1]
                                del B[j]
                                break
                if(matchFound == False and A[i+1] == checkPair[0]) :
                    transformations.append("pos(" + A[i] + "(" + currPair[0] + "," + A[i+1] + "),none(" + currPair[1] + "," + checkPair[1] + "))")
            elif(A[i] == "left_of") :
                if(A[i+1] == checkPair[0]) :
                    for j in range(len(B)) :
                        if(len(B) <= 3) :
                            break
                        if(B[j] == "right_of") :
                            if(B[j+1] == checkPair[1]) :
                                transformations.append("pos(" + A[i] + "(" + currPair[0] + "," + A[i+1] + ")," + B[j] + "(" + currPair[1] + "," + B[j+1] + "))")
                                matchFound = True
                                del B[j+1]
                                del B[j]
                                break
                        elif(B[j] == "left_of") :
                            if(B[j+1] == checkPair[1]) :
                                matchFound = True
                                del B[j+1]
                                del B[j]
                                break
                if(matchFound == False and A[i+1] == checkPair[0]) :
                    transformations.append("pos(" + A[i] + "(" + currPair[0] + "," + A[i+1] + "),none(" + currPair[1] + "," + checkPair[1] + "))")
            elif(A[i] == "above") :
                if(A[i+1] == checkPair[0]) :
                    for j in range(len(B)) :
                        if(len(B) <= 3) :
                            break
                        if(B[j] == "below") :
                            if(B[j+1] == checkPair[1]) :
                                transformations.append("pos(" + A[i] + "(" + currPair[0] + "," + A[i+1] + ")," + B[j] + "(" + currPair[1] + "," + B[j+1] + "))")
                                matchFound = True
                                del B[j+1]
                                del B[j]
                                break
                        elif(B[j] == "above") :
                            if(B[j+1] == checkPair[1]) :
                                matchFound = True
                                del B[j+1]
                                del B[j]
                                break
                if(matchFound == False and A[i+1] == checkPair[0]) :
                    transformations.append("pos(" + A[i] + "(" + currPair[0] + "," + A[i+1] + "),none(" + currPair[1] + "," + checkPair[1] + "))")
            elif(A[i] == "below") :
                if(A[i+1] == checkPair[0]) :
                    for j in range(len(B)) :
                        if(len(B) <= 3) :
                            break
                        if(B[j] == "above") :
                            if(B[j+1] == checkPair[1]) :
                                transformations.append("pos(" + A[i] + "(" + currPair[0] + "," + A[i+1] + ")," + B[j] + "(" + currPair[1] + "," + B[j+1] + "))")
                                matchFound = True
                                del B[j+1]
                                del B[j]
                                break
                        elif(B[j] == "below") :
                            if(B[j+1] == checkPair[1]) :
                                matchFound = True
                                del B[j+1]
                                del B[j]
                                break
                if(matchFound == False and A[i+1] == checkPair[0]) :
                    transformations.append("pos(" + A[i] + "(" + currPair[0] + "," + A[i+1] + "),none(" + currPair[1] + "," + checkPair[1] + "))")
            elif(A[i] == "overlap" or A[i] == "contains" or A[i] == "inside" or A[i] == "outside") :
                if(A[i+1] == checkPair[0]) :
                    for j in range(1,len(B),2) :
                        if(len(B) <= 3) :
                            break
                        if(B[j+1] == checkPair[1]) :
                            if(A[i] == B[j]) :
                                matchFound = True
                                del B[j+1]
                                del B[j]
                                break
                            elif(B[j] == "overlap") :
                                matchFound = True
                                transformations.append("pos(" + A[i] + "(" + currPair[0] + "," + A[i+1] + ")," + B[j] + "(" + currPair[1] + "," + B[j+1] + "))")
                                del B[j+1]
                                del B[j]
                                break
                            elif(B[j] == "contains") :
                                matchFound = True
                                transformations.append("pos(" + A[i] + "(" + currPair[0] + "," + A[i+1] + ")," + B[j] + "(" + currPair[1] + "," + B[j+1] + "))")
                                del B[j+1]
                                del B[j]
                                break
                            elif(B[j] == "inside") :
                                matchFound = True
                                transformations.append("pos(" + A[i] + "(" + currPair[0] + "," + A[i+1] + ")," + B[j] + "(" + currPair[1] + "," + B[j+1] + "))")
                                del B[j+1]
                                del B[j]
                                break
                            elif(B[j] == "outside") :
                                matchFound = True
                                transformations.append("pos(" + A[i] + "(" + currPair[0] + "," + A[i+1] + ")," + B[j] + "(" + currPair[1] + "," + B[j+1] + "))")
                                del B[j+1]
                                del B[j]
                                break
                if(matchFound == False and A[i+1] == checkPair[0]) :
                    transformations.append("pos(" + A[i] + "(" + currPair[0] + "," + A[i+1] + "),none(" + currPair[1] + "," + checkPair[1] + "))")

    del B[0:3]
    for i in range(0,len(B)-1,1) :
        if(B[i+1] == checkPair[1]) :
            if(B[i] == "large" or B[i] == "small") :
                transformations.append("change(none(" + currPair[0] + ")," + B[i] + "(" + currPair[1] + "))")
            elif(B[i] == "overlap" or B[i] == "contains" or B[i] == "inside" or B[i] == "outside" or B[i] == "above" or B[i] == "below" or B[i] == "right_of" or B[i] == "left_of"):
                transformations.append("pos(none(" + currPair[0] + "," + checkPair[0] + ")," + B[i] + "(" + currPair[1] + "," + checkPair[1] + "))")

    return transformations

def getTransformation2(A, B) :
    #iterate through all combinations of transforms
    currBest = []
    bestA = []
    bestB = []

    worstPenalty = 10000000
    firstOrderLength = 1000
    for i in A :
        for j in B :
            #iterate through every possible pair in a specific set of transforms
            Alist = []
            Blist = []
            for k in i[0] :
                Alist.append(k)
            for k in j[0] :
                Blist.append(k)

            tempMatch = []
            pairs = [zip(x,Blist) for x in itertools.permutations(Alist,len(Blist))]
            for pair in pairs :
                tempMatch.append(list(pair))
            #lists of attributes for easier parsing
            iAttributes = []
            jAttributes = []

            for k in range(1,len(i),1) :
                split = re.split('\\=|,0,|\\,|\\(|\\)|\\[|\\]|\\:| ', i[k])
                split = list(filter(None,split))
                iAttributes.append(split)
            for k in range(1,len(j),1) :
                split = re.split('\\=|,0,|\\,|\\(|\\)|\\[|\\]|\\:| ', j[k])
                split = list(filter(None,split))
                jAttributes.append(split)

            for k in range(len(tempMatch)) :
                #temp attributes so we can delete from it
                numDeleted = 0
                tempIattributes = iAttributes[:]
                tempJattributes = jAttributes[:]
                allPairs = []

                for l in range(len(tempMatch[k])) :
                    allPairs.append([tempMatch[k][l][0][0],tempMatch[k][l][1][0]])
                    allPairs.append([tempMatch[k][l][0][1],tempMatch[k][l][1][1]])
                pairTransform = []
                tempPenalty = 0

                for l in range(len(tempIattributes)) :
                    #we have 4 cases:
                    #add/del
                    #change (small/large, shape changes)
                    #move (top/bottom, left/right)
                    #pos (right_of/left_of, above/below, overlap/inside/outside/contains)
                    #pos can have "none" also
                    pairFound = False
                    for s in range(len(tempJattributes)) :
                        if(tempIattributes[l][0] == tempJattributes[s][0]) :
                            #case match, we need to split into 4 cases
                            if(tempIattributes[l][0] == "addt" or tempIattributes[l][0] == "delt") :
                                for p in range(0,len(allPairs),2) :
                                    if(tempIattributes[l][1] == allPairs[p][0]) :
                                        for ye in range(0,len(allPairs),2):
                                            if(tempJattributes[s][1] == allPairs[ye][1]) :
                                                pairFound = True
                                                del tempJattributes[s]
                                                numDeleted += 1
                                                break
                                if(pairFound) :
                                    break
                                else :
                                    break
                            elif(tempIattributes[l][0] == "change" or tempIattributes[l][0] == "move") :
                                if(tempIattributes[l][1] == tempJattributes[s][1] and tempIattributes[l][3] == tempJattributes[s][3]) :
                                    for p in range(0, len(allPairs), 2) :
                                        if(tempIattributes[l][2] == allPairs[p][0]) :
                                            for ye in range(0,len(allPairs),2):
                                                if(tempJattributes[s][2] == allPairs[ye][1]) :
                                                    if(tempIattributes[l][4] == allPairs[p+1][0]) :
                                                        if(tempJattributes[s][4] == allPairs[ye+1][0]) :
                                                            pairFound = True
                                                            del tempJattributes[s]
                                                            numDeleted += 1
                                                            break
                                        if(pairFound) :
                                            break
                                if(pairFound) :
                                    break
                                else :
                                    break
                            elif(tempIattributes[l][0] == "pos") :
                                if(tempIattributes[l][1] == tempJattributes[s][1] and tempIattributes[l][4] == tempJattributes[s][4]) :
                                    for p in range(0, len(allPairs), 2) :
                                        if tempIattributes[l][2] == allPairs[p][0] and tempIattributes[l][5] == allPairs[p+1][0] and tempJattributes[s][2] == allPairs[p][1] and tempJattributes[s][5] == allPairs[p+1][1]:
                                            for pa in range(0, len(allPairs),2) :
                                                if tempIattributes[l][3] == allPairs[pa][0] and tempIattributes[l][6] == allPairs[pa+1][0] and tempJattributes[s][3] == allPairs[pa][1] and tempJattributes[s][6] == allPairs[pa+1][1]:
                                                    pairFound = True
                                                    del tempJattributes[s]
                                                    numDeleted += 1
                                                    break
                                    if pairFound == True:
                                        break

                    if(pairFound) :
                        continue
                    else :
                        if(tempIattributes[l][0] == "change") :
                            if(tempIattributes[l][1] == "small" or tempIattributes[l][1] == "large")  :
                                tempPenalty += 1
                            else :
                                tempPenalty += 10000
                        elif(tempIattributes[l][0] == "move") :
                            tempPenalty += 10
                        elif(tempIattributes[l][0] == "pos") :
                            tempPenalty += 100
                        elif(tempIattributes[l][0] == "addt" or tempIattributes[l][0] == "delt") :
                            tempPenalty += 1000
                        pairTransform.append("remove(" + str(tempIattributes[l]) + ")")

                for z in range(len(tempJattributes)) :
                    if(tempJattributes[z][0] == "change") :
                        if(tempJattributes[z][1] == "small" or tempJattributes[z][1] == "large")  :
                            tempPenalty += 1
                        else :
                            tempPenalty += 10000
                    elif(tempJattributes[z][0] == "move") :
                        tempPenalty += 10
                    elif(tempJattributes[z][0] == "pos") :
                        tempPenalty += 100
                    elif(tempJattributes[z][0] == "addt" or tempJattributes[z][0] == "delt") :
                        tempPenalty += 1000
                    pairTransform.append("add(" + str(tempJattributes[z]) + ")")

                if(worstPenalty > tempPenalty) :
                    currBest = pairTransform[:]
                    worstPenalty = tempPenalty
                    firstOrderLength = len(i) + len(j)
                    bestA = i[:]
                    bestB = j[:]
                elif(worstPenalty == tempPenalty) :
                    if(firstOrderLength > (len(i) + len(j))) :
                        currBest = pairTransform[:]
                        worstPenalty = tempPenalty
                        firstOrderLength = len(i) + len(j)
                        bestA = i[:]
                        bestB = j[:]

    return([worstPenalty, bestA, bestB, currBest])

def determineAnswer(costs) :
    biggestCost = 1000000
    costList = []
    for i in costs :
        costList.append(i[0])
        if(biggestCost > i[0]) :
            biggestCost = i[0]

    indices = [l for l, x in enumerate(costList) if x == biggestCost]

    currBest = indices[0]
    for i in range(1,len(indices),1) :
        firstCostOld = len(costs[currBest][1]) + len(costs[currBest][2])
        firstCostNew = len(costs[indices[i]][1]) + len(costs[indices[i]][2])
        if(firstCostOld > firstCostNew) :
            currBest = indices[i]

    #print("T(T(A,B),T(C,K))")
    #print(costs[currBest][3])
    #print("T(A,B)")
    #print(costs[currBest][1])
    #print("T(C,K)")
    #print(costs[currBest][2])
    print("K = " + str(currBest+1))

def run() :
    #read input, do a1 and clean up folder
    inputFolder = sys.argv[1]
    outputFolder = 'outputs' # change this to the path where you want to dump your interpretation files from A1

    files = glob.glob(outputFolder + '/*')
    for f in files:
        os.remove(f)

    inputFiles = glob.glob(inputFolder + '/*.txt') # gives a list of paths to all text files in inputFolder
    for filePath in inputFiles:
        filePath = filePath.replace('\\','/') # in windows, glob returns path with '\\' instead of '/'
        main(filePath, outputFolder) # accessing the main function of A1

    #read interpretations and store in these data structures
    A = []
    B = []
    C = []
    K1 = []
    K2 = []
    K3 = []
    K4 = []
    K5 = []

    outputFiles = glob.glob(outputFolder + '/*.txt')
    for filePath in outputFiles :
        filePath = filePath.replace('\\','/')
        a1inputs = re.split('/', filePath)
        a1inputs = list(filter(None, a1inputs))

        #parse the files and store the correct ones in each list
        if(a1inputs[1][0] == 'A') :
            A.append(readInput(filePath))
        if(a1inputs[1][0] == 'B') :
            B.append(readInput(filePath))
        if(a1inputs[1][0] == 'C') :
            C.append(readInput(filePath))
        if(a1inputs[1][0:2] == 'K1') :
            K1.append(readInput(filePath))
        if(a1inputs[1][0:2] == 'K2') :
            K2.append(readInput(filePath))
        if(a1inputs[1][0:2] == 'K3') :
            K3.append(readInput(filePath))
        if(a1inputs[1][0:2] == 'K4') :
            K4.append(readInput(filePath))
        if(a1inputs[1][0:2] == 'K5') :
            K5.append(readInput(filePath))

    #print("A:")
    #print(A)
    #print("\n")
    #print("B:")
    #print(B)
    #print("\n")
    #print("C:")
    #print(C)
    #print("\n")
    #print("K5:")
    #print(K5)
    #print("\n")

    #now we need to make a cost function
    #we need one for file to file
    #another one for transformation to transformation
    #first create every possible matching
    ABmatching = makeMatch(A,B)
    CK1matching = makeMatch(C,K1)
    CK2matching = makeMatch(C,K2)
    CK3matching = makeMatch(C,K3)
    CK4matching = makeMatch(C,K4)
    CK5matching = makeMatch(C,K5)

    #now we have lists containing every possible matching
    #we need to make a physical description of each matching

    #get all the transformations given a matching and the attributes
    ABtransforms = newGetTransformations(ABmatching, A, B)
    CK1transforms = newGetTransformations(CK1matching, C, K1)
    CK2transforms = newGetTransformations(CK2matching, C, K2)
    CK3transforms = newGetTransformations(CK3matching, C, K3)
    CK4transforms = newGetTransformations(CK4matching, C, K4)
    CK5transforms = newGetTransformations(CK5matching, C, K5)

    #final costs of T(T(AB),T(CKx)))
    costs = []

    costs.append(getTransformation2(ABtransforms, CK1transforms))
    costs.append(getTransformation2(ABtransforms, CK2transforms))
    costs.append(getTransformation2(ABtransforms, CK3transforms))
    costs.append(getTransformation2(ABtransforms, CK4transforms))
    costs.append(getTransformation2(ABtransforms, CK5transforms))

    #determine the final answer
    determineAnswer(costs)

run()
