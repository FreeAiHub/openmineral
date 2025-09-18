# Ensure the repository root is on sys.path so tests can import the backend package reliably
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
