from dataclasses import dataclass


@dataclass()
class SuccessResponse:
    """dataclass to store the success requests' responses"""
    body: str


@dataclass()
class ErrorResponse:
    """dataclass to store the error requests' responses"""
    body: str
