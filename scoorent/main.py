from fastapi import FastAPI

from scoorent.routers import router
from scoorent.exceptions_handlers import users


app = FastAPI()


# include routers
app.include_router(router)

# include exception handlers
[
    app.add_exception_handler(
        exc_class_or_status_code=exc,
        handler=users.exceptions[exc]
    ) for exc in users.exceptions.keys()
]
