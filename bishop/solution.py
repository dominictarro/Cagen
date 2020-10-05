import time
d={c:i+1 for i,c in enumerate('abcdefgh')}
def solution1(a,b,n):
  if n==0:return a==b
  x=abs(d[a[0]]-d[b[0]])
  y=abs(int(a[1])-int(b[1]))
  if n==1:return x==y
  return (x+y)%2==0


def solution(a,b,n):
  if n==0:return a==b
  x=abs(d[a[0]]-d[b[0]])
  y=abs(int(a[1])-int(b[1]))
  if n==1:return x==y
  return x%2==y%2

n = 100000
j = 100
args = ("h1", "b3", 2)
res = [[0]*j,[0]*j]

for k in range(j):

	t1 = time.time()
	for _ in range(n):
		solution(*args)
	elapsed = time.time()-t1
	#print("2", elapsed, elapsed/n)
	res[1][k] = elapsed
	del t1, elapsed

	t0 = time.time()
	for _ in range(n):
		solution1(*args)
	elapsed = time.time()-t0
	#print("1", elapsed, elapsed/n)
	res[0][k] = elapsed
	del t0, elapsed


print("1", sum(res[0])/(n*j))
print("2", sum(res[1])/(n*j))
