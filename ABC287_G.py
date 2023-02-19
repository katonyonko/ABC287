import io
import sys

_INPUT = """\
2
3
1 1
2 2
3 3
7
3 4
1 1 10
3 4
2 1 0
2 3 0
3 4
3 2
4
11
19
-1
4
2
2 3
2 1
1
3 2
1
4
"""

#ここから下を提出
class segtree():
  n=1
  size=1
  log=2
  d=[0]
  op=None
  e=10**15
  def __init__(self,V,OP,E):
      self.n=len(V)
      self.op=OP
      self.e=E
      self.log=(self.n-1).bit_length()
      self.size=1<<self.log
      self.d=[E for i in range(2*self.size)]
      for i in range(self.n):
          self.d[self.size+i]=V[i]
      for i in range(self.size-1,0,-1):
          self.update(i)
  def set(self,p,x):
      assert 0<=p and p<self.n
      p+=self.size
      self.d[p]=x
      for i in range(1,self.log+1):
          self.update(p>>i)
  def get(self,p):
      assert 0<=p and p<self.n
      return self.d[p+self.size]
  def prod(self,l,r):
      assert 0<=l and l<=r and r<=self.n
      sml=self.e
      smr=self.e
      l+=self.size
      r+=self.size
      while(l<r):
          if (l&1):
              sml=self.op(sml,self.d[l])
              l+=1
          if (r&1):
              smr=self.op(self.d[r-1],smr)
              r-=1
          l>>=1
          r>>=1
      return self.op(sml,smr)
  def all_prod(self):
      return self.d[1]
  def max_right(self,l,f):
      assert 0<=l and l<=self.n
      assert f(self.e)
      if l==self.n:
          return self.n
      l+=self.size
      sm=self.e
      while(1):
          while(l%2==0):
              l>>=1
          if not(f(self.op(sm,self.d[l]))):
              while(l<self.size):
                  l=2*l
                  if f(self.op(sm,self.d[l])):
                      sm=self.op(sm,self.d[l])
                      l+=1
              return l-self.size
          sm=self.op(sm,self.d[l])
          l+=1
          if (l&-l)==l:
              break
      return self.n
  def min_left(self,r,f):
      assert 0<=r and r<=self.n
      assert f(self.e)
      if r==0:
          return 0
      r+=self.size
      sm=self.e
      while(1):
          r-=1
          while(r>1 & (r%2)):
              r>>=1
          if not(f(self.op(self.d[r],sm))):
              while(r<self.size):
                  r=(2*r+1)
                  if f(self.op(self.d[r],sm)):
                      sm=self.op(self.d[r],sm)
                      r-=1
              return r+1-self.size
          sm=self.op(self.d[r],sm)
          if (r& -r)==r:
              break
      return 0
  def update(self,k):
      self.d[k]=self.op(self.d[2*k],self.d[2*k+1])
  def __str__(self):
      return str([self.get(i) for i in range(self.n)])

def solve(N,cards,Q,query):
  score=sorted(list(set([cards[i][0] for i in range(N)]+[query[i][2] for i in range(Q) if query[i][0]==1])))
  ans=[]
  dic={score[i]:i for i in range(len(score))}
  count_ini=[0 for i in range(len(score))]
  score_ini=[0 for i in range(len(score))]
  for i in range(N):
    a,b=cards[i]
    count_ini[dic[a]]+=b
    score_ini[dic[a]]+=a*b
  st_count=segtree(count_ini,(lambda x,y: x+y),0)
  st_score=segtree(score_ini,(lambda x,y: x+y),0)
  for i in range(Q):
    if query[i][0]==1:
      x,y=query[i][1:]
      x-=1
      a,b=cards[x]
      from_id=dic[a]
      to_id=dic[y]
      cards[x][0]=y
      st_count.set(from_id,st_count.get(from_id)-b)
      st_count.set(to_id,st_count.get(to_id)+b)
      st_score.set(from_id,st_score.get(from_id)-a*b)
      st_score.set(to_id,st_score.get(to_id)+y*b)
    elif query[i][0]==2:
      x,y=query[i][1:]
      x-=1
      a,b=cards[x]
      id=dic[a]
      cards[x][1]=y
      st_count.set(id,st_count.get(id)+y-b)
      st_score.set(id,st_score.get(id)+a*(y-b))
    else:
      x=query[i][1]
      l=st_count.min_left(len(score), lambda func: func<=x)
      if st_count.all_prod()<x: ans.append(-1)
      else:
        if l>0: ans.append(st_score.prod(l,len(score))+score[l-1]*(x-st_count.prod(l,len(score))))
        else: ans.append(st_score.prod(l,len(score)))
  return ans

def simple_solution(N,cards,Q,query):
  ans=[]
  for i in range(Q):
    if query[i][0]==1:
      x,y=query[i][1:]
      x-=1
      cards[x][0]=y
    elif query[i][0]==2:
      x,y=query[i][1:]
      x-=1
      cards[x][1]=y
    else:
      x=query[i][1]
      tmp=sorted(cards,reverse=True)
      cnt=0
      now=0
      ans2=0
      if sum([cards[i][1] for i in range(N)])<x: ans.append(-1)
      else:
        while now<N and cnt+tmp[now][1]<=x:
          ans2+=tmp[now][0]*tmp[now][1]
          cnt+=tmp[now][1]
          now+=1
        if cnt<x: ans2+=tmp[now][0]*(x-cnt)
        ans.append(ans2)
  return ans

from random import randint
def random_case():
  N=randint(1,10)
  cards=[[randint(0,10),randint(0,10)] for _ in range(N)]
  Q=randint(1,10)
  query=[]
  for i in range(Q):
    d=randint(1,3)
    if d<=2: x,y=randint(1,N),randint(0,10); query.append([d,x,y])
    else: x=randint(1,20); query.append([d,x])
  return N,cards,Q,query

def read_input():
  N=int(input())
  cards=[list(map(int,input().split())) for _ in range(N)]
  Q=int(input())
  query=[list(map(int,input().split())) for _ in range(Q)]
  return N,cards,Q,query

def read_output():
  res=[]
  l=int(input())
  for i in range(l): res.append(int(input()))
  return res

def output(ans):
  for i in range(len(ans)):
    print(ans[i])

def test():
  sys.stdin = io.StringIO(_INPUT)
  case_no=int(input())
  for i in range(case_no):
    sol=solve(*read_input())
    ans=read_output()
    if sol!=ans:
      print(sol)
      print(ans)

def main():
  ans=solve(*read_input())
  output(ans)

from copy import deepcopy
def random_test():
  while True:
    N,cards,Q,query=random_case()
    N2=N
    cards2=deepcopy(cards)
    Q2=Q
    query2=deepcopy(query)
    a=solve(N,cards,Q,query)
    b=simple_solution(N2,cards2,Q2,query2)
    if a!=b:
      print(N)
      for i in range(N): print(*cards[i])
      print(Q)
      for i in range(Q): print(*query[i])
      print(a)
      print(b)
      break

if __name__ == "__main__":
  flg=1
  if flg==0: main()
  elif flg==1: test()
  else: simple_solution()
