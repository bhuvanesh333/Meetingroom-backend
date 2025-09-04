from fastapi import FastAPI
from database import dataBase_Initializer

import logging
from fastapi.middleware.cors import CORSMiddleware
from routes.Routes import IncludeRoutes

#tables.Base.metadata.create_all(dataBase_Initializer.engine)
app=FastAPI()
excluded_paths = {"/"
             }

try:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        
    )
    logging.info("CORS middleware added successfully.")
except Exception as e:
    logging.error(f"Failed to add CORS middleware: {str(e)}")


class Initialize:
    IncludeRoutes(app)

@app.on_event("shutdown")
async def shutdown_event():
    # Clean up resources here
    pass
