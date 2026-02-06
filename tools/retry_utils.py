from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests


def create_retry_decorator(max_attempts=3, min_wait=1, max_wait=10):
    """
    Create a retry decorator with exponential backoff.
    
    Args:
        max_attempts (int): Maximum number of retry attempts
        min_wait (int): Minimum wait time in seconds
        max_wait (int): Maximum wait time in seconds
        
    Returns:
        Retry decorator
    """
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=min_wait, max=max_wait),
        retry=retry_if_exception_type((
            requests.exceptions.RequestException,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError
        )),
        reraise=True
    )


# Default retry decorator for API calls
api_retry = create_retry_decorator(max_attempts=3, min_wait=1, max_wait=10)
