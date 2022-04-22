from typing import MutableMapping
from libnum import generate_prime
import math
import random
 
# tính x^n mod p cũng có thể dùng trực tiếp pow
def power(x,n,p):
    res =1
    x=x%p
    while(n>0):
        if(n %2==1):
            res =(res*x)%p
        
        n=n/2
        x=(x*x)%p
    return res

#Phân tích ra thừa số nguyên tố
def findPrimefactors(n):
    s =[]
    if(n%2==0): s.append(2)

    while (n%2==0):
        n=n/2
    for i in range(3,round(math.sqrt(n))+1,2):
        while(n%i==0):
            if(i!=s[-1]):
               s.append(i)
            n=n//i
    if(n>2): s.append(n)
    return s

# Tìm phần tử nguyên thủy đầu tiên
def findPrimitive(p):
    num =p-1
    s= findPrimefactors(num)
    for n in range (2,p):
        flag= False
        for i in s:
            k= round(num/i)
            if pow(n,k,p)==1:
                flag=True
                break
        if (flag==False): 
            return n
    return -1

# p=generate_prime(256) 
p = 66972148094483699263382968961897701756411803992532544790333750127279599047321

print('Số nguyên tố p=', p)
print(' p-1 phân tích được ra các thừa số nguyên tố là:', findPrimefactors(p-1))
alpha = findPrimitive(p)
print('Phần tử nguyên thủy của p là alpha=',alpha)

# chọn a=1107 - ngày tháng sinh
a=int(input('Vui lòng nhập a: '))
#a=1107

k=int(input('Vui lòng nhập khóa k: '))
#k=113

# chọn x= số hóa tên 'BAO'
x=578327393061624261148250
print('x=',x)
# Tính beta
beta = pow(alpha,a)

print('a=', a)
print('k=',k)
print('beta= ', beta)
# Mã hóa e K'(x,k)=(y1,y2)

y1= pow(alpha,k,p)
_y2= pow(beta,k,p)
y2=(x*_y2)%p
print('Mật mã của x là (y1,y2):')
print('y1=', y1)
print('y2=', y2)

#Giải mã y2* (y1^a)^-1  mod p

res1 = pow(y1,a,p)
res2 = pow(res1,-1,p)
res = (y2* res2)%p
print('Kết quả giải mã được là:',res)
if (res==x): print ('Giải mã thành công')

# Chữ ký và kiểm thử chữ ký

# chữ ký
# Kiểm tra xem số p-1 có là modulo nghịch đảo của k không
def eValid(a,b):
    try:
        t=pow(a,-1,b)
        return t
    except ValueError:
        return False
k1=int(input('Vui lòng nhập khóa k1: '))
while(eValid(k1,p-1)==False):
    k1= int(input('k1 không hợp lệ.Vui lòng nhập lại k1: '))

gamma = pow(alpha, k1,p)
s1= pow(k1,-1,p-1)       #eValid
s=(x-a*gamma)*s1%(p-1)
print(s1)
print('Chữ ký sig(x,k)=(',gamma,',',s,')')

# kiểm thử chữ ký
t1= pow(beta,gamma,p)
t2=pow(gamma,s,p)
t= (t1*t2)%p
print('beta^gamma* gamma^s mod p=',t)
kt= pow(alpha,x,p)
print('alpha^x=',kt)
if(t==kt):
    print('Chữ ký sig(x,k1) được xác nhận là đúng')
else:
    print('Chữ ký sai')

