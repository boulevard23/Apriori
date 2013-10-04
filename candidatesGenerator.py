from __future__ import division
from collections import defaultdict
import time

class CandidatesGenerator:

  def __init__(self, fileName, minSupport):
    self.formattedInputData = self.getOriData(fileName)
    self.minSupport = minSupport
    self.candidates = []

  def getOriData(self, fileName):
    oriData = []
    with open(fileName, 'r') as file:
      for line in file:
        oriData.append(line.strip().split('\t')[1:])

    # Convert all the string original data to int data
    result = []
    for row in oriData:
      tmp = []
      for i in range(len(row)):
        if row[i] == 'UP':
          tmp.append(i * 2)
        elif row[i] == 'Down':
          tmp.append(i * 2 + 1)
        elif row[i] == 'ALL':
          tmp.append(200)
        elif row[i] == 'AML':
          tmp.append(201)
        elif row[i] == 'Breast Cancer':
          tmp.append(202)
        elif row[i] == 'Colon Cancer':
          tmp.append(203)
      result.append(tmp)

    return result

  def generateAllCandidates(self):
    # generate the first round
    candidates = defaultdict(self.count)

    for row in self.formattedInputData:
      for i in row:
        candidates[i] += 1

    #print len(candidates)
    candidates = {key: value for key, value in candidates.items() if value/len(self.formattedInputData) >= self.minSupport}
    #print len(candidates)

    tmp = [(k, ) for k in candidates.keys()]
    self.candidates.extend(tmp)
    self.boolInputData = [self.fillBool(row) for row in self.formattedInputData]
    while len(tmp) > 0:
      tmp = self.generateCandidates(tmp)

    return self.candidates

  def generateCandidates(self, oldList):
    newList = []
    oldList.sort()
    for i in range(len(oldList)):
      for j in range(i + 1, len(oldList)):
        if oldList[i][:-1] == oldList[j][:-1]:
          if oldList[i][-1] < oldList[j][-1] + 1:
            tmp = oldList[i] + (oldList[j][-1], )
            newList.append(tmp)
        else:
          break

    #print 'old: ', len(newList)
    #if len(newList) > 0 and len(newList[0]) > 2:
      #newList = [item for item in newList if delInfrequent(tmpData, item)]
    #print 'mid: ', len(newList)
    #newList = [item for item in newList if self.checkMinSupport(item)]
    newList = self.filter(newList)
    #newList = checkMinSupport3(oriData, newList, minSupport)
    #print 'new: ', len(newList)

    self.candidates.extend(newList)
    return newList
    #generateCandidates(newList, oriData, minSupport, result)

  #def delInfrequent(smallList, item):
    #setList = set(smallList)
    #combos = itertools.combinations(list(item), len(item) - 1)
    #for e in combos:
      #if e not in setList:
        #return False
    #return True

  def filter(self, oldList):
    newList = [item for item in oldList if self.checkMinSupport(item)]
    return newList

  # Using python's 'in' keyword to check the frequent of an item set
  def checkMinSupport2(self, item):
    size = len(self.formattedInputData)
    print size
    count = 0

    for row in self.formattedInputData:
      flag = True
      for i in item:
        if i not in row:
          flag = False
      if flag:
        count += 1

    if count/size < self.minSupport:
      return False
    else:
      return True

  # Using sieve to check the frequent of an item set
  def checkMinSupport(self, item):
    #size = len(self.boolInputData)
    #count = 0

    #for row in self.boolInputData:
      #flag = True
      #for i in item:
        #if row[i] is False:
          #flag = False
          #break
      #if flag:
        #count += 1

    frequent = self.getFrequent(item)

    if frequent < self.minSupport:
      return False
    else:
      return True

  def fillBool(self, row):
    result = [False] * 204
    for item in row:
      result[item] = True
    return result
    #print result

  def count(self):
    return 0

  def getFrequent(self, item):
    size = len(self.boolInputData)
    count = 0

    for row in self.boolInputData:
      flag = True
      for i in item:
        if row[i] is False:
          flag = False
          break
      if flag:
        count += 1

    return count/size


if __name__ == '__main__':
  start = time.time()
  generator = CandidatesGenerator('association-rule-test-data.txt', 0.3)
  result = generator.generateAllCandidates()
  print len(result)
  print 'execute time: ', time.time() - start
