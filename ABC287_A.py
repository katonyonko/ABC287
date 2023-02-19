import io
import sys

_INPUT = """\
6
3
For
Against
For
5
Against
Against
For
Against
For
1
For
"""

sys.stdin = io.StringIO(_INPUT)
case_no=int(input())
for __ in range(case_no):
  N=int(input())
  ans=0
  for i in range(N):
    if input()=='For': ans+=1
  if ans>N//2: print('Yes')
  else: print('No')