import logging
import os
import sys


logger = logging.getLogger(__name__)

actions_path = os.path.join(os.getcwd(), "actions")
if actions_path not in sys.path:
    sys.path.append(actions_path)
    logger.info("Added actions package path to sys.path")
    logger.info(f"Added actions path: {actions_path}")
