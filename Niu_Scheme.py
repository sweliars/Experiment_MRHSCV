import hashlib
import hmac
import time
from hashlib import sha256
from pypbc import G2, Element, GT, Zr, Parameters, Pairing

from util import sxor, lagrange_basis_poly


class Niu_receiver():
    def __init__(self, id_i,b_i,B_i,gama_i,d_i,x_ci,pk_cli):
        self.id_i = id_i
        self.b_i = b_i
        self.B_i = B_i
        self.gama_i = gama_i
        self.d_i = d_i
        self.x_ci = x_ci
        self.pk_cli = pk_cli
        pass




# Privacy-Preserving Mutual Heterogeneous Signcryption Schemes Based on 5G Network Slicing
class Niu_scheme():
    def __init__(self,pairing,num):
        self.num=num

        self.pairing=pairing
        self.g2=Element.random(pairing,G2)
        self.s=Element.random(pairing,Zr)
        self.P_pub=self.g2*self.s

        # UserA
        self.ID_A="ID_A"
        self.x_A=Element.random(pairing,Zr)
        self.PK_A=self.g2*(self.x_A.__invert__())

        # UserB
        self.receivers=[]
        for i in range(num):
            id_i="ID_B"+str(i)
            b_i=Element.random(pairing,Zr)
            B_i=self.g2*b_i
            gama_i=Element.from_hash(pairing,Zr,id_i+str(B_i))
            d_i=b_i+self.s*gama_i

            x_ci=Element.random(pairing,Zr)
            pk_cli=self.g2*x_ci
            reveiver=Niu_receiver(id_i,b_i,B_i,gama_i,d_i,x_ci,pk_cli)
            self.receivers.append(reveiver)
        pass


    def signcrytion(self,message):
        k=Element.random(self.pairing,Zr)
        R=self.g2*k
        h=Element.from_hash(self.pairing,Zr,str(self.ID_A)+str(message)+str(R))
        R_1=self.g2*h
        self.message=message
        c=sxor(str(self.ID_A)+str(message),str(R_1))
        u=(h-k)*self.x_A
        g1=Element.random(self.pairing,G2)
        R_2=g1*k

        x_i_list=[]
        v_i_list = []
        for i in range(self.num):
            receiver = self.receivers[i]
            x_i = Element.from_hash(self.pairing, Zr, str(receiver.id_i))
            Q_i = receiver.pk_cli + receiver.B_i * (k.__invert__()) + self.P_pub * (receiver.gama_i * k.__invert__())
            v_i = (g1 + Q_i) * k
            v_i_list.append(v_i)
            x_i_list.append(x_i)
            # print("v_i",v_i)

        a_i_lists=[]
        for i in range(self.num):
            a_i_list=lagrange_basis_poly(self.pairing,x_i_list,i)
            a_i_lists.append(a_i_list)

        T_list=[]

        for i in range(self.num):
            T=Element.zero(self.pairing,G2)
            for j in range(self.num):
                T+= v_i_list[j]*a_i_lists[j][i]
            T_list.append(T)

        return c,u,R_2,T_list



    def unsigncryption(self,c, u, R_2, T):
        ID_i_m=None
        for i in range(self.num):
            receiver=self.receivers[i]
            x_i=Element.from_hash(self.pairing,Zr,str(receiver.id_i))
            v_i = Element.zero(self.pairing, G2)

            for power in range(len(T)):
                v_i += T[power] * (x_i ** power)
            # print("v_i",v_i)

            R=(v_i-R_2-self.g2*(receiver.d_i))*(receiver.x_ci.__invert__())
            R_1=R+self.PK_A*u
            ID_i_m=sxor(str(R_1),str(c))
            # print(ID_i_m)
            h=Element.from_hash(self.pairing,Zr,str(self.ID_A)+str(self.message)+str(R))
            if R.__eq__(self.g2*h-self.PK_A*u):
                # print("true")
                pass
            else:
                print("false")

        return ID_i_m


if __name__ == '__main__':

    params = Parameters(qbits=512, rbits=160)
    pairing = Pairing(params)

    Niu_Scheme=Niu_scheme(pairing,1)

    message="hello world"

    c, u, R_2, T=Niu_Scheme.signcrytion(message)

    message_2=Niu_Scheme.unsigncryption(c, u, R_2, T)


    print(message_2)










