from __future__ import division
import itertools
from collections import namedtuple
from collections import defaultdict
import time
import Queue

class Trie():

  def __init__(self):
    self.tree = {}

  def add(self, *nodes):
    if len(nodes) == 1:
      self.tree[nodes[0]] = {}
    else:
      try:
        children = self.tree[nodes[0]]
        for node in nodes[1:-1]:
          children = children[node]
      except KeyError:
        return

      children[nodes[-1]] = {}

  # Need to check if it works
  def findPath(self, nodes):
    try:
      children = self.tree[nodes[0]]
      for node in nodes[1:]:
        children = children[node]
    except KeyError:
      return None
    return children

  def keys(self):
    return self.tree.keys()

  def __getitem__(self, key):
    return self.tree[key]

  def __setitem__(self, key, value):
    self.tree[key] = value

  def __str__(self):
    return 'Tree: %s' % self.tree

def checkInfrequent(t, nodes):
  #print 'nodes2: ', nodes
  combinations = itertools.combinations(nodes, len(nodes) - 1)
  for elem in combinations:
    if t.findPath(list(elem)) is None:
      return False
  return True

#def checkSupport(t, nodes):

def generateCandidates(t, queue):
  if len(queue) == 0:
    leafs = list(t.keys())
    leafs.sort()
    for i in range(len(leafs)):
      for j in range(i + 1, len(leafs)):
        if leafs[i][0] < leafs[j][0]:
          t[leafs[i]][leafs[j]] = {}
      if len(t[leafs[i]]) > 1:
        tmpPath = [leafs[i], t[leafs[i]]]
        queue.append(tmpPath)
  else:
    path = queue.pop(0)
    parent = path[-1]
    leafs = list(parent.keys())
    leafs.sort()
    for i in range(len(leafs)):
      for j in range(i + 1, len(leafs)):
        if leafs[i][0] < leafs[j][0]:
          tmpPath1 = path[:-1]
          tmpPath1.extend([leafs[i], leafs[j]])
          if checkInfrequent(t, tmpPath1):
            parent[leafs[i]][leafs[j]] = {}
      if len(parent[leafs[i]]) > 1:
        tmpPath2 = path[:-1]
        tmpPath2.extend([leafs[i], parent[leafs[i]]])
        queue.append(tmpPath2)

def count():
  return 0

def getOriData(fileName):
  oriData = []
  with open(fileName, 'r') as file:
    for line in file:
      oriData.append(line.strip().split('\t')[1:-1])

  result = []
  for row in oriData:
    tmp = []
    for i in range(len(row)):
      if row[i] == 'UP':
        tmp.append(i * 2)
      else:
        tmp.append(i * 2 + 1)
    result.append(tmp)

  return result

if __name__ == '__main__':
  t = Trie()

  Gene = namedtuple('Gene', ['name', 'arrow'])
  oriData = getOriData('association-rule-test-data.txt')
  #print 'oriData: ', oriData
  #print 'a' + 'b'
  with open('test.dat', 'a') as f:
    for row in oriData:
      for i in range(len(row)):
        if row[i] == 'UP':
          f.write(str(i * 2) + ' ')
        else:
          f.write(str(i * 2 + 1) + ' ')
      f.write('\n')

  minSupport = 0.8

  #print oriData

  candidates = defaultdict(count)

  #for row in oriData:
    #for i in range(len(row)):
      #key = Gene('G' + str(i + 1), row[i])
      #candidates[key] += 1

  #print len(candidates)
  #candidates = {key: value for key, value in candidates.items() if value/len(oriData) > minSupport}
  #print len(candidates)
  for row in oriData:
    for i in range(10):
      key = Gene('G' + str(i + 1), row[i])
      candidates[key] += 1

  print len(candidates)
  candidates = {key: value for key, value in candidates.items() if value/len(oriData) > minSupport}
  print len(candidates)

  #for k in candidates.keys():
    #t.add(k)
  #t.add(Gene('G1', 'UP'))
  #t.add(Gene('G2', 'DOWN'))
  #t.add(Gene('G2', 'DOWN'), Gene('G3', 'UP'))
  #t.add(Gene('G1', 'UP'), Gene('G4', 'DOWN'))
  #t.add(Gene('G2', 'UP'), Gene('G4', 'DOWN'))
  #t.add(Gene('G2', 'DOWN'), Gene('G3', 'UP'), Gene('G4', 'DOWN'))
  #t.add(Gene('G2', 'DOWN'), Gene('G1', 'UP'), Gene('G5', 'UP'))
  #t.add(Gene('G2', 'DOWN'), Gene('G4', 'DOWN'))

  #t.add((('G1', 'UP'),))
  #t.add((('G2', 'DOWN'),))
  #t.add((('G2', 'DOWN'), ('G3', 'UP')))
  #t.add((('G1', 'UP'), ('G4', 'DOWN')))
  #t.add((('G2', 'UP'), ('G4', 'DOWN')))
  #t.add((('G2', 'DOWN'), ('G3', 'UP'), ('G4', 'DOWN')))
  #t.add((('G2', 'DOWN'), ('G1', 'UP'), ('G5', 'UP')))
  #t.add((('G2', 'DOWN'), ('G4', 'DOWN')))

  #t.add(Gene('G1', 'UP'))
  #t.add(Gene('G1', 'DOWN'))
  #t.add(Gene('G2', 'UP'))
  #t.add(Gene('G2', 'DOWN'))
  #t.add(Gene('G3', 'UP'))
  #t.add(Gene('G4', 'DOWN'))
  #t.add(Gene('G5', 'UP'))
  #t.add(Gene('G5', 'DOWN'))
  #t.add(Gene('G6', 'UP'))
  #t.add(Gene('G6', 'DOWN'))
  #t.add(Gene('G7', 'UP'))
  #t.add(Gene('G7', 'DOWN'))
  #t.add(Gene('G8', 'UP'))
  #t.add(Gene('G8', 'DOWN'))
  #t.add(Gene('G9', 'UP'))
  #t.add(Gene('G9', 'DOWN'))
  #t.add(Gene('G10', 'UP'))
  #t.add(Gene('G10', 'DOWN'))
  #t.add(Gene('G11', 'UP'))
  #t.add(Gene('G11', 'DOWN'))
  #t.add(Gene('G12', 'UP'))
  #t.add(Gene('G12', 'DOWN'))
  #t.add(Gene('G13', 'UP'))
  #t.add(Gene('G13', 'DOWN'))
  #t.add(Gene('G14', 'UP'))
  #t.add(Gene('G14', 'DOWN'))
  #t.add(Gene('G15', 'UP'))
  #t.add(Gene('G15', 'DOWN'))



  #print t

  q = []
  generateCandidates(t, q)

  iterRound = 1
  #prune(t, iterRound)
  #print 'first queue: ', q

  start_time = time.time()
  while len(q) > 0:
    #print q
    if len(q[0]) - 1 == iterRound:
      #print q
      generateCandidates(t, q)
      #print 'generate'
    else:
      #print len(q[0]) - 1
      iterRound = len(q[0]) - 1
      #prune(t, iterRound)
    #print '************queue***********'
    #print t
  #print t
  print time.time() - start_time, 'seconds'
