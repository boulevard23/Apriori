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

    print 'AND OR: ', self.logicalWords
    print 'SENTENCE: ', self.oriSentences

  def generateRuleForSentence(self, candidates, tmpList):
    result = []
    for c in candidates:
      rules = self.generateRules(c)
      rules = self.filterRules(rules, tmpList)
      result.extend(self.rulesToStrList(rules))

    self.rulesForSentences.append(result)

  def rulesToStrList(self, rules):
    result = [str(key) + ' -> ' + str(value) for key, value in rules.items()]
    #print result
    return result

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
      try:
        result.append(int(sentences[2][1:-1]))
      except ValueError:
        print 'Input format error'

    genes = sentences[-1][1:-1].split(', ')

    try:
      for i in range(len(genes)):
        if genes[i].endswith('UP'):
          genes[i] = (int(genes[i][1]) - 1) * 2
        elif genes[i].endswith('DOWN'):
          genes[i] = (int(genes[i][1]) - 1) * 2 + 1
    except ValueError:
      print  'Input format error'

    result.append(genes)
    print 'temp1: ', result
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

    print 'temp2: ', result
    return result

  def filterByTemplate1(self, tmp1List, candidates):
    length = tmp1List[1] if tmp1List[0] == 0 else tmp1List[1] + 1
    regex = self.generateRegex(tmp1List[2], tmp1List[1])
    #print 'regex: ', regex
    result = [item for item in candidates if len(self.getRegexResult(' '.join(map(str, item)), regex)) > 0 and len(item) >= length]
    return result

  def filterByTemplate2(self, tmp2List, candidates):
    size1 = tmp2List[1]
    if tmp2List[0] == 0:
      for item in candidates:
        if len(item) >= size1:
          rules = generateRules(item, size=size1)
    elif tmp2List[0] == 1:
      for item in candidates:
        if len(item) >= size1:
          rules = generateRules(item, low=size1)
    else:
      for item in candidates:
        if len(item) >= size1:
          rules = generateRules(item, low=size1, head=True)

  def generateRegex(self, items, logicNum):
    s = '\\b|\\b'.join(map(str, items))
    if logicNum == 0:
      return '^((?!.*(\\b' + s + '\\b)).*)$'
    else:
      return '(.*(\\b' + s + '\\b).*){' + str(logicNum) + '}'

  def getRegexResult(self, inputStr, regex):
    p = re.compile(regex)
    return p.findall(inputStr)

  def filter(self, tmpList, candidates):
    if len(tmpList) == 3:
      return self.filterByTemplate1(tmpList, candidates)
    elif len(tmpList) == 2:
      return self.filterByTemplate2(tmpList, candidates)
    else:
      print 'Input format error'

  # Generate all the combination of rules
  def generateRules(self, tup, low=1, head=False, size=0):
    rules = {}
    for i in range(low, len(tup)):
      combines = itertools.combinations(list(tup), i)
      for e in combines:
        if head: # for head size, need to set both low and head
          rules[tuple(set(tup) - set(e))] = list(e)
        elif len(e) >= size: # if size == 0, it generates all the combinations. else it finds the combinations >= size
          rules[e] = list(set(tup) - set(e))

    return rules

  # Filter the rules by re-evalutate them using temp1 or temp2
  def filterRules(self, rules, tmpList):
    if len(tmpList) == 3:
      return self.filterRulesByTemplate1(rules, tmpList)
    else:
      return self.filterRulesByTemplate2(rules, tmpList)

  def filterRulesByTemplate1(self, rules, tmp1List):
    if tmp1List[0] == 0:
      return rules
    else:
      rules = {key: value for key, value in rules.items() if self.checkValidityOfRuleByT1(key, value, tmp1List)}
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

  def filterRulesByTemplate2(self, rules, tmp2List):
    pass


if __name__ == '__main__':
  parser = Parser('rule has (1) of (G1_UP, G2_UP, G3_UP, G4_UP) and body has (none) of (G5_DOWN, G6_DOWN, G7_DOWN) or sizeof head >= 4')
  parser.splitTemplates()
