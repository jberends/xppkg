#!/usr/bin/env python
"""
This file is the main runner. You may execute this as a 'script'
"""

import sys
from xppkg.backwardcompat import main_during_development

if __name__ == "__main__":
    exit = main_during_development()
    if exit:
        sys.exit(exit)