import math
import time
import multiprocessing as mp

start_time = time.time()

# Determines particle type based on PDG code (1 for positive pion, -1 for negative pion, 0 otherwise)
def check_type(pdg_code):
    if abs(pdg_code) == 211:
        return 1 if pdg_code > 0 else -1
    return 0

def process_event_batch(batch_data):
    batch_positive = 0
    batch_negative = 0
    batch_events = len(batch_data)
    
    for event_data in batch_data:
        pos = 0
        neg = 0
        for pdg_code in event_data:
            t = check_type(pdg_code)
            if t == 1:
                pos += 1
            elif t == -1:
                neg += 1
        
        batch_positive += pos
        batch_negative += neg
    
    return {
        'batch_positive': batch_positive,
        'batch_negative': batch_negative,
        'batch_events': batch_events
    }

def process_file(file_index):
    base = '/Users/mihai-edi/Projects/Code Sinaia/Data_Science/Dataset/output-Set'
    file_path = f"{base}{file_index}.txt"
    
    batch_size = 1000
    event_batches = []
    current_batch = []
    
    try:
        with open(file_path, "r") as infile:
            print(f"[Process {mp.current_process().name}] Processing file {file_index}: {file_path}")
            
            while True:
                first_line = infile.readline()
                if not first_line:
                    break
                    
                try:
                    event_id, num_particles = map(int, first_line.strip().split())
                except ValueError:
                    continue  

                # Read event data
                event_pdg_codes = []
                for _ in range(num_particles):
                    line = infile.readline()
                    if not line:
                        break
                    try:
                        pdg_code = int(line.strip().split()[3])
                        event_pdg_codes.append(pdg_code)
                    except (IndexError, ValueError):
                        continue  

                current_batch.append(event_pdg_codes)
                
                # When batch is full, add to batches list
                if len(current_batch) >= batch_size:
                    event_batches.append(current_batch)
                    current_batch = []
            
            # Add remaining events as final batch
            if current_batch:
                event_batches.append(current_batch)
        
        # Process batches sequentially within this file process
        file_positive = 0
        file_negative = 0
        file_events = 0
        
        if event_batches:
            # Process each batch sequentially (no nested multiprocessing)
            for batch in event_batches:
                batch_result = process_event_batch(batch)
                file_positive += batch_result['batch_positive']
                file_negative += batch_result['batch_negative']
                file_events += batch_result['batch_events']
        
        # Calculate per-file statistics
        if file_events > 0:
            avg_positive = file_positive / file_events
            avg_negative = file_negative / file_events
            mean_difference = abs(avg_positive - avg_negative)
            
            # Calculate uncertainties (standard error of the mean)
            uncertainty_positive = math.sqrt(avg_positive / file_events)
            uncertainty_negative = math.sqrt(avg_negative / file_events)
            combined_uncertainty = math.sqrt(uncertainty_positive**2 + uncertainty_negative**2)
            
            # Calculate significance (sigma from zero)
            significance = mean_difference / combined_uncertainty if combined_uncertainty > 0 else 0
            
            # Statistical significance test (typically > 3 sigma is significant)
            is_significant = "Yes" if significance > 3 else "No"
            
            result = {
                'file_index': file_index,
                'file_events': file_events,
                'file_positive': file_positive,
                'file_negative': file_negative,
                'avg_positive': avg_positive,
                'avg_negative': avg_negative,
                'uncertainty_positive': uncertainty_positive,
                'uncertainty_negative': uncertainty_negative,
                'mean_difference': mean_difference,
                'combined_uncertainty': combined_uncertainty,
                'significance': significance,
                'is_significant': is_significant,
                'num_batches': len(event_batches)
            }
            
            print(f"[Process {mp.current_process().name}] File {file_index} completed: {file_events} events in {len(event_batches)} batches")
            return result
                        
    except FileNotFoundError:
        print(f"[Process {mp.current_process().name}] File {file_path} not found, skipping...")
        return None

if __name__ == '__main__':
    # Configuration
    total_files = 11
    num_file_processes = min(4, mp.cpu_count())
    
    print(f"Processing {total_files} files using {num_file_processes} processes")
    print(f"Each file will batch events into groups of 1000 for sequential processing within each process")
    
    file_results = []
    
    # Process files in parallel
    with mp.Pool(processes=num_file_processes) as pool:
        # Submit file processing tasks
        async_results = [pool.apply_async(process_file, (i,)) for i in range(0, total_files)]
        
        # Collect results from all files
        for i, async_result in enumerate(async_results):
            try:
                result = async_result.get()  # Get result from the file
                if result:
                    file_results.append(result)
                    print(f"File {i} completed with {result['file_events']} events processed in {result['num_batches']} batches")
            except Exception as exc:
                print(f"File {i} generated an exception: {exc}")

    # Sort results by file index for consistent output
    file_results.sort(key=lambda x: x['file_index'])

    # Print results for each file
    for result in file_results:
        print(f"\nFile {result['file_index']} Results:")
        print(f"  Events: {result['file_events']} (processed in {result['num_batches']} batches)")
        print(f"  Average Positive Pions per Event: {result['avg_positive']:.5f} ± {result['uncertainty_positive']:.5f}")
        print(f"  Average Negative Pions per Event: {result['avg_negative']:.5f} ± {result['uncertainty_negative']:.5f}")
        print(f"  Mean Difference (Average Positive - Average Negative): {result['mean_difference']:.5f}")
        print(f"  Mean Difference is {result['significance']:.2f} sigma from zero, indicating that it is statistically {'significant' if result['is_significant'] == 'Yes' else 'insignificant'}.")

    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")
    print(f"Used {num_file_processes} processes for files with event batching (1000 events per batch)")