import logging
activity_logger = logging.getLogger("activity")
security_logger = logging.getLogger("security")
system_logger = logging.getLogger("system")

class AppLogger:
    @staticmethod
    def log_activity(msg, user=None, status="INFO"):
        extra = f" | user={user.id if user else 'Anon'}"
        full_msg = f"{msg}{extra}"

        if status == "INFO":
            activity_logger.info(full_msg)
        elif status == "ERROR":
            activity_logger.error(full_msg)

    @staticmethod
    def log_security(msg, user=None, path=None):
        user_info = f"user={user.id if user else 'Anon'}"
        path_info = f"path={path if path else 'N/A'}"
        security_logger.warning(f"{msg} | {user_info} | {path_info}")


    @staticmethod
    def log_system_error(msg, include_traceback=False):

        system_logger.error(msg, exc_info=include_traceback)