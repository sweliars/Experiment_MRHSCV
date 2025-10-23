import hashlib
import hmac
import time
from hashlib import sha256
from pypbc import G2, Element, GT, Zr, Parameters, Pairing

from util import sxor, lagrange_basis_poly, get_multi_receivers_coefficients, \
    get_multi_receivers_value_by_coefficient

class Our_receiver():
    def __init__(self, id_i,x_i,P_i,r_i,R_i,h_i,d_i):
        self.x_i=x_i
        self.id_i=id_i
        self.P_i=P_i
        self.r_i=r_i
        self.R_i=R_i
        self.h_i=h_i
        self.d_i=d_i
        pass

# Privacy-Preserving Mutual Heterogeneous Signcryption Schemes Based on 5G Network Slicing
class Our_scheme():
    def __init__(self,pairing,num):
        self.num=num

        self.pairing=pairing
        self.g2=Element.random(pairing,G2)
        self.s=Element.random(pairing,Zr)
        self.P_pub=self.g2*self.s

        # UserA
        self.ID_A="ID_A"
        self.x_R=Element.random(pairing,Zr)
        self.P_R=self.g2*(self.x_R)

        # UserB
        self.receivers=[]
        for i in range(num):
            id_i="ID_B"+str(i)
            x_i=Element.random(pairing,Zr)
            P_i=self.g2*x_i
            r_i=Element.random(pairing,Zr)
            R_i=self.g2*(r_i)
            h_i=Element.from_hash(pairing,Zr,id_i+str(P_i)+str(R_i))
            d_i=r_i+self.s*h_i
            reveiver=Our_receiver(id_i,x_i,P_i,r_i,R_i,h_i,d_i)
            self.receivers.append(reveiver)
        pass


    def signcrytion(self,message):
        self.message=message

        v=Element.random(self.pairing,Zr)
        V=self.P_R*v

        gama_list=[]

        for i in range(self.num):
            receiver=self.receivers[i]
            h_i=Element.from_hash(self.pairing,Zr,str(receiver.id_i)+str(receiver.P_i)+str(receiver.R_i))
            W_i=(receiver.P_i+receiver.R_i+self.P_pub*h_i)*(v*self.x_R)
            gama_i=Element.from_hash(self.pairing,Zr,str(W_i))
            gama_list.append(gama_i)


        t=Element.random(self.pairing,Zr)

        A_list=get_multi_receivers_coefficients(self.pairing,gama_list,t)
        A = str(A_list)
        C=sxor(str(t),str(self.message))
        # print(C)

        h_4=Element.from_hash(self.pairing,Zr,self.ID_A+str(self.P_R)+str(self.P_pub)+str(self.message)+str(A)+str(V))
        h_5=Element.from_hash(self.pairing,Zr,self.ID_A+str(self.P_R)+str(self.P_pub)+str(self.message)+str(A)+str(V)+str(h_4))

        S=h_4*v+h_5*(self.x_R.__invert__())
        U=sxor(str(self.ID_A)+str(self.P_R)+str(S)+str(C),str(t))
        return A_list,U,V,C,S



    def unsigncryption(self,A_list,U,V,C,S):
        m=None
        for i in range(self.num):
            receiver=self.receivers[i]
            W_i=V*(receiver.x_i+receiver.d_i)
            gama_i=Element.from_hash(self.pairing,Zr,str(W_i))
            t=get_multi_receivers_value_by_coefficient(self.pairing,A_list,gama_i)
            ID_S_C=sxor(str(U),str(t))
            # print(ID_S_C)

            m=sxor(str(C),str(t))
            A = str(A_list)
            h_4 = Element.from_hash(self.pairing, Zr,
                                    self.ID_A + str(self.P_R) + str(self.P_pub) + str(self.message) +str(A)+ str(V)).__invert__()
            h_5 = Element.from_hash(self.pairing, Zr,
                                    self.ID_A + str(self.P_R) + str(self.P_pub) + str(self.message) + str(A)+str(V)+str(h_4))

            L=self.P_R*S*(h_4)
            R=V+self.g2*h_5*(h_4)
            if L.__eq__(R):
                # print("true")
                pass
            else:
                print("false")

        return m



if __name__ == '__main__':

    params = Parameters(qbits=512, rbits=160)
    pairing = Pairing(params)

    Our_Scheme=Our_scheme(pairing,2)

    message="hello world"

    A_list,U,V,C,S=Our_Scheme.signcrytion(message)

    message_2=Our_Scheme.unsigncryption(A_list,U,V,C,S)


    print(message_2)










