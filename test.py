import os

def list_files_os_walk(start_path):
  for root, _, files in os.walk(start_path):
    for file in files:
      if file.endswith('.xml'):
        print(os.path.join(root, file))

# Example usage:
list_files_os_walk('op/umd')