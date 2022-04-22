from random import random
from typing import Tuple
from libnum import generate_prime
import libnum
import random
p=1092917513274372122286774856355924354973391200253 #160 bits p=generate_prime(p)
a = 1  
b = 10  
s = 19
k = 15
class ECC:
    def __init__(self, a, b, modulo):
        self.a = a
        self.b = b
        self.modulo = modulo
        self.zero = (None, None)

    # Tính tổng P+Q
    def add(self, P, Q):
        if (P == self.zero):
            return Q
        if (Q == self.zero):
            return P
        x1, y1 = P
        x2, y2 = Q
        if x1 == x2 and y1 != y2:
            return self.zero
        if x1 == x2:
            lamda = (3 * x1 * x1 + self.a) * pow(2 * y1, -1,self.modulo)
        else:
            lamda = (y2 - y1) * pow(x2 - x1,-1, self.modulo)
        x = (lamda * lamda - x1 - x2) % self.modulo
        y = (lamda * (x1 - x) - y1) % self.modulo
        return (x, y)

    # Tính nQ
    def multiply(self, P, n):
        Q = self.zero
        for i in range(n):
            Q = self.add(Q, P)
        return Q

print(f"Elliptic curve: y^2 = x^3 + {a}*x + {b} mod p")
print('p=',p)
ecc = ECC(a, b, p)

# Kiểm tra tọa độ x có thuộc đường cong E không, nếu có tính tọa độ y theo x
def onCurve(x):
    z=(x**3 +a*x+b)%p
    if(libnum.has_sqrtmod(z,{p:1})):  
        y=next(libnum.sqrtmod(z,{p:1}))
    print("(%d,%d)" % (x,y))

    if ((y**2 % p) == ((x**3+a*x+b) %p)): 
        print("Điểm này thuộc E")
    else:
        print("Điểm này không thuộc E")    

#thử xP=4
#onCurve(4) # sau đó tính được tọa độ y của P
P: Tuple[int, int] = (4,1006462020242386297383479675793873753633925500690)
print('P=', P)

# Lập bảng cửu chương cho nP
for i in range (1,21):  # n=20 ta lập bảng cửu chương tới 20P, chạy n tùy ý trong phạm vi
    T= ecc.multiply(P,i)
    print(i,'P=')
    onCurve(T[0])
    
B = ecc.multiply(P, s) #B=sP

# Công khai (E,p,P,B)
print('Công khai (E,p,P,B):')
print('Điểm sinh P=', P)
print('p=',p)
print('B=', B)


def encode(k: int, M: Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    # mã hóa M1= kP
    M1 = ecc.multiply(P, k)

    # mã hóa M2= M +kB
    kB = ecc.multiply(B, k)
    M2 = ecc.add(M, kB)
    return (M1, M2)


def decode(M1: Tuple[int, int], M2: Tuple[int, int]) -> Tuple[int, int]:
    sM1 = ecc.multiply(M1, s)
    sM1_ = (sM1[0], p - sM1[1])   # sM1_ là điểm đối xứng với sM1
    res = ecc.add(M2, sM1_)
    return res



print('Bản tin M=13P: M=')
M=ecc.multiply(P,13)
print(M)

M1, M2 = encode(k, M)
print("Mã hóa: (M1,M2)")
print('M1=',M1)
print('M2=',M2)

print("Giải mã:")
print(ecc.multiply(M1, s))
Res = decode(M1, M2)
print(Res)
if( Res==M):
    print('Giải mã thành công')
else:
    print('Giải mã thất bại')

# Chữ ký
# n là số điểm của đường cong E tính được là một số nguyên tố
n= 1092917513274372122286776282503556125139562074411

# h= số hóa họ và tên lấy kết quả từ RSA 
h=578327393061624261148250
# chọn khóa riêng của người gửi là d và chọn luôn d=3
#d= random.randint(1,n)
d=3
print('Khóa riêng người gửi là d=',d)
Q=ecc.multiply(P,d)

print('Q=',Q)
# Chọn ngẫu nhiên một số k1
k1=15
k1P=ecc.multiply(P,k1)
r= k1P[0]%n
t=pow(k1,-1,n)
s1=((h+d*r)*t)%n
if(r!=0 and s1!=0):
    print('k1=',k1)
    print('k1P',k1P)
    print('Chữ ký là cặp số nguyên (r,s)=(',r,',',s1,')')

# Xác thực chữ ký
w=pow(s1,-1,n)
print('w=',w)
u1=(h*w)%n
print('u1=',u1)
u2=(r*w)%n
print('u2=',u2)
# z=u1*P+u2*Q
u=(u1+u2*d)%n
z=ecc.multiply(P,u)
v=z[0]%n
if(v==r):
    print('Chữ ký đúng')
else:
    print('Chữ ký sai')