class MeteoraAPIError(Exception):
    """Base exception for Meteora API errors"""
    pass

class RateLimitError(MeteoraAPIError):
    """Raised when API rate limit is exceeded"""
    pass

class PoolNotFoundError(MeteoraAPIError):
    """Raised when pool is not found"""
    pass

class InsufficientLiquidityError(MeteoraAPIError):
    """Raised when there's not enough liquidity"""
    pass

class InvalidRangeError(MeteoraAPIError):
    """Raised when liquidity range is invalid"""
    pass 