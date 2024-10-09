from typing import TypedDict


class ApiResponse(TypedDict):
    successful: bool
    message: str
    errors: list
    data: list | dict
    code: int
