"""
Kaggle Submission Packaging Script.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from package_submission import package

if __name__ == "__main__":
    package()
