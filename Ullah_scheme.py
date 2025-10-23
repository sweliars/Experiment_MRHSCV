
from pypbc import G2, Element, GT, Zr, Parameters, Pairing

from util import sxor, encrypt, decrypt


# A Conditional Privacy Preserving Heterogeneous Signcryption Scheme for Internet of Vehicles

class Ullah_sender():
    def __init__(self,ID_A,xita_s,l_s,lamda_s,epslon_s,h_v_s,v_s):
        self.ID_A = ID_A
        self.xita_s= xita_s
        self.l_s= l_s
        self.lamda_s= lamda_s
        self.epslon_s= epslon_s
        self.h_v_s= h_v_s
        self.v_s = v_s

class Ullah_receiver():
    def __init__(self,ID_B,xita_r,l_r,lamda_r,epslon_r,h_v_r,v_r):
        self.ID_B = ID_B
        self.xita_r = xita_r
        self.l_r = l_r
        self.lamda_r = lamda_r
        self.epslon_r = epslon_r
        self.h_v_r = h_v_r
        self.v_r = v_r

class Ullah_scheme():
    def __init__(self,pairing,num):
        self.num=num

        self.pairing=pairing
        self.D=Element.random(pairing,G2)
        self.Q=Element.random(pairing,Zr)
        self.fa=self.D*self.Q


        # UserA
        self.sender_list = []
        for i in range(self.num):
            ID_A = "ID_A"+str(i)
            xita_s = Element.random(pairing, Zr)
            l_s=self.D*xita_s

            lamda_s=Element.random(pairing, Zr)
            epslon_s=self.D*lamda_s
            h_v_s=Element.from_hash(pairing, Zr, ID_A + str(epslon_s)+str(l_s))
            v_s=lamda_s+self.Q*h_v_s
            sender=Ullah_sender(ID_A,xita_s,l_s,lamda_s,epslon_s,h_v_s,v_s)
            self.sender_list.append(sender)


        # UserB
        self.receiver_list = []
        for i in range(self.num):
            ID_B="ID_B"+str(i)
            xita_r = Element.random(pairing, Zr)
            l_r = self.D * xita_r
            lamda_r=Element.random(pairing, Zr)
            epslon_r=self.D*lamda_r
            h_v_r=Element.from_hash(pairing, Zr, ID_B + str(epslon_r)+str(l_r))
            v_r=lamda_r+self.Q*h_v_r
            receiver=Ullah_receiver(ID_B,xita_r,l_r,lamda_r,epslon_r,h_v_r,v_r)
            self.receiver_list.append(receiver)
        pass


    def signcrytion(self,message):
        self.message=message
        I_s_list=[]
        A_s_list=[]
        EN_s_list=[]
        C_s_list=[]

        for i in range(0,self.num):
            sender=self.sender_list[i]
            receiver=self.receiver_list[i]

            b_s=Element.random(self.pairing, Zr)
            A_s=self.D*b_s
            C_r=Element.from_hash(self.pairing, Zr, receiver.ID_B + str(receiver.epslon_r)+str(receiver.l_r))
            C_s = Element.from_hash(self.pairing, Zr, sender.ID_A + str(sender.epslon_s) + str(sender.l_s))
            F_r=receiver.epslon_r+self.fa*C_r
            G_s=F_r*b_s
            K=Element.from_hash(self.pairing, Zr, str(A_s)+str(G_s))
            EN_s=encrypt(str(self.message)+str(sender.ID_A)+str(receiver.epslon_r)+str(A_s)+str(C_s)+str(G_s),str(K))
            I_s=b_s+K*(sender.v_s+sender.xita_s)
            I_s_list.append(I_s)
            A_s_list.append(A_s)
            EN_s_list.append(EN_s)
            C_s_list.append(C_s)

        return I_s_list,A_s_list,EN_s_list,C_s_list


    def unsigncryption(self,I_s_list,A_s_list,EN_s_list,C_s_list):
        m=None
        for i in range(self.num):
            sender = self.sender_list[i]
            receiver = self.receiver_list[i]
            I_s=I_s_list[i]
            A_s=A_s_list[i]
            EN_s=EN_s_list[i]
            C_s=C_s_list[i]


            G_s=A_s*receiver.v_r
            K=Element.from_hash(self.pairing, Zr, str(A_s)+str(G_s))
            m=decrypt(EN_s,str(K))
            # print(m)
            # C_s = Element.from_hash(self.pairing, Zr, self.ID_A + str(self.epslon_s) + str(self.l_s))
            C_s = Element.from_hash(self.pairing, Zr, sender.ID_A + str(sender.epslon_s) + str(sender.l_s))
            C_s = Element.from_hash(self.pairing, Zr, sender.ID_A + str(sender.epslon_s) + str(sender.l_s))
            C_r = Element.from_hash(self.pairing, Zr, receiver.ID_B + str(receiver.epslon_r) + str(receiver.l_r))
            C_r = Element.from_hash(self.pairing, Zr, receiver.ID_B + str(receiver.epslon_r) + str(receiver.l_r))
            F_s=sender.epslon_s+self.fa*C_s
            L=self.D*I_s
            R = A_s + (sender.epslon_s + self.fa * C_r + sender.l_s) * K

            # R=A_s+(F_s+sender.l_s)*K
            if L.__eq__(R):
                # print("true")
                pass
            else:
                # print("false")
                pass

        return m



if __name__ == '__main__':

    params = Parameters(qbits=512, rbits=160)

    pairing = Pairing(params)

    Ullah_Scheme=Ullah_scheme(pairing,10)

    message="hello world"

    I_s,A_s,EN_s,C_s=Ullah_Scheme.signcrytion(message)

    message_2=Ullah_Scheme.unsigncryption(I_s,A_s,EN_s,C_s)


    print(message_2)










