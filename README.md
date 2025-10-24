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


```bash
# 0) Clone the repository
git clone https://gitlab.example.com/your-group/mrhscv-pi.git
cd mrhscv-pi

# 1) Log system information (optional)
bash scripts/collect_sysinfo.sh > artifacts/sysinfo_$(date +%F).log

# 2) Install dependencies (requires sudo)
sudo bash scripts/bootstrap_pi.sh

# 3) Create virtual environment & install packages
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip wheel
pip install -r requirements.txt

# 4) Build and install pypbc (if not auto-built)
bash scripts/build_pbc.sh
pip install ./third_party/pypbc

# 5) Run quick benchmark (encryption/decryption/sign/verify)
python bench/run_micro_bench.py --repeat 1000 --json artifacts/microbench.json

# 6) Run ns-3 simulation (end-to-end latency)
python sim/run_ns3_scenario.py --time 100 --pkt-size 200 --interval 1.0 \
  --topo data/cangzhou.net.xml --fcd data/fcd_0_100s.xml \
  --out artifacts/ns3_latency.csv

# 7) Plot results
python viz/plot_latency.py artifacts/ns3_latency.csv --out figs/latency.png
```


## Detailed Setup Steps

### 1) System and Basic Tools

```bash
sudo apt update
sudo apt install -y build-essential cmake git pkg-config \
  libffi-dev libgmp-dev libmpfr-dev libmpc-dev python3-venv python3-dev
```

### 2) Python and Virtual Environment

```bash
python3 -V
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip wheel
pip install -r requirements.txt
```

> If `_cffi_backend` is missing: `sudo apt install python3-cffi libffi-dev && pip install cffi`.

### 3) GMP/PBC/pypbc Installation

```bash
cd third_party/pbc
./configure --prefix=$(pwd)/install --disable-shared
make -j$(nproc) && make install
export C_INCLUDE_PATH=$(pwd)/install/include:$C_INCLUDE_PATH
export LIBRARY_PATH=$(pwd)/install/lib:$LIBRARY_PATH
export LD_LIBRARY_PATH=$(pwd)/install/lib:$LD_LIBRARY_PATH
cd ../../
pip install ./third_party/pypbc
```

### 4) ns-3 Python Binding

```bash
cd ~ && git clone https://gitlab.com/nsnam/ns-3-dev.git ns-3
cd ns-3 && git checkout ns-3.46
sudo apt install -y python3-dev libqt5svg5-dev
./ns3 configure --enable-examples --enable-tests --build-profile=optimized
./ns3 build
./ns3 run examples/tutorial/first.py
```

> Python binding requires `cppyy`. If build errors occur, upgrade `setuptools`, `pip`, and `wheel`, then reinstall `cppyy` and `cppyy-cling`.

### 5) MRHSCV Source Compilation

Core protocol under `core/` is pure Python + pypbc, no compilation required.

## Running and Reproducing Experiments

### A. Encryption/Decryption Micro-benchmark

```bash
source .venv/bin/activate
python bench/run_micro_bench.py --repeat 2000 --warmup 200 \
  --out artifacts/microbench.csv --json artifacts/microbench.json
```

### B. ns-3 End-to-End Latency Scenario

```bash
source .venv/bin/activate
python sim/run_ns3_scenario.py \
  --time 100 --pkt-size 200 --interval 1.0 \
  --wifi-mode ErpOfdmRate24Mbps --radius 2000 \
  --topo data/cangzhou.net.xml --fcd data/fcd_0_100s.xml \
  --out artifacts/ns3_latency.csv --log artifacts/ns3_run.log
```

### C. Optional Raspberry Pi Power Measurement

* Use a USB power meter for energy readings aligned with JSON timestamps.
* If unavailable, use `vcgencmd measure_temp` or thermal sensors; see `scripts/log_temp.sh`.

## Result Validation and Self-check

1. **Commit snapshot:** `git rev-parse HEAD | tee artifacts/git_commit.txt`
2. **System snapshot:** `scripts/collect_sysinfo.sh > artifacts/sysinfo.log`
3. **Dependency hash:** `pip freeze > artifacts/pip_freeze.txt`
4. **Meta-check:** `scripts/check_meta.py` validates runtime configurations.

## FAQ

* **Q1: Missing _cffi_backend** → Install `python3-cffi` and `libffi-dev`, then `pip install cffi`.
* **Q2: pypbc compile/link errors** → Ensure environment variables point to PBC `install` directories.
* **Q3: cppyy/cling errors** → Upgrade build tools and reinstall `cppyy`, `cppyy-cling`.
* **Q4: UdpEcho signature mismatch** → Use `UdpEchoClientHelper(string_ip, port)` per `sim/ns3_helpers.py`.
* **Q5: Timing trustworthiness** → Benchmarks use `time.perf_counter_ns()`; all raw CSV/JSON logs are preserved in `artifacts/`.

## Security and Compliance

* No confidential keys or data included. Default parameters are public test curves.
* All results can be regenerated from source; reproducibility script provided: `scripts/one_click_reproduce.sh`.

## Citation

```
@software{mrhscv_pi_artifact,
  title  = {MRHSCV Raspberry Pi Artifact},
  author = {Your Name and Coauthors},
  year   = {2025},
  url    = {https://gitlab.example.com/your-group/mrhscv-pi},
  note   = {Version commit: <git hash>}
}
```

## Acknowledgments and License

* **License**: Apache-2.0 (or as appropriate)
* **Acknowledgments**: Thanks to the ns-3 and PBC communities for their open-source contributions.

---

### Key Scripts Summary

* `scripts/bootstrap_pi.sh`: Install dependencies and configure environment.
* `scripts/build_pbc.sh`: Build PBC and set environment paths.
* `scripts/collect_sysinfo.sh`: Log system details.
* `scripts/one_click_reproduce.sh`: Fully automated reproduction workflow for artifact evaluation.
