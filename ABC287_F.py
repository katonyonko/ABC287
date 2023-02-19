import io
import sys

_INPUT = """\
6
4
1 2
2 3
3 4
2
1 2
10
3 4
3 6
6 9
1 3
2 4
5 6
6 10
1 8
5 7
"""

sys.stdin = io.StringIO(_INPUT)
case_no=int(input())
for __ in range(case_no):
  mod=998244353
  N=int(input())
  G=[[] for _ in range(N)]
  for _ in range(N-1):
    a,b=map(lambda x:int(x)-1,input().split())
    G[a].append(b)
    G[b].append(a)

  def dfs(G,r=0):
    used=[False]*len(G)
    parent=[-1]*len(G)
    st=[]
    st.append(r)
    while st:
        x=st.pop()
        if used[x]==True:
            continue
        used[x]=True
        for v in G[x]:
            if v==parent[x]:
                continue
            parent[v]=x
            st.append(v)
    return parent

  from collections import deque
  def bfs(G,s):
    inf=10**30
    D=[inf]*len(G)
    D[s]=0
    dq=deque()
    dq.append(s)
    while dq:
      x=dq.popleft()
      for y in G[x]:
        if D[y]>D[x]+1:
          D[y]=D[x]+1
          dq.append(y)
    return D

  parent=dfs(G,0)
  D=bfs(G,0)
  D=sorted([(D[i],i) for i in range(N)],reverse=True)
  ans=[None for _ in range(N)]
  for i in range(N):
    s=D[i][1]
    dp=[0]*4
    dp[0]=1
    dp[3]=1
    for u in G[s]:
      if u==parent[s]: continue
      tmp2=ans[u]
      tmp=[0]*(len(dp)+len(tmp2)-2)
      for i in range(len(dp)//2):
        for j in range(len(tmp2)//2):
          tmp[(i+j)*2]=(tmp[(i+j)*2]+dp[i*2]*tmp2[j*2])%mod
          tmp[(i+j)*2]=(tmp[(i+j)*2]+dp[i*2]*tmp2[j*2+1])%mod
          tmp[(i+j)*2+1]=(tmp[(i+j)*2+1]+dp[i*2+1]*tmp2[j*2])%mod
          if i+j>0: tmp[(i+j-1)*2+1]=(tmp[(i+j-1)*2+1]+dp[i*2+1]*tmp2[j*2+1])%mod
      dp=tmp
    ans[s]=dp.copy()

  print(*[sum(ans[0][i*2:(i+1)*2])%mod for i in range(1,N+1)],sep='\n')