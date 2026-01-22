import traceback
from typing import Optional, Dict, Any

from manimator.logging.logger import logging


class ManimatorException(Exception):
    """
    Base exception for Manimator.
    Captures location, cause, and optional context.
    """

    def __init__(
        self,
        message: str,
        *,
        cause: Optional[Exception] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.cause = cause
        self.context = context or {}

        # Extract traceback info if cause exists
        if cause and cause.__traceback__:
            tb = cause.__traceback__
            while tb.tb_next:
                tb = tb.tb_next  

            self.lineno = tb.tb_lineno
            self.file_name = tb.tb_frame.f_code.co_filename
        else:
            self.lineno = None
            self.file_name = None

        super().__init__(self.__str__())

        # Centralized logging
        logging.error(self.__str__())

    def __str__(self) -> str:
        lines = [f"{self.message}"]

        if self.file_name and self.lineno:
            lines.append(f"Location: {self.file_name}:{self.lineno}")

        if self.context:
            lines.append("Context:")
            for k, v in self.context.items():
                lines.append(f"   - {k}: {v}")

        if self.cause:
            lines.append(
                f"Cause: {type(self.cause).__name__}: {self.cause}"
            )

        return "\n".join(lines)
