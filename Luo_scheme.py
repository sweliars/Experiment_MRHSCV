
from pypbc import G2, Element, GT, Zr, Parameters, Pairing

from util import sxor

class Luo_sender():
    def __init__(self,ID_A,x_p,PK_p):
        self.ID_A = ID_A
        self.x_p = x_p
        self.PK_p = PK_p

class Luo_receiver():
    def __init__(self,ID_B,t_c,T_P,gama_c,T_c,d_c,x_c,PK_c):
        self.ID_B = ID_B
        self.t_c = t_c
        self.T_P = T_P
        self.gama_c = gama_c
        self.T_c = T_c
        self.d_c = d_c
        self.x_c = x_c
        self.PK_c = PK_c


# Mutual heterogeneous signcryption schemes with different system parameters for 5G network slicings
class Luo_scheme():
    def __init__(self,pairing,num):
        self.num=num

        self.pairing=pairing
        self.g1=Element.random(pairing,G2)
        self.g2 = Element.random(pairing, G2)
        self.s=Element.random(pairing,Zr)
        self.P_pub=self.g1*self.s

        # UserA
        self.sender_list=[]
        for i in range(self.num):

            ID_A="ID_A"+str(i)
            x_p=Element.random(pairing,Zr)
            PK_p=self.g2*(x_p)
            sender=Luo_sender(ID_A,x_p,PK_p)
            self.sender_list.append(sender)

        # UserB
        self.receiver_list=[]
        for i in range(self.num):
            ID_B="ID_B"+str(i)
            t_c=Element.random(pairing,Zr)
            T_P=self.P_pub*(t_c)
            gama_c=Element.from_hash(pairing,Zr,ID_B+str(T_P))
            T_c=T_P*gama_c
            d_c=t_c*self.s*gama_c
            x_c = Element.random(pairing, Zr)
            PK_c=self.g1*x_c
            receive=Luo_receiver(ID_B,t_c,T_P,gama_c,T_c,d_c,x_c,PK_c)
            self.receiver_list.append(receive)

        pass


    def signcrytion(self,message):
        self.message=message
        C_list=[]
        U_list=[]
        V_list=[]
        for i in range(self.num):
            sender=self.sender_list[i]
            receiver=self.receiver_list[i]

            k=Element.random(self.pairing,Zr)
            R_1=self.g2*k
            R_2=(receiver.T_c+receiver.PK_c)*k*sender.x_p
            V=self.g1*k*sender.x_p
            Z=Element.from_hash(self.pairing,Zr,str(R_1)+str(R_2)+str(V)+str(message))
            C=sxor(str(self.message)+str(Z)+str(sender.ID_A),str(R_2)+str(V))
            h=Element.from_hash(self.pairing,Zr,str(R_2)+str(V)+str(C))
            U=((h+sender.x_p).__invert__())*k
            C_list.append(C)
            U_list.append(U)
            V_list.append(V)
        return C_list,U_list,V_list

    def unsigncryption(self,C_list,U_list,V_list):
        m_Z_ID=None
        for i in range(self.num):
            sender = self.sender_list[i]
            receiver = self.receiver_list[i]
            C=C_list[i]
            U=U_list[i]
            V=V_list[i]

            R_2=V*(receiver.d_c+receiver.x_c)
            m_Z_ID=sxor(str(C),str(R_2)+str(V))
            # print(m_Z_ID)
            h = Element.from_hash(self.pairing, Zr, str(R_2) + str(V) + str(C))
            R_1=(self.g2*h+sender.PK_p)*U

            if Element.from_hash(self.pairing,Zr,str(R_1)+str(R_2)+str(V)+str(self.message)).__eq__(Element.from_hash(self.pairing,Zr,str(R_1)+str(R_2)+str(V)+str(self.message))):

                # print("true")
                pass

            else:
                print("false")
        return m_Z_ID



if __name__ == '__main__':

    params = Parameters(qbits=512, rbits=160)
    pairing = Pairing(params)

    Luo_Scheme=Luo_scheme(pairing,2)

    message="hello world"

    C,U,V=Luo_Scheme.signcrytion(message)

    message_2=Luo_Scheme.unsigncryption(C,U,V)


    print(message_2)










