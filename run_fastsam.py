import time
import torch
import cv2
import os
from ultralytics import FastSAM


# Force single thread (reduces memory overhead)
torch.set_num_threads(1)
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
print("Enviroment and torch configuration done.")

# Load smallest ~23MB model with memory optimization
model_name = "FastSAM-s.pt"
print(f"Loading {model_name} model..")
model = FastSAM(model_name)
print(f"{model_name} model loading done.")

# Ensure FP32 (faster on ARM without FP16)
model.model.float()  
model.overrides["conf"] = 0.5
model.overrides["iou"] = 0.9
model.overrides["max_det"] = 100
print("Model configuration done.")

def main():
    start = time.time()
    input_path = "image.jpg"

    # Run inference with minimal settings
    print("Model inference started...")
    results = model(
        input_path,
        device="cpu",
        verbose=False,
        stream=False,
        imgsz=320,  # Force smaller input size for model
        half=False,  # No FP16 on CPU
    )
    print("Model inference done.")
    elapsed = time.time() - start

    # Save
    output_path = "output.jpg"
    results[0].save(output_path)

    print(f"Output saved to {output_path}")
    print(f"Model inference took {elapsed:.1f}s")


if __name__ == "__main__":
    main()
