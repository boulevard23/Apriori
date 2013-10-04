from __future__ import division
from candidatesGenerator import CandidatesGenerator
from parser import Parser

if __name__ == '__main__':
  minSupport = raw_input('Enter the min support: ')
  print 'Generating all the candidates...'
  generator = CandidatesGenerator('association-rule-test-data.txt', float(minSupport))
  candidates = generator.generateAllCandidates()
  print 'Generated', len(candidates), 'candidates'
  #print len(candidates)

  while(True):
    inputStr = raw_input('Enter the query: ')
    parser = Parser(inputStr)
    #parser = Parser('rule has (3) of (G59_UP, G72_UP, G82_DOWN, G89_UP) or sizeof body >= 2')
    parser.splitTemplates()
    rules = parser.generateRuleForSentence(candidates)

    for logicalWord in parser.logicalWords:
      if logicalWord == 'and':
        rule1 = rules.pop(0)
        rule2 = rules.pop(0)
        new_rule = list(set(tuple(rule1)) & set(tuple(rule2)))
        rules.insert(0, new_rule)
      else:
        rule1 = rules.pop(0)
        rule2 = rules.pop(0)
        new_rule = list(set(tuple(rule1)) | set(tuple(rule2)))
        rules.insert(0, new_rule)

    result = rules[0]

    for rule in result:
      body = rule[0]
      head = rule[1]
      bodyStr = []
      headStr = []
      for item in body:
        if item % 2 == 0:
          bodyStr.append('G' + str(item//2 + 1) + '_UP')
        else:
          bodyStr.append('G' + str((item - 1)//2 + 1) + '_DOWN')
      for item in head:
        if item % 2 == 0:
          headStr.append('G' + str(item//2 + 1) + '_UP')
        else:
          headStr.append('G' + str((item - 1)//2 + 1) + '_DOWN')

      ruleStr = ', '.join(bodyStr) + ' -> ' + ', '.join(headStr)
      a = generator.getFrequent(body + head)
      b = generator.getFrequent(head)
      confidence = a/b
      print ruleStr, '  Min support: ', minSupport, ' confidence: ', format(confidence, '.2f')
