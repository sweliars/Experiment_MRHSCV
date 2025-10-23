import hashlib
import hmac
import time
from hashlib import sha256
from pypbc import G2, Element, GT, Zr, Parameters, Pairing

from util import sxor, lagrange_basis_poly, get_multi_receivers_coefficients, \
    get_multi_receivers_value_by_coefficient

class Wang_sender():
    def __init__(self, ID_A,d_i,D_i,t_i,T_i,u_i,PK_i,v_i,l_i,SK_i,k,h_i):
        self.ID_A = ID_A
        self.d_i = d_i
        self.D_i = D_i
        self.t_i = t_i
        self.T_i = T_i
        self.u_i = u_i
        self.PK_i = PK_i
        self.v_i = v_i
        self.l_i = l_i
        self.SK_i = SK_i
        self.k=k
        self.h_i = h_i

class Wang_receiver():
    def __init__(self,ID_r,sk_r):
        self.ID_r=ID_r
        self.sk_r=sk_r

# Efficient and Provably Secure Offline/Online Heterogeneous Signcryption Scheme for VANETs
class Wang_scheme():
    def __init__(self,pairing,num):
        self.num=num

        self.pairing=pairing
        self.g2=Element.random(pairing,G2)
        self.s=Element.random(pairing,Zr)
        self.msk=self.s
        self.P_pub=self.g2*self.s

        # UserA
        self.sender_list=[]
        for i in range(num):
            ID_A="ID_A"+str(i)
            d_i=Element.random(pairing,Zr)
            D_i=self.g2*(d_i)
            t_i=Element.random(pairing,Zr)
            T_i=self.g2*(t_i)
            u_i=Element.from_hash(pairing,Zr,str(ID_A)+str(D_i)+str(T_i))
            PK_i=T_i+D_i*u_i
            v_i = Element.from_hash(pairing, Zr, str(ID_A) + str(PK_i))
            l_i=t_i+self.s*v_i
            SK_i=l_i+u_i*d_i
            k=Element.random(pairing,Zr)
            h_i=(PK_i+self.P_pub*v_i)*k
            sender=Wang_sender(ID_A,d_i,D_i,t_i,T_i,u_i,PK_i,v_i,l_i,SK_i,k,h_i)
            self.sender_list.append(sender)

        # UserB
        self.receiver_list=[]
        for i in range(num):
            ID_r="ID_B"+str(i)
            sk_r=Element.from_hash(pairing, G2, str(ID_r))*self.s
            receiver=Wang_receiver(ID_r,sk_r)
            self.receiver_list.append(receiver)

        pass


    def signcrytion(self,message):
        self.message=message
        C_i, R_i, r_i_1=None, None, None

        C_i_list=[]
        R_i_list=[]
        r_i_1_list=[]
        for i in range(self.num):
            sender=self.sender_list[i]
            receiver=self.receiver_list[i]

            r_i=Element.random(self.pairing,Zr)
            s_i=(sender.SK_i.__invert__())*r_i
            R_i=self.g2*r_i
            U_i=self.pairing.apply(self.P_pub*r_i,Element.from_hash(self.pairing, G2, str(receiver.ID_r)))
            W_i=Element.from_hash(self.pairing, Zr, str(U_i))
            f=Element.from_hash(self.pairing, Zr, str(message)+str(R_i))
            r_i_1=sender.k-f*s_i
            C_i=sxor(str(W_i),str(r_i_1))

            C_i_list.append(C_i)
            R_i_list.append(R_i)
            r_i_1_list.append(r_i_1)

        return C_i_list,R_i_list,r_i_1_list




    def unsigncryption(self,C_i_list,R_i_list,r_i_1_list):
        m=None
        for i in range(self.num):
            sender = self.sender_list[i]
            receiver = self.receiver_list[i]
            C_i=C_i_list[i]
            R_i=R_i_list[i]
            r_i_1=r_i_1_list[i]


            U_i=self.pairing.apply(R_i,receiver.sk_r)
            W_i=Element.from_hash(self.pairing, Zr, str(U_i))
            r_i_1_m=sxor(str(W_i),str(C_i))

            f = Element.from_hash(self.pairing, Zr, str(self.message) + str(R_i))
            R=R_i*f+(sender.PK_i+self.P_pub*sender.v_i)*r_i_1
            if (sender.h_i).__eq__(R):
                # print("true")
                pass
            else:
                print("false")

        return m



if __name__ == '__main__':

    params = Parameters(qbits=512, rbits=160)
    pairing = Pairing(params)

    Wang_Scheme=Wang_scheme(pairing,2)

    message="hello world"

    C_i,R_i,r_i_1=Wang_Scheme.signcrytion(message)

    message_2=Wang_Scheme.unsigncryption(C_i,R_i,r_i_1)


    print(message_2)










