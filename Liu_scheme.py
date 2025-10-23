
from pypbc import G2, Element, GT, Zr, Parameters, Pairing

from util import sxor
# Mutual Heterogeneous Signcryption Schemes for 5G Network Slicings

class Liu_sender():
    def __init__(self,ID_A,x_p,sk_p,PK_p):
        self.ID_A = ID_A
        self.x_p = x_p
        self.PK_p = PK_p
        self.sk_p = sk_p

class Liu_receiver():
    def __init__(self,ID_B,t,T,gama,d,x_c,PK_c1):
        self.ID_B = ID_B
        self.t=t
        self.T = T
        self.gama = gama
        self.d = d
        self.x_c = x_c
        self.PK_c1 = PK_c1

class Liu_scheme():
    def __init__(self,pairing,num):
        self.num=num

        self.pairing=pairing
        self.g2=Element.random(pairing,G2)
        self.s=Element.random(pairing,Zr)
        self.P_pub=self.g2*self.s

        # UserA
        self.sender_list=[]
        for i in range(num):

            ID_A="ID_A"+str(i)
            x_p=Element.random(pairing,Zr)
            sk_p=x_p
            PK_p=self.g2*(x_p.__invert__())
            sender=Liu_sender(ID_A,x_p,sk_p,PK_p)
            self.sender_list.append(sender)

        # UserB
        self.receiver_list = []
        for i in range(num):
            ID_B="ID_B"+str(i)
            t=Element.random(pairing,Zr)
            T=self.g2*(t)
            gama=Element.from_hash(pairing,Zr,ID_B+str(T))
            d=t+self.s*gama
            x_c = Element.random(pairing, Zr)
            PK_c1=self.g2*x_c
            receiver=Liu_receiver(ID_B,t,T,gama,d,x_c,PK_c1)
            self.receiver_list.append(receiver)
        pass


    def signcrytion(self,message):
        self.message=message
        c_list=[]
        u_list=[]
        V_list=[]
        for i in range(0,self.num):
            sender = self.sender_list[i]
            receiver = self.receiver_list[i]

            k=Element.random(self.pairing,Zr)
            R_1=self.g2*k
            # print({i},"R_1:",R_1)
            h=Element.from_hash(self.pairing,Zr,str(message)+str(R_1))
            R_2=self.g2*h
            c=sxor(str(self.message),str(R_2))
            u=sender.sk_p*(h-k)
            gama=Element.from_hash(self.pairing,Zr,receiver.ID_B+str(receiver.T))
            V=receiver.PK_c1*k+receiver.T+self.P_pub*gama
            c_list.append(c)
            u_list.append(u)
            V_list.append(V)
        return c_list,u_list,V_list


    def unsigncryption(self,c_list,u_list,V_list):
        m=None
        for i in range(self.num):
            sender = self.sender_list[i]
            receiver = self.receiver_list[i]
            c=c_list[i]
            u=u_list[i]
            V=V_list[i]


            R_1=(V-self.g2*receiver.d)*(receiver.x_c.__invert__())
            # print({i},"R_1:",R_1)
            R_2=R_1+sender.PK_p*u
            m=sxor(c,str(R_2))
            # print(m)
            h=Element.from_hash(self.pairing,Zr,str(self.message)+str(R_1))
            if R_1.__eq__(self.g2*h-sender.PK_p*u):
                # print("true")
                pass
            else:
                print("false")

        return m



if __name__ == '__main__':

    params = Parameters(qbits=512, rbits=160)
    pairing = Pairing(params)

    Liu_Scheme=Liu_scheme(pairing,10)

    message="hello world"

    c,u,V=Liu_Scheme.signcrytion(message)

    message_2=Liu_Scheme.unsigncryption(c,u,V)


    print(message_2)










