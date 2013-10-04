from collections import defaultdict

def tree():
  return defaultdict()

def f():
  return 0

if __name__ == '__main__':
  a = tree()
  a[('G1', 'UP')]
  a[50][40]
  a[50][70]
  a[60]

  b = {(1, 2): 1, (2, 3): 2}
  print b[(1, 2)]
