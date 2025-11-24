import subprocess
import sys

def start_red():
    print("--- Starting Redbot Instance: 'PUTNAMEHERE' ---")
    
    # The command you requested
    command = "source /home/container/redenv/bin/activate && redbot PUTNAMEHERE"
    
    # We must use executable='/bin/bash' because 'source' is a bash command 
    # (standard /bin/sh usually uses '.' instead of 'source')
    try:
        subprocess.run(command, shell=True, executable='/bin/bash')
    except KeyboardInterrupt:
        # This handles pressing Ctrl+C gracefully without printing a python error trace
        print("\nBot stopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    start_red()