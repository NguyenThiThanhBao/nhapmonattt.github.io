# from libnum import generate_prime
# Có thể dùng generate_prime để sinh ra số nguyên tố lớn ngẫu nhiên
# p= generate_prime(256)
# q= generate_prime(256)

import math

from libnum.common import len_in_bits

def gcd(a, b):
  
    if (a == 0):
        return b
    if (b == 0):
        return a
  
    if (a == b):
        return a
  
    if (a > b):
        return gcd(a%b, b)
    return gcd(a, b%a)

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

p=108727583271094938804067468427449177408134313544087916009935531860166325579893
q=105107824811362760480723104326217167178876041720593089117887439801773691758649

print('Số nguyên tố p= ',p)
print('Số nguyên tố q= ',q)

n =p * q
print('Độ dài bit của n là:', len_in_bits(n))
print('n=',n)
phi = (p-1) * (q-1)
print('phi=(p-1)*(q-1)=', phi)
print(phi%3)
#chọn e thỏa mãn 1<e<phi và gcd(e,phi)=1
e=int(input('Vui lòng nhập số e: '))
while(math.gcd(e,phi)!=1 or e<=1 or e>=phi):
    e= int(input('e không thỏa mãn. Vui lòng nhập lại e: '))
    
# Cũng chọn e có 256 bit, chọn luôn e là số nguyên tố 
#e= 107020324028697780970257011405130133134438432904802840806508701642073169434969

# Tìm d sao cho ed= 1(mod phi) d= e^-1 mod phi
d = pow(e,-1,phi)

#Thông tin cần gửi x là họ tên đầy đủ
s="nguyenthithanhbao"
x=0
for i in range(len(s)):
    t= ord(s[i])-97
    x=x+ t*pow(26,len(s)-1-i)


# Mã hóa y= x^e mod n
y = pow(x, e,n)  # y=power(x,e,n)

#Giải mã x= y^d mod n
z = pow(y,d,n)     # z= power(x,e,n)



if gcd(e, phi)==1: print('Tìm được e với phi nguyên tố cùng nhau')
#if math.gcd(e, phi)==1: print('Tìm được e với phi nguyên tố cùng nhau') 
print('Khóa công khai k=(n,e)=(n=', n,'e=', e,')')
print('Số d (ed=1(mod phi))=', d)
print('Thông báo cần gửi x=',x)
print('Kết quả mã hóa y= ', y)
print('Kết quả giải mã z=',z)
if(x==z):
    print("x=z => Giải mã thành công")
else: print("Giải mã thất bại")
 

# Kí và kiểm thử chữ ký
# a và b là hai số thuộc Z(n)* sao cho a.b mod phi=1

# Kiểm tra xem số b có là modulo nghịch đảo của a không
def eValid(a,b):
    try:
        d=pow(a,-1,b)
        return d
    except ValueError:
        return False

a=int(input('Vui lòng nhập số a: '))
while(eValid(a,phi)==False):
    a= int(input('a không hợp lệ.Vui lòng nhập lại a: '))

b=eValid(a,phi)
print('b=',b)
sig=pow(x,a,n)
print('Chữ ký sig(x) là',sig)
# Kiểm thử chữ ký
print('sig^b mod n =',pow(sig,b,n))
if(x== pow(sig,b,n)):
    print('=> Chữ ký đúng')
else:
    print('=> Chữ ký sai')
