import time

from pypbc import Parameters, Pairing

from Ali_scheme import Ali_scheme
from Liu_scheme import Liu_scheme
from Luo_scheme import Luo_scheme
from Niu_Scheme import Niu_scheme
from Our_scheme import Our_scheme
from Ullah_scheme import Ullah_scheme
from Wang_Scheme import Wang_scheme

if __name__ == '__main__':
    # params = Parameters(qbits=512, rbits=160)

    params= Parameters(qbits=1024, rbits=224)
    # params = Parameters(qbits=1536, rbits=256)
    pairing = Pairing(params)

    message = "hello world"

    nums=[2,4,6,8,10,12]

    averag_count=100

    our_time=[]
    Qiu_time=[]
    Luo_time=[]
    Liu_time=[]
    Ali_time=[]
    Niu_time=[]
    Ullah_time=[]
    Wang_time=[]

    for num in nums:
        Our_Scheme = Our_scheme(pairing, num)
        Luo_Scheme = Luo_scheme(pairing, num)
        Liu_Scheme = Liu_scheme(pairing, num)
        Ali_Scheme = Ali_scheme(pairing, num)
        Niu_Scheme = Niu_scheme(pairing, num)
        Ullah_Scheme = Ullah_scheme(pairing, num)
        Wang_Scheme = Wang_scheme(pairing, num)

        start_time = time.time()
        for i in range(averag_count):
            I_s, A_s, EN_s, C_s = Ullah_Scheme.signcrytion(message)
            message_2 = Ullah_Scheme.unsigncryption(I_s, A_s, EN_s, C_s)
        end_time = time.time()
        t2 = (end_time - start_time) / averag_count
        Ullah_time.append(t2)


        start_time = time.time()
        for i in range(averag_count):
            A_list, U, V, C, S = Our_Scheme.signcrytion(message)
            message_2 = Our_Scheme.unsigncryption(A_list, U, V, C, S)
        end_time = time.time()
        t2 = (end_time - start_time) / averag_count
        our_time.append(t2)
        # print("Our:", t2)


        start_time = time.time()
        for i in range(averag_count):
            C_i, R_i, r_i_1 = Wang_Scheme.signcrytion(message)
            message_2 = Wang_Scheme.unsigncryption(C_i, R_i, r_i_1)
        end_time = time.time()
        t2 = (end_time - start_time) / averag_count
        Wang_time.append(t2)



        start_time = time.time()
        for i in range(averag_count):
            c, u, R_2, T=Niu_Scheme.signcrytion(message)
            message_2=Niu_Scheme.unsigncryption(c, u, R_2, T)
        end_time = time.time()
        t2 = (end_time - start_time)/averag_count
        Niu_time.append(t2)
        # print("Niu:", t2)

        start_time = time.time()
        for i in range(averag_count):
            w_i,S_i,R_i=Ali_Scheme.signcrytion(message)
            message_2=Ali_Scheme.unsigncryption(w_i,S_i,R_i)
        end_time = time.time()
        t2 = (end_time - start_time)/averag_count
        Ali_time.append(t2)
        # print("Ali:", t2)

        start_time = time.time()
        for i in range(averag_count):
            c, u, V = Liu_Scheme.signcrytion(message)
            message_2 = Liu_Scheme.unsigncryption(c, u, V)
        end_time = time.time()
        t2 = (end_time - start_time)/averag_count
        Liu_time.append(t2)
        # print("Liu", t2)

        start_time = time.time()
        for i in range(averag_count):
            C, U, V = Luo_Scheme.signcrytion(message)
            message_2 = Luo_Scheme.unsigncryption(C, U, V)
        end_time = time.time()
        t2 = (end_time - start_time)/averag_count
        Luo_time.append(t2)
        # print("Luo:", t2)



    print("Our=", our_time)
    print("Niu=", Niu_time)
    print("Ali=", Ali_time)
    print("Liu=", Liu_time)
    print("Luo=", Luo_time)
    print("Ullah=", Ullah_time)
    print("Wang=", Wang_time)


