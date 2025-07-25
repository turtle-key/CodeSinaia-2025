import math
import matplotlib.pyplot as plt
import numpy as np
import random
import time

threshold = 0.05

# Particle type checker
def check_type(pdg_code):
    if abs(pdg_code) == 211:
        return 1 if pdg_code > 0 else -1
    return 0

# Uncertainty calculations
def poisson_distribution(average):
    return math.sqrt(average)

def difference(no_1, no_2):
    return abs(no_1 - no_2)

def combined_uncertainty(no_1, no_2):
    return math.sqrt(no_1 + no_2)

def significance(no_1, no_2, comb_uncertainty):
    return abs(no_1 - no_2) / comb_uncertainty if comb_uncertainty != 0 else 0

# Subsampling helper: pick 3 from every 10 batches
def subsample_batches(data, group_size=10, sample_size=3):
    sampled = []
    for i in range(0, len(data), group_size):
        group = data[i:i+group_size]
        if not group:
            continue
        indices = sorted(random.sample(range(len(group)), min(sample_size, len(group))))
        sampled.extend([group[j] for j in indices])
    return sampled

file_path = "/Users/mihai-edi/Projects/Code Sinaia/Data_Science/Dataset/output-Set1.txt"
batch_size = 1000

batch_event_numbers = []
positive_pion_batches = []
negative_pion_batches = []

total_positive = 0
total_negative = 0
total_events = 0
batch_pos = 0
batch_neg = 0

# ------------------------- Batching -------------------------
start_batch = time.time()

try:
    with open(file_path, "r") as infile:
        while True:
            first_line = infile.readline()
            if not first_line:
                break
            try:
                event_id, num_particles = map(int, first_line.strip().split())
            except ValueError:
                continue  

            pos = 0
            neg = 0
            for _ in range(num_particles):
                line = infile.readline()
                try:
                    pdg_code = int(line.strip().split()[3])
                    t = check_type(pdg_code)
                    if t == 1:
                        pos += 1
                    elif t == -1:
                        neg += 1
                except (IndexError, ValueError):
                    continue  

            total_positive += pos
            total_negative += neg
            total_events += 1

            batch_pos += pos
            batch_neg += neg

            if total_events % batch_size == 0:
                batch_event_numbers.append(total_events)
                positive_pion_batches.append(batch_pos)
                negative_pion_batches.append(batch_neg)
                batch_pos = 0
                batch_neg = 0

except FileNotFoundError:
    print(f"File not found: {file_path}")
    exit()
except IOError:
    print("Error reading the file.")
    exit()

end_batch = time.time()
batch_duration = end_batch - start_batch

# ------------------------- Subsampling -------------------------
start_subsample = time.time()

subsampled_x = subsample_batches(batch_event_numbers)
subsampled_pos = subsample_batches(positive_pion_batches)
subsampled_neg = subsample_batches(negative_pion_batches)

end_subsample = time.time()
subsample_duration = end_subsample - start_subsample

# ------------------------- Plot: Pions vs Event -------------------------
plt.figure(figsize=(12, 6))
plt.plot(batch_event_numbers, positive_pion_batches,
         label="Positive pions (per 1000 events)", color="blue", linewidth=1)
plt.plot(batch_event_numbers, negative_pion_batches,
         label="Negative pions (per 1000 events)", color="red", linewidth=1)

plt.plot(subsampled_x, subsampled_pos,
         label="Subsampled Positive Pions", color="green")
plt.plot(subsampled_x, subsampled_neg,
         label="Subsampled Negative Pions", color="gold")

plt.axhline(0, color="black", linewidth=0.8)
plt.xlabel("Event number")
plt.ylabel("Pion count per batch")
plt.title("Pions per Batch (Positive vs Negative)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()

# Auto scale Y if needed
if positive_pion_batches and negative_pion_batches:
    ymin = min(positive_pion_batches + negative_pion_batches + subsampled_pos + subsampled_neg)
    ymax = max(positive_pion_batches + negative_pion_batches + subsampled_pos + subsampled_neg)
    plt.ylim(ymin, ymax)

plt.show()

# ------------------------- Plot: Runtime Comparison -------------------------
plt.figure(figsize=(6, 5))
methods = ['Batching', 'Subsampling']
times = [batch_duration, subsample_duration]
colors = ['skyblue', 'orange']

plt.bar(methods, times, color=colors)
plt.ylabel("Time (seconds)")
plt.title("Runtime Comparison: Batching vs Subsampling")
plt.grid(axis='y', linestyle='--', alpha=0.5)
for i, v in enumerate(times):
    plt.text(i, v + 0.01, f"{v:.4f}s", ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.show()