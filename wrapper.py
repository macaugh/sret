import sys
import main

def main_wrapper():
    # Read targets from stdin
    targets = sys.stdin.readlines()

    # Process each target
    for target in targets:
        target = target.strip()

        # Call the main function in main.py
        response = main.main(target)

        # Check the 'vulnerable' field in the response and print the appropriate message
        if response['vulnerable']:
            print(f"[P2-NEEDS-INVESTIGATION] {target}")
        else:
            print(f"[P3-NOT-VULNERABLE] {target}")

if __name__ == "__main__":
    main_wrapper()