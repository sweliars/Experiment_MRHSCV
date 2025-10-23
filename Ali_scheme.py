from copy import deepcopy

from blinker import receiver_connected
from pypbc import G2, Element, GT, Zr, Parameters, Pairing, G1

from util import sxor


class Ali_receiver():
    def __init__(self,ID_B,xita_i,sk_ir,pk_ir):
        self.ID_B=ID_B
        self.xita_i=xita_i
        self.sk_ir=sk_ir
        self.pk_ir=pk_ir
    pass

class Ali_sender():
    def __init__(self,ID_A,v_i,K_i,h_i1,delta_i,beta_i,pk_is):
        self.ID_A=ID_A
        self.v_i=v_i
        self.K_i=K_i
        self.h_i1=h_i1
        self.delta_i=delta_i
        self.beta_i=beta_i
        self.pk_is=pk_is
    pass

# Bilinear Pairing-Based Hybrid Signcryption for Secure Heterogeneous Vehicular Communications
class Ali_scheme():
    def __init__(self,pairing,num):
        self.num=num

        self.pairing=pairing
        self.g2=Element.random(pairing,G2)
        self.a=Element.random(pairing,Zr)
        self.P_pub=self.g2*self.a
        self.g=self.pairing.apply(self.g2,self.g2)

        # UserA
        self.sender_list=[]
        for i in range(self.num):
            ID_A = "ID_A"+str(i)
            v_i = Element.random(pairing, Zr)
            K_i = self.g2 * (v_i)
            h_i1=Element.from_hash(pairing, Zr, ID_A + str(K_i)+str(self.P_pub))
            delta_i=self.a+h_i1*v_i
            beta_i=Element.random(pairing, Zr)
            pk_is=self.g2*delta_i
            sender=Ali_sender(ID_A,v_i,K_i,h_i1,delta_i,beta_i,pk_is)
            self.sender_list.append(sender)


        self.receiver_list=[]
        # UserB
        for i in range(0,num):
            ID_B="ID_B"+str(i)
            xita_i=Element.random(pairing,Zr)
            sk_ir=self.g2*(xita_i.__invert__())
            pk_ir=self.g2*(xita_i)
            receiver=Ali_receiver(ID_B,xita_i,sk_ir,pk_ir)
            self.receiver_list.append(receiver)

        pass


    def signcrytion(self,message):
        self.message=message
        w_i_list=[]
        S_i_list=[]
        R_i_list=[]

        for i in range(0,self.num):
            sender=self.sender_list[i]
            receiver=self.receiver_list[i]
            self.beta_i=Element.random(self.pairing, Zr)
            u_i=self.g**self.beta_i
            w_i=sxor(str(u_i),message)
            h_i3=Element.from_hash(self.pairing,Zr,str(message)+str(sender.ID_A)+str(sender.pk_is)+str(u_i))
            S_i=self.g2*(self.beta_i*((h_i3*sender.delta_i).__invert__()))
            R_i=receiver.pk_ir*self.beta_i

            w_i_list.append(w_i)
            S_i_list.append(S_i)
            R_i_list.append(R_i)

        return w_i_list,S_i_list,R_i_list


    def unsigncryption(self,w_i_list,S_i_list,R_i_list):
        m_i=None
        for i in range(self.num):
            sender = self.sender_list[i]
            receiver=self.receiver_list[i]
            w_i=w_i_list[i]
            S_i=S_i_list[i]
            R_i=R_i_list[i]

            u_i = self.pairing.apply(R_i, receiver.sk_ir)
            m_i = sxor(str(u_i), w_i)
        #     # print(m_i)
            h_i3 = Element.from_hash(self.pairing, Zr, str(self.message) + str(sender.ID_A) + str(sender.pk_is) + str(u_i))
            self.pairing.apply(S_i, sender.pk_is * h_i3)
            if u_i.__eq__(self.pairing.apply(S_i, sender.pk_is * h_i3)):
                # print("true")
                pass
            else:
                print("false")


        return m_i



if __name__ == '__main__':

    params = Parameters(qbits=512, rbits=160)
    pairing = Pairing(params)

    Ali_Scheme=Ali_scheme(pairing,10)

    message="hello world"

    w_i,S_i,R_i=Ali_Scheme.signcrytion(message)

    message_2=Ali_Scheme.unsigncryption(w_i,S_i,R_i)


    print(message_2)










