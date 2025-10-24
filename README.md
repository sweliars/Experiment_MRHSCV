# Experiment_MRHSCV
The Source code in the Raspberry PI experiment in MRHSCV computational efficiency comparison


> This repository provides the full implementation of the **MRHSCV** scheme on Raspberry Pi, including code structure, environment setup, compilation and execution steps, performance evaluation scripts, and reproducible experiment workflows. It supports one-click experiment reproduction and robust error tracing.



## Table of Contents


1. Overview

2. Hardware and System

3. Software Dependencies

4. Source Code Structure

5. Running and Reproducing Experiments


## Overview

This README aims to help reviewers and researchers reproduce the **MRHSCV** protocol implementation on the Raspberry Pi platform. 

## Hardware and System

* **SoC**: Raspberry Pi 4B (4/8GB) or Raspberry Pi 5 (recommended)
* **Architecture**: armv7l
* **OS**: Ubuntu 20.04.5 LTS
* **Compiler**: gcc/g++ ≥ 9.4.0, gmp ≥ 6.1.2
* **Storage**: ≥ 32GB


## Software Dependencies

* Python 3.8(for pypbc use 3.8)
* System dependencies: `m4, flex, bison`
```bash
sudo apt-get install m4
sudo apt-get install flex
sudo apt-get install bison
```

### System packages: `GMP,PBC,pypbc`
#### the install for GMP
```bash
wget https://gmplib.org/download/gmp/gmp-6.1.2.tar.lz
lzip -d gmp-6.1.2.tar.lz
tar -xvf gmp-6.1.2.tar
cd gmp-6.1.2

./configure
make
make check
sudo make install
```

#### the install for PBC
```bash
wget https://crypto.stanford.edu/pbc/files/pbc-0.5.14.tar.gz
tar -xvf pbc-0.5.14.tar.gz
cd pbc-0.5.14

./configure
make
sudo make install
```


#### the install for pypbc
```bash
git clone https://github.com/debatem1/pypbc
sudo python3 setup.py install
sudo pip3 install pypbc
```



## Source Code Structure

```
src/
├── Ali_scheme.py                    #  implementation of Bilinear Pairing-Based Hybrid Signcryption for Secure Heterogeneous Vehicular Communications
├── Liu_scheme.py                    #  implementation of Mutual Heterogeneous Signcryption Schemes for 5G Network Slicings
├── Luo_scheme.py                    #  implementation of Mutual heterogeneous signcryption schemes with different system parameters for 5G network slicings
├── Niu_scheme.py                    #  implementation of Privacy-Preserving Mutual Heterogeneous Signcryption Schemes Based on 5G Network Slicing
├── Ullah_scheme.py                  #  implementation of A Conditional Privacy Preserving Heterogeneous Signcryption Scheme for Internet of Vehicles
├── Wang_scheme.py                   #  implementation of Efficient and Provably Secure Offline/Online Heterogeneous Signcryption Scheme for VANETs
├── Our_scheme.py                    #  implementation of MRHSCV
├── sender_80.py                     #  Sender-side (qbits=512, rbits=160): measures sender computation time only
├── sender_112.py                    #  Sender-side (qbits=1024, rbits=224): measures sender computation time only
├── sender_128.py                    #  Sender-side (qbits=1536, rbits=256): measures sender computation time only
├── receiver_80.py                   #  Receiver-side (qbits=512, rbits=160): measures receiver computation time only
├── receiver_112.py                  #  Receiver-side (qbits=1024, rbits=224): measures receiver computation time only
├── receiver_128.py                  #  Receiver-side (qbits=1536, rbits=256): measures receiver computation time only
├── main_80.py                       #  Sender and Receiver(qbits=512, rbits=160): measures total computation time
├── main_112.py                      #  Sender and Receiver(qbits=1024, rbits=224): measures total computation time
├── main_128.py                      #  Sender and Receiver(qbits=1536, rbits=256): measures total computation time
├── utili.py                         # toolkit for implementation

```




## Quick Start
The sender, receiver and overall execution time of different schemes can be measured simultaneously

### 1) measures sender computation time


```bash
sudo python3 sender_80.py
sudo python3 sender_112.py
sudo python3 sender_128.py
```



### 2) measures receiver computation time

```bash
sudo python3 receiver_80.py
sudo python3 receiver_112.py
sudo python3 receiver_128.py
```

### 3) measures total computation time


```bash
sudo python3 main_80.py
sudo python3 main_112.py
sudo python3 main_128.py
```





