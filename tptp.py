# cook your dish here
t=int(input())
while(t!=0):
    n,m,a,b,c=map(int,input().split())
    if n==m:
        print(c*n)
    elif n<m:
        print((n*c)+((m-n)*b))
    elif n>m:
        print((m*c)+((n-m)*a))
    
    t-=1


 

