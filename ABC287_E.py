import io
import sys

_INPUT = """\
6
3
abc
abb
aac
11
abracadabra
bracadabra
racadabra
acadabra
cadabra
adabra
dabra
abra
bra
ra
a
"""

sys.stdin = io.StringIO(_INPUT)
case_no=int(input())
for __ in range(case_no):
  from collections import defaultdict
  N=int(input())
  S=[input() for _ in range(N)]
  T=sorted([(S[i],i) for i in range(N)])
  S.sort()
  node=0
  d=[set() for _ in range(5*10**5+1)]
  d2=[-1]*N
  d3={}
  parent=[-1]*(5*10**5+1)
  for i in range(N):
    now=0
    for j in range(len(S[i])):
      if S[i][j] in d[now]:
        now=d3[(now,S[i][j])]
      else:
        node+=1
        d[now].add(S[i][j])
        d3[(now,S[i][j])]=node
        parent[node]=now
        now=node
      if j==len(S[i])-1:
        d2[i]=now
  from collections import Counter
  tmp=Counter(d2)
  ans=[0]*N
  for i in range(N):
    if len(d[d2[i]])>0 or tmp[d2[i]]>1: ans[T[i][1]]=len(S[i])
    else:
      ans2=len(S[i])-1
      now=d2[i]
      while parent[now]!=-1 and parent[now] not in tmp and len(d[parent[now]])==1:
        ans2-=1
        now=parent[now]
      ans[T[i][1]]=ans2
  for i in range(N): print(ans[i])
  # print(d[:10],d2,d3)