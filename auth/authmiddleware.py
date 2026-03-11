from datetime import datetime,timezone
import re
from typing import List, Optional
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from bson import ObjectId

from auth.jwt_token_manger import token_manager_singleton
from database.dataBase_Initializer import get_blacklisted_tokens, get_user_sessions  ,get_all_type_users
from schema.commonSchema import ROLE

class AuthMiddleware(BaseHTTPMiddleware):
    
    def __init__(self, app, public_paths: Optional[List[str]] = None):
        super().__init__(app)
        self.token_manager = token_manager_singleton
        self.public_paths = public_paths 

    def user_find_by_id(self, user_id: str):
        cluster_admins,cluster_users = get_all_type_users()
        cluster_admins_user = cluster_admins.find_one({"_id": ObjectId(user_id), "is_online": True})
        if cluster_admins_user:
            return cluster_admins_user,ROLE.CLUSTER_ADMIN
        cluster_users_user = cluster_users.find_one({"_id": ObjectId(user_id), "is_online": True})
        if cluster_users_user:
            return cluster_users_user,ROLE.CLUSTER_USER
    
    async def dispatch(self, request: Request, call_next)-> JSONResponse:
        """
        Main middleware method that processes every request
        """
        # Skip authentication for public paths
        if self._is_public_path(request):
            return await call_next(request)
        
        try:
            # Step 1: Extract and validate token
            token = self._extract_token(request)
            if not token:
                return self._unauthorized_response("Authentication token required")
            
            # Step 2: Check if token is blacklisted
            if await self._is_token_blacklisted(token):
                return self._unauthorized_response("Token has been revoked")
            
            # Step 3: Verify JWT token
            payload = self.token_manager.verify_token(token)
    
            if not payload:
                return self._unauthorized_response("Invalid or expired token")
            
            # Step 4: Validate token type
            if payload.get("type") != "access":
                return self._unauthorized_response("Invalid token type")
            
            # Step 5: Extract user and session info
            user_id = payload.get("sub")
            session_token = payload.get("session_token")
            
            if not user_id or not session_token:
                return self._unauthorized_response("Invalid token payload")
            
            # Step 6: Verify user exists and is active
            user,role = self.user_find_by_id(user_id)
            
            if not user:
                return self._unauthorized_response("User not found or inactive")
            
            # Step 7: Verify session is valid
            session = get_user_sessions().find_one({
                "user_id": user_id,
                "session_token": self.token_manager.hash_token(session_token),
                "is_online": True,
                "expire_at": {"$gt": datetime.now(timezone.utc)}
            })
            
            if not session:
                return self._unauthorized_response("Session expired or invalid")
            
            # Step 8: Update session last accessed
            get_user_sessions().update_one(
                {"_id": session["_id"]},
                {"$set": {"last_accessed": datetime.now(timezone.utc)}}
            )
            
            # Step 9: Add user context to request state
            if role == ROLE.CLUSTER_ADMIN:
                request.state.user = {
                "id": str(user["_id"]),
                "admin_name": user["admin_name"],
                "email": user["email_id"],
                "role": role,
                "session_token": session_token
            }
            elif role == ROLE.CLUSTER_USER:
                request.state.user = {
                "id": str(user["_id"]),
                "username": user["username"],
                "email": user["email_id"],
                "role": role,
                "session_token": session_token
            }

            
            # Step 10: Check authorization for protected routes
            if not self._is_authorized(request, user):
                return self._forbidden_response("Insufficient permissions")
            
            # Process the request with authentication context
            response = await call_next(request)
            
            # Add security headers
            self._add_security_headers(response)
            
            return response
            
        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except Exception as e:
            # Log unexpected errors
            print(f"Auth middleware error: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal authentication error"}
            )
    
    def _is_public_path(self, request: Request) -> bool:
        """Check if the request path is in public paths"""
        path = request.url.path
        return any(re.match(pattern, path) for pattern in self.public_paths)
    
    def _extract_token(self, request: Request) -> Optional[str]:
        """Extract token from Authorization header"""
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header[7:]  # Remove "Bearer " prefix
        return None
    
    async def _is_token_blacklisted(self, token: str) -> bool:
        """Check if token is blacklisted in MongoDB"""
        hashed_token = self.token_manager.hash_token(token)
        blacklisted = get_blacklisted_tokens().find_one({
            "token": hashed_token
        })
        return blacklisted is not None
    
    def _is_authorized(self, request: Request, user: dict) -> bool:
        """
        Check if user has permission to access the route
        You can extend this for more complex role-based access
        """
        path = request.url.path
        method = request.method
        
        # Admin can access everything
        if user.get("role") == "admin":
            return True
        
        # User-specific routes
        if path.startswith("/user/") and "admin" in path:
            return user.get("role") == "admin"
        
        # Example: Only admins can delete
        if method == "DELETE" and user.get("role") != "admin": #FIXME
            return True
            return False
        
        # Add more authorization rules as needed
        return True
    
    def _unauthorized_response(self, detail: str) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": detail},
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    def _forbidden_response(self, detail: str) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": detail}
        )
    
    def _add_security_headers(self, response):
        """Add security headers to response"""
        security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block"
        }
        for header, value in security_headers.items():
            response.headers[header] = value