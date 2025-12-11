from fastapi import FastAPI

import logging
from fastapi.middleware.cors import CORSMiddleware
from auth.authmiddleware import AuthMiddleware
from routes.Routes import IncludeRoutes
from service.MeeQ_service.Scheduler.Cluster_UserScheduler import ClusterUserScheduler

app=FastAPI()
excluded_paths = {"/api/cluserUserAuth/ClusterUserLogin",
                  "/api/cluserUserPage/stream",
                  "/api/cluserUserAuth/ClusterUserSignup",
                  "/api/cluserAdminAuth/ClusterAdminLogin"}

try:
    app.add_middleware(
        AuthMiddleware,
        public_paths=excluded_paths
    )
    logging.info("Auth middleware added successfully.")
except Exception as e:
    logging.error(f"Failed to add Auth middleware: {str(e)}")
    
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



@app.on_event("startup")
def start_scheduler():
    ClusterUserScheduler.scheduler.start()

@app.on_event("shutdown")
def stop_scheduler():
    ClusterUserScheduler.scheduler.shutdown()

@app.get("/")
def read_root():
    return {"message": "Scheduler running"}

class Initialize:
    IncludeRoutes(app)

