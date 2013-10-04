import re
import itertools

class Parser:

  def __init__(self, inputTxt):
    self.inputTxt = inputTxt
    self.oriSentences = []
    self.logicalWords = []
    self.formattedSentences = []
    self.rulesForSentences = []

  def splitTemplates(self):
    p = re.compile(r'\bAND\b|\bOR\b', re.IGNORECASE)
    self.logicalWords = p.findall(self.inputTxt)
    self.oriSentences = re.split(p, self.inputTxt.upper())

    p = re.compile(r'\([^)]+\)|\S+')
    self.oriSentences = [p.findall(s) for s in self.oriSentences]
    for s in self.oriSentences:
      if s[1] == 'HAS':
        self.formattedSentences.append(self.parseTemplate1(s))
      elif s[0] == 'SIZEOF':
        self.formattedSentences.append(self.parseTemplate2(s))
      else:
        print 'Input format error'

    #print 'AND OR: ', self.logicalWords
    #print 'SENTENCE: ', self.oriSentences

  def generateRuleForSentence(self, candidates):
    #print self.formattedSentences
    for tmpList in self.formattedSentences:
      result = []
      if len(tmpList) == 3:
        filteredCandidates = self.filterByTemplate1(tmpList, candidates)
        for c in filteredCandidates:
          rules = self.generateRules(c)
          rules = self.filterRulesByTemplate1(rules, tmpList)
          result.extend(rules)
      else:
        result = self.generateRules4Template2(tmpList, candidates)

      self.rulesForSentences.append(result)

    return self.rulesForSentences

  def parseTemplate1(self, sentences):
    result = []

    if sentences[0] == 'RULE':
      result.append(0)
    elif sentences[0] == 'BODY':
      result.append(1)
    elif sentences[0] == 'HEAD':
      result.append(2)
    else:
      print 'Input format error'

    if sentences[2] == '(ANY)':
      result.append(1)
    elif sentences[2] == '(NONE)':
      result.append(0)
    else:
      num = re.search(r'\d+', sentences[2]).group()
      result.append(int(num))

    genes = sentences[-1][1:-1].split(', ')

    for i in range(len(genes)):
      if genes[i].endswith('UP'):
        num = re.search(r'\d+', genes[i]).group()
        genes[i] = (int(num) - 1) * 2
      elif genes[i].endswith('DOWN'):
        num = re.search(r'\d+', genes[i]).group()
        genes[i] = (int(num) - 1) * 2 + 1

    result.append(genes)
    return result

  def parseTemplate2(self, sentences):
    result = []

    if sentences[1] == 'RULE':
      result.append(0)
    elif sentences[1] == 'BODY':
      result.append(1)
    elif sentences[1] == 'HEAD':
      result.append(2)
    else:
      print 'Input format error'

    try:
      result.append(int(sentences[-1]))
    except ValueError:
      print 'Input format error'

    #print 'temp2: ', result
    return result

  def filterByTemplate1(self, tmp1List, candidates):
    length = tmp1List[1] if tmp1List[0] == 0 else tmp1List[1] + 1
    regex = self.generateRegex(tmp1List[2], tmp1List[1])
    result = [item for item in candidates if len(self.getRegexResult(' '.join(map(str, item)), regex)) > 0 and len(item) >= length]
    return result

  def generateRules4Template2(self, tmp2List, candidates):
    final_rules = []
    size1 = tmp2List[1]
    if tmp2List[0] == 0:
      for item in candidates:
        if len(item) >= size1:
          rules = self.generateRules(item, tmp=1, part=0, size=size1)
          final_rules.extend(rules)
    elif tmp2List[0] == 1:
      for item in candidates:
        if len(item) >= size1 + 1:
          #print item
          rules = self.generateRules(item, tmp=1, part=1, size=size1)
          final_rules.extend(rules)
    else:
      for item in candidates:
        if len(item) >= size1 + 1:
          rules = self.generateRules(item, tmp=1, part=2, size=size1)
          final_rules.extend(rules)

    #print 'final:', rules
    return final_rules

  def generateRegex(self, items, logicNum):
    s = '\\b|\\b'.join(map(str, items))
    if logicNum == 0:
      return '^((?!.*(\\b' + s + '\\b)).*)$'
    else:
      return '(.*(\\b' + s + '\\b).*){' + str(logicNum) + '}'

  def getRegexResult(self, inputStr, regex):
    p = re.compile(regex)
    return p.findall(inputStr)

  #def filter(self, tmpList, candidates):
    #if len(tmpList) == 3:
      #return self.filterByTemplate1(tmpList, candidates)
    #elif len(tmpList) == 2:
      #return self.filterByTemplate2(tmpList, candidates)
    #else:
      #print 'Input format error'

  # Generate all the combination of rules
  def generateRules(self, tup, tmp=0, size=0, part=0):
    rules = []
    if tmp == 0: # for template 1
      for i in range(1, len(tup)):
        combines = itertools.combinations(list(tup), i)
        for e in combines:
          rules.append((e, tuple(set(tup) - set(e))))
    else:
      if part == 0:
        if len(tup) < size:
          pass
        else:
          for i in range(1, len(tup)):
            combines = itertools.combinations(list(tup), i)
            for e in combines:
              rules.append((e, tuple(set(tup) - set(e))))
      elif part == 1:
        for i in range(size, len(tup)):
          combines = itertools.combinations(list(tup), i)
          for e in combines:
            rules.append((e, tuple(set(tup) - set(e))))
      else:
        for i in range(size, len(tup)):
          combines = itertools.combinations(list(tup), i)
          for e in combines:
            rules.append((tuple(set(tup) - set(e)), e))
    return rules


   #Filter the rules by re-evalutate them using temp1 or temp2
  #def filterRules(self, rules, tmpList):
    #if len(tmpList) == 3:
      #return self.filterRulesByTemplate1(rules, tmpList)
    #else:
      #return self.filterRulesByTemplate2(rules, tmpList)

  def filterRulesByTemplate1(self, rules, tmp1List):
    if tmp1List[0] == 0:
      return rules
    else:
      rules = [item for item in rules if self.checkValidityOfRuleByT1(item[0], item[1], tmp1List)]
      return rules

  def checkValidityOfRuleByT1(self, body, head, tmp1List):
    if tmp1List[0] == 1:   # This is body
      if tmp1List[1] == 0: # has none of
        return True if len(set(tmp1List[2]) & set(body)) == 0 else False # intersection of the input tuple and body is 0
      else:
        return True if len(set(tmp1List[2]) & set(body)) >= tmp1List[1] else False # intersection of the input tuple and body >= input num
    else:                 # This is head
      if tmp1List[1] == 0:
        return True if len(set(tmp1List[2]) & set(head)) == 0 else False # intersection of the input tuple and body is 0
      else:
        return True if len(set(tmp1List[2]) & set(head)) >= tmp1List[1] else False # intersection of the input tuple and body >= input num

if __name__ == '__main__':
  parser = Parser('rule has (1) of (G1_UP, G2_UP, G3_UP, G4_UP) and body has (none) of (G5_DOWN, G6_DOWN, G7_DOWN) or sizeof head >= 4')
  parser.splitTemplates()
