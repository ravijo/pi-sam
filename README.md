# pi-sam
Run **Fast Segment Anything Model (FastSAM)** on a **Raspberry Pi Zero 2W (512 MB RAM)** using CPU-only PyTorch

This repository documents a real, reproducible setup where FastSAM runs fully offline on extremely constrained hardware (no GPU, no cloud, just patience).

## ✨ What this repo shows

- Installing **Python 3.9.25** via pyenv on Raspberry Pi Zero 2W
- Running **FastSAM** with **512 MB RAM** using swap
- Handling dependency conflicts and OpenCV issues
- Practical performance numbers and memory usage
- A reference setup that *actually works*

## 🧪 Tested hardware & software

| Component   | Details                       |
|-------------|-------------------------------|
| Board       | Raspberry Pi Zero 2W          |
| RAM         | 512 MB                        |
| CPU         | ARM Cortex-A53 (aarch64)      |
| OS          | Raspberry Pi OS Lite / Debian |
| Python      | 3.9.25 (via pyenv)            |
| PyTorch     | 2.8.0+cpu                     |
| Ultralytics | 8.4.12                        |
| OpenCV      | 4.13.0.92 (headless)          |
| Storage     | microSD (swap-heavy)          |

## ⚠️ Warnings

- Python 3.9 installation via pyenv takes significant time
- Swap is mandatory (2 GB or more)
- Heavy swap usage will wear SD cards. Use a good one
- Model inference is slow (~14 seconds per image)
- Peak memory usage exceeds 1 GB swap
- This is for experimentation & learning, not production

## 🔁 Increase swap memory (IMPORTANT)

FastSAM **will not run reliably** on Raspberry Pi without increasing swap memory.

👉 Follow the exact swap setup instructions [here](https://github.com/ravijo/pi-llm?tab=readme-ov-file#-step-2-increase-swap-memory)

Complete this step before proceeding further.

## 🧠 Model used

This repo uses a compact vision model:

- **FastSAM-s** (small variant)
- Framework: Ultralytics
- Task: Image segmentation (Segment Anything)

Larger variants may consume even more resources.

## 🔧 Step 1: Set up pyenv environment

The default Python on Raspberry Pi OS is 3.13, but we need Python 3.9 for compatibility.

Configure pyenv:

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

Add these to your `~/.bashrc` for persistence:

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
```

## 🛠️ Step 2: Install build dependencies

```bash
sudo apt update && sudo apt install -y \
    libssl-dev libffi-dev libreadline-dev \
    libbz2-dev libsqlite3-dev libncursesw5-dev \
    zlib1g-dev liblzma-dev tk-dev
```

## 🐍 Step 3: Install Python 3.9.25

Clone this repository and create a temporary directory for Python build files:

```bash
git clone https://github.com/ravijo/pi-sam.git
cd ~/pi-sam
mkdir -p ~/pi-sam/tmp
```

Install Python 3.9.25 (this takes time):

```bash
TMPDIR=~/pi-sam/tmp \
PYTHON_CONFIGURE_OPTS="--without-ensurepip" pyenv install 3.9.25
```

## 📦 Step 4: Create virtual environment

```bash
~/.pyenv/versions/3.9.25/bin/python -m venv venv_3_9
source venv_3_9/bin/activate
```

Verify Python version:

```bash
python --version
# Should output: Python 3.9.25
```

## 🔥 Step 5: Install ultralytics (for FastSAM)

Install ultralytics package:

```bash
TMPDIR=~/pi-sam/tmp \
pip install --no-cache-dir --default-timeout=1000 ultralytics==8.4.12
```

### Handling dependency failures

If `sympy` installation fails during the process, install it manually:

```bash
TMPDIR=~/pi-sam/tmp \
pip install --no-cache-dir sympy==1.14.0
```

## 🧩 Step 6: Install PyTorch (CPU version)

```bash
TMPDIR=~/pi-sam/tmp \
pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

## 🔍 Step 7: Verify installation

Manually test imports in Python interpreter:

```bash
$ python
Python 3.9.25 (main, Feb  7 2026, 22:00:10) 
[GCC 14.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> import cv2
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: libGL.so.1: cannot open shared object file: No such file or directory
>>> exit()
```

## 🩹 Step 8: Fix OpenCV issue

OpenCV requires GUI libraries that aren't available. Switch to headless version.

Check installed OpenCV version:

```bash
$ pip list | grep opencv
opencv-python          4.13.0.92
```

Uninstall the GUI version:

```bash
pip uninstall -y opencv-python
```

Install headless version:

```bash
TMPDIR=~/pi-sam/tmp \
pip install --no-cache-dir opencv-python-headless==4.13.0.92
```

## ✅ Step 9: Verify all dependencies

Final verification:

```bash
$ python 
Python 3.9.25 (main, Feb  7 2026, 22:00:10) 
[GCC 14.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> import numpy
>>> import cv2
>>> from ultralytics import FastSAM
>>> exit()
```

### Installed package versions

```bash
$ pip list | grep -E "ultralytics|opencv|torch|torchvision|numpy"
numpy                  2.0.2
opencv-python-headless 4.13.0.92
torch                  2.8.0+cpu
torchvision            0.23.0
ultralytics            8.4.12
ultralytics-thop       2.0.18
```

## ▶️ Step 10: Run FastSAM

Create and run your FastSAM script:

```bash
$ python run_fastsam.py
Enviroment and torch configuration done.
Loading FastSAM-s.pt model..
FastSAM-s.pt model loading done.
Model configuration done.
Model inference started...
Model inference done.
Output saved to output.jpg
Model inference took 13.7s
```

## 📊 Observed performance

- Model inference: ~13.7 seconds per image
- RAM usage: ~284 MB
- Swap usage: ~1.1 GB (active)
- Total memory consumption: >1 GB

Memory snapshot during inference:

```
               total        used        free      shared  buff/cache   available
Mem:           416Mi       284Mi       106Mi       324Ki        89Mi       131Mi
Swap:          2.0Gi       1.1Gi       889Mi
```

## 🧩 Why this works

- Python 3.9 compatibility with ultralytics ecosystem
- CPU-optimized PyTorch build
- Headless OpenCV (no GUI dependencies)
- Swap-backed virtual memory
- FastSAM-s (small variant) model
- ARM64 build with minimal background services

## 🚫 Known limitations

- Slow inference speed (~14 seconds per image)
- Heavy swap usage (>1 GB)
- SD card wear due to constant swapping
- Limited to small model variants
- No real-time processing capability
- Memory pressure during model loading

## 💡 Who is this for?

- Edge AI / IoT enthusiasts
- Raspberry Pi developers
- People experimenting with vision models on constrained hardware
- Anyone curious about running modern AI on minimal resources
- Researchers testing deployment scenarios

## 📝 Example script

Here's a minimal `run_fastsam.py` example:

```python
from ultralytics import FastSAM

# Load model
model = FastSAM("FastSAM-s.pt")

# Run inference
results = model("input.jpg")

# Save results
results[0].save("output.jpg")
```

## 📜 License

This repo documents usage of:
- **ultralytics** - AGPL-3.0 license
- **FastSAM** - subject to its model license
- **PyTorch** - BSD-style license

Please check respective licenses before redistribution.

## 🙌 Acknowledgements

- **Ultralytics** for the FastSAM implementation
- **FastSAM** model authors
- **PyTorch** team for CPU support
- Raspberry Pi community for enabling edge AI experiments

## ⭐ Note

If this repo saved you time or helped you get FastSAM running on Pi, please feel free to ⭐ it.
