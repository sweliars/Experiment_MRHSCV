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
    params = Parameters(qbits=512, rbits=160)

    # params= Parameters(qbits=1024, rbits=224)
    # params = Parameters(qbits=1536, rbits=256)

    pairing = Pairing(params)

    message = "hello world"

    nums=[2,4,6,8,10,12]

    averag_count=10

    our_time=[]
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

        I_s_list=[]
        A_s_list=[]
        EN_s_list=[]
        C_s_list=[]
        for i in range(averag_count):
            I_s, A_s, EN_s, C_s = Ullah_Scheme.signcrytion(message)
            I_s_list.append(I_s)
            A_s_list.append(A_s)
            EN_s_list.append(EN_s)
            C_s_list.append(C_s)

        start_time = time.time()
        for i in range(averag_count):
            message_2 = Ullah_Scheme.unsigncryption(I_s_list[i], A_s_list[i], EN_s_list[i], C_s_list[i])
        end_time = time.time()
        t2 = (end_time - start_time) / averag_count
        Ullah_time.append(t2)

        C_i_list = []
        R_i_list = []
        r_i_1_list = []
        for i in range(averag_count):
            C_i, R_i, r_i_1 = Wang_Scheme.signcrytion(message)
            C_i_list.append(C_i)
            R_i_list.append(R_i)
            r_i_1_list.append(r_i_1)

        start_time = time.time()
        for i in range(averag_count):
            message_2 = Wang_Scheme.unsigncryption(C_i_list[i], R_i_list[i], r_i_1_list[i])
        end_time = time.time()
        t2 = (end_time - start_time) / averag_count
        Wang_time.append(t2)

        A_list_list = []
        U_list = []
        V_list = []
        C_list=[]
        S_list = []
        for i in range(averag_count):
            A_list, U, V, C, S = Our_Scheme.signcrytion(message)
            A_list_list.append(A_list)
            U_list.append(U)
            V_list.append(V)
            C_list.append(C)
            S_list.append(S)


        start_time = time.time()
        for i in range(averag_count):
            message_2=Our_Scheme.unsigncryption(A_list_list[i],U_list[i],V_list[i],C_list[i],S_list[i])
        end_time = time.time()
        t2 = (end_time - start_time)/averag_count
        our_time.append(t2)
        # print("Our:", t2)



        c_list = []
        u_list = []
        R_2_list = []
        T_list = []
        for i in range(averag_count):
            c, u, R_2, T = Niu_Scheme.signcrytion(message)
            c_list.append(c)
            u_list.append(u)
            R_2_list.append(R_2)
            T_list.append(T)

        start_time = time.time()
        for i in range(averag_count):
            message_2=Niu_Scheme.unsigncryption(c_list[i], u_list[i], R_2_list[i], T_list[i])
        end_time = time.time()
        t2 = (end_time - start_time)/averag_count
        Niu_time.append(t2)
        # print("Niu:", t2)


        w_i_list=[]
        S_i_list = []
        R_i_list = []
        for i in range(averag_count):
            w_i, S_i, R_i = Ali_Scheme.signcrytion(message)
            w_i_list.append(w_i)
            S_i_list.append(S_i)
            R_i_list.append(R_i)

        start_time = time.time()
        for i in range(averag_count):
            message_2=Ali_Scheme.unsigncryption(w_i_list[i],S_i_list[i],R_i_list[i])
        end_time = time.time()
        t2 = (end_time - start_time)/averag_count
        Ali_time.append(t2)
        # print("Ali:", t2)


        c_list=[]
        u_list=[]
        V_list=[]
        for i in range(averag_count):
            c, u, V = Liu_Scheme.signcrytion(message)
            c_list.append(c)
            u_list.append(u)
            V_list.append(V)

        start_time = time.time()
        for i in range(averag_count):
            message_2 = Liu_Scheme.unsigncryption(c_list[i], u_list[i], V_list[i])
        end_time = time.time()
        t2 = (end_time - start_time)/averag_count
        Liu_time.append(t2)
        # print("Liu", t2)

        C_list=[]
        U_list=[]
        V_list=[]
        for i in range(averag_count):
            C, U, V = Luo_Scheme.signcrytion(message)
            C_list.append(C)
            U_list.append(U)
            V_list.append(V)

        start_time = time.time()
        for i in range(averag_count):
            message_2 = Luo_Scheme.unsigncryption(C_list[i], U_list[i], V_list[i])
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

