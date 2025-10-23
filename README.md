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

This README aims to help reviewers and researchers reproduce the **MRHSCV** protocol implementation on the Raspberry Pi platform. It includes:

1. Public implementation of core cryptographic primitives (signcryption, verification, etc.);
2. Unified software stack (GMP/PBC/pypbc + ns-3 Python bindings + dependencies);
3. One-click scripts and validation utilities ensuring reproducibility on **Raspberry Pi 4B/5 (64-bit OS)**.

## Hardware and System

* **SoC**: Raspberry Pi 4B (4/8GB) or Raspberry Pi 5 (recommended)
* **Architecture**: aarch64 (64-bit)
* **OS**: Raspberry Pi OS (64-bit) / Ubuntu Server 22.04 (ARM64)
* **Compiler**: gcc/g++ ≥ 11
* **Storage**: ≥ 32GB microSD or NVMe (for Pi 5)

> Run `scripts/collect_sysinfo.sh` to log your system information.

## Software Dependencies

* Python 3.8/3.10 (recommended: 3.10; for pypbc use 3.8)
* System packages: `build-essential cmake git pkg-config libffi-dev libgmp-dev libmpfr-dev libmpc-dev`
* PBC Library: `libpbc` (build from source)
* Python packages: `virtualenv wheel cffi cryptography numpy pandas matplotlib cppyy`
* ns-3 (≥ 3.44 with Python bindings)

> Run [`scripts/bootstrap_pi.sh`](scripts/bootstrap_pi.sh) for automatic installation.

## Quick Start (5 Minutes)

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

## Source Code Structure

```
mrhscv-pi/
├── core/                    # MRHSCV core protocol implementation
│   ├── keygen.py            # Key generation / parameter setup
│   ├── signcrypt.py         # Signcryption interface
│   ├── unsigncrypt.py       # Unsigncryption / verification
│   ├── utils.py             # Utilities (hash, encode, serialize)
│   └── params/              # Curve & PBC parameters (.param)
├── sim/                     # ns-3 integration and simulation scripts
│   ├── ns3_helpers.py       # Python helper (UdpEchoClientHelper, etc.)
│   ├── run_ns3_scenario.py  # Main simulation script
│   └── configs/             # Scenario configs
├── bench/                   # Micro-benchmarks
│   └── run_micro_bench.py
├── viz/                     # Visualization scripts
│   └── plot_latency.py
├── scripts/                 # Automation scripts
│   ├── bootstrap_pi.sh
│   ├── build_pbc.sh
│   ├── collect_sysinfo.sh
│   └── one_click_reproduce.sh
├── third_party/
│   ├── pbc/                 # PBC source (optional submodule)
│   └── pypbc/               # Python bindings
├── data/                    # Topology and trace data
│   ├── cangzhou.net.xml
│   └── fcd_0_100s.xml
├── artifacts/               # Logs, results, metadata
├── figs/                    # Figures and plots
├── requirements.txt
├── CITATION.cff
└── LICENSE
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
