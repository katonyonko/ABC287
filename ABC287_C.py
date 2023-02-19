import io
import sys

_INPUT = """\
6
4 3
1 3
4 2
3 2
2 0
5 5
1 2
2 3
3 4
4 5
5 1
"""

sys.stdin = io.StringIO(_INPUT)
case_no=int(input())
for __ in range(case_no):
  #DFS
  def dfs(G,r=0):
      used=[1]*len(G)
      parent=[-1]*len(G)
      st=[]
      st.append(r)
      while st:
          x=st.pop()
          if used[x]==0:
              continue
          used[x]=0
          for v in G[x]:
              if v==parent[x]:
                  continue
              parent[v]=x
              st.append(v)
      return used

  N,M=map(int,input().split())
  G=[[] for _ in range(N)]
  for i in range(M):
    u,v=map(lambda x: int(x)-1, input().split())
    G[u].append(v)
    G[v].append(u)
  if M!=N-1: print('No')
  else:
    tmp=[0]*2
    for i in range(N):
      if 0<len(G[i])<3:
        tmp[len(G[i])-1]+=1
    if tmp[0]==2 and tmp[1]==N-2:
      s=0
      for i in range(N):
        if len(G[i])==1: s=i; break
      ans=sum(dfs(G,s))
      if ans==0: print('Yes')
      else: print('No')
    else: print('No')