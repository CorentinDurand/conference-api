from typing import Set

from fastapi import Depends, Header, HTTPException, status

# Simple role-based access control via header X-User-Role.
# Roles are lowercase for comparison: "admin", "event_manager", "viewer".
VALID_ROLES: Set[str] = {"admin", "event_manager", "viewer"}


def require_role(*allowed_roles: str):
    allowed = {r.lower() for r in allowed_roles}

    def dependency(x_user_role: str = Header(..., alias="X-User-Role")):
        role = x_user_role.lower()
        if role not in VALID_ROLES:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unknown role",
            )
        if role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role",
            )
        return role

    return Depends(dependency)
