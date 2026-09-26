from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """ Define a msg de erro
    """
    message: str