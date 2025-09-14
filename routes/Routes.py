from fastapi import FastAPI
from routes.MeeQ_resourse.Cluster_AdminAuthResource import cluster_admin_auth_resourse
from routes.MeeQ_resourse.Cluster_AdminPageResource import cluster_admin_page_resourse
class IncludeRoutes:

    def __init__(self,app:FastAPI) :
        self.app = app
        self.includeRoutes()
    
    def includeRoutes(self):
        self.app.include_router(cluster_admin_auth_resourse, prefix="/api/cluserAdminAuth", tags=["ClusterAdminAuth"])
        self.app.include_router(cluster_admin_page_resourse, prefix="/api/cluserAdminPage", tags=["ClusterAdminPage"])