import os
import re
from pathlib import Path

def convert_file_to_surge(input_path, output_path, policy="PROXY"):
    # Initialize lists for header and domains
    header = []
    domains = []
    
    # Read the input file
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue  # Skip empty lines
                if line.startswith('#'):
                    header.append(line)  # Store header lines
                else:
                    # Remove *. wildcard prefix if present
                    domain = line[2:] if line.startswith('*.') else line
                    # Validate domain (basic check for valid characters)
                    if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9-_\.]*[a-zA-Z0-9]$', domain):
                        domains.append(domain)
    
        # Write to output file
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write header as comments
            for line in header:
                f.write(f"{line}\n")
            if header:
                f.write("\n")  # Add a blank line after header
            # Write domains in Surge format
            for domain in domains:
                f.write(f"DOMAIN-SUFFIX,{domain},{policy}\n")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def batch_convert_to_surge(input_dir, output_dir, policy="PROXY"):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Iterate through all .txt files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_dir, filename)
            # Change extension to .conf for output
            output_filename = filename.replace('.txt', '.conf')
            output_path = os.path.join(output_dir, output_filename)
            print(f"Converting {filename} to {output_filename}")
            convert_file_to_surge(input_path, output_path, policy)

if __name__ == "__main__":
    # Define input and output directories
    input_dir = os.path.expanduser("~/data/dns-blocklists-main/wildcard")
    output_dir = os.path.expanduser("~/data/dns-blocklists-main/wildcard-surge")

    # Run batch conversion with default policy 'REJECT'
    batch_convert_to_surge(input_dir, output_dir, "REJECT")