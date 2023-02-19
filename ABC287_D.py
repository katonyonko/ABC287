import io
import sys

_INPUT = """\
6
a?c
b?
atcoder
?????
beginner
contest
f??df
?fff
"""

sys.stdin = io.StringIO(_INPUT)
case_no=int(input())
for __ in range(case_no):
  S=input()
  T=input()
  forward=10**20
  backward=10**20
  for i in range(len(T)):
    if S[i]!=T[i] and S[i]!='?' and T[i]!='?': forward=i; break
  for i in range(len(T)):
    if S[-i-1]!=T[-i-1] and S[-i-1]!='?' and T[-i-1]!='?': backward=i; break
  for i in range(len(T)+1):
    if i<=forward and len(T)-i<=backward: print('Yes')
    else: print('No')