import io
import sys

_INPUT = """\
6
3 3
142857
004159
071028
159
287
857
5 4
235983
109467
823476
592801
000333
333
108
467
983
4 4
000000
123456
987111
000000
000
111
999
111
"""

sys.stdin = io.StringIO(_INPUT)
case_no=int(input())
for __ in range(case_no):
  N,M=map(int,input().split())
  S=[input() for _ in range(N)]
  T=[input() for _ in range(M)]
  ans=0
  for i in range(N):
    tmp=0
    for j in range(M):
      if S[i][3:]==T[j]: tmp=1
    if tmp==1: ans+=1
  print(ans)