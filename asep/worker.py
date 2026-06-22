from __future__ import annotations

import time
import logging
from asep.runner import TaskRunner

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("asep.worker")

def main() -> None:
    logger.info("ASEP worker started. Polling task queue in PostgreSQL.")
    runner = TaskRunner()
    while True:
        try:
            runner.run_pending_tasks()
        except Exception as e:
            logger.error(f"Error in worker polling loop: {e}", exc_info=True)
        time.sleep(5)


if __name__ == "__main__":
    main()
