import sys
from pathlib import Path


# Configure paths for tests
tests_dir = Path(__file__).absolute().parent
mlops_dir = tests_dir.parent
sys.path.append(str(mlops_dir))
