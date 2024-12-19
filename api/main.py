# import os, sys

# current_dir = os.path.abspath(os.path.dirname(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.insert(0, parent_dir) 

from litestar import Litestar, get
from users.controller import UserController

@get("/")
async def hello_world() -> dict[str, str]:
    """Handler function that returns a greeting dictionary."""
    return {"hello": "world"}


app = Litestar(route_handlers=[UserController], 
               debug=True)