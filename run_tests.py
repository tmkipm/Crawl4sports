import pytest
import sys
import os

def main():
    # Add the src directory to the Python path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
    
    # Run pytest with specific arguments
    pytest_args = [
        'tests',  # Test directory
        '-v',     # Verbose output
        '--cov=src',  # Coverage reporting
        '--cov-report=term-missing',  # Show missing lines in coverage
        '--asyncio-mode=auto'  # Auto-detect asyncio mode
    ]
    
    # Add additional arguments from command line
    pytest_args.extend(sys.argv[1:])
    
    # Run the tests
    sys.exit(pytest.main(pytest_args))

if __name__ == '__main__':
    main() 