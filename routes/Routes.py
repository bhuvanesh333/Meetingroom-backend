from fastapi import FastAPI


class IncludeRoutes:

    def __init__(self,app:FastAPI) :
        self.app = app
        self.includeRoutes()
    
    def includeRoutes(self):
        pass