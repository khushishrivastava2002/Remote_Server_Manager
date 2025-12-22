from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import paramiko
import io
from app.auth import get_current_user
from app.database import get_database
from app.models import (
    ServerCreate, ServerUpdate, ServerResponse, ServerInDB, UserInDB,
    CommandExecute, CommandLog
)

router = APIRouter()

@router.post("/servers", response_model=ServerResponse)
async def add_server(server: ServerCreate, current_user: UserInDB = Depends(get_current_user), db = Depends(get_database)):
    server_data = server.model_dump()
    server_data["owner_id"] = current_user.username
    
    new_server = await db["servers"].insert_one(server_data)
    created_server = await db["servers"].find_one({"_id": new_server.inserted_id})
    return ServerResponse(**created_server)

@router.get("/servers", response_model=List[ServerResponse])
async def list_servers(current_user: UserInDB = Depends(get_current_user), db = Depends(get_database)):
    servers = await db["servers"].find({"owner_id": current_user.username}).to_list(100)
    return [ServerResponse(**s) for s in servers]

@router.put("/servers/{server_id}", response_model=ServerResponse)
async def update_server(server_id: str, server_update: ServerUpdate, current_user: UserInDB = Depends(get_current_user), db = Depends(get_database)):
    # Validate ObjectId
    from bson import ObjectId
    if not ObjectId.is_valid(server_id):
        raise HTTPException(status_code=400, detail="Invalid server ID")
        
    server = await db["servers"].find_one({"_id": ObjectId(server_id), "owner_id": current_user.username})
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    
    update_data = {k: v for k, v in server_update.model_dump().items() if v is not None}
    
    if update_data:
        await db["servers"].update_one({"_id": ObjectId(server_id)}, {"$set": update_data})
    
    updated_server = await db["servers"].find_one({"_id": ObjectId(server_id)})
    return ServerResponse(**updated_server)

@router.delete("/servers/{server_id}")
async def delete_server(server_id: str, current_user: UserInDB = Depends(get_current_user), db = Depends(get_database)):
    from bson import ObjectId
    if not ObjectId.is_valid(server_id):
        raise HTTPException(status_code=400, detail="Invalid server ID")

    result = await db["servers"].delete_one({"_id": ObjectId(server_id), "owner_id": current_user.username})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Server not found")
    return {"detail": "Server deleted"}

def is_destructive_command(command: str) -> bool:
    blacklist = ["rm -rf /", "mkfs", ":(){ :|:& };:", "dd if=/dev/zero"]
    # Simple check, can be bypassed but serves as a basic guard
    for item in blacklist:
        if item in command:
            return True
    return False

@router.post("/servers/{server_id}/execute")
async def execute_command(server_id: str, cmd: CommandExecute, current_user: UserInDB = Depends(get_current_user), db = Depends(get_database)):
    from bson import ObjectId
    if not ObjectId.is_valid(server_id):
        raise HTTPException(status_code=400, detail="Invalid server ID")

    server = await db["servers"].find_one({"_id": ObjectId(server_id), "owner_id": current_user.username})
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    
    if is_destructive_command(cmd.command):
        raise HTTPException(status_code=400, detail="Destructive command detected and blocked")

    # SSH Execution
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Assuming password auth for simplicity as per requirements "password/key"
        # In a real app, we would handle keys more securely
        connect_kwargs = {
            "hostname": server["ip_address"],
            "username": server["username"],
            "port": server["port"],
        }
        if server.get("password"):
            connect_kwargs["password"] = server["password"]
        elif server.get("private_key"):
            key_file = io.StringIO(server["private_key"])
            pkey = paramiko.RSAKey.from_private_key(key_file)
            connect_kwargs["pkey"] = pkey
        else:
             raise HTTPException(status_code=400, detail="No credentials provided for server")

        ssh.connect(**connect_kwargs)
        
        stdin, stdout, stderr = ssh.exec_command(cmd.command)
        exit_status = stdout.channel.recv_exit_status()
        output_str = stdout.read().decode()
        error_str = stderr.read().decode()
        
        ssh.close()
        
        # Log execution
        log_entry = CommandLog(
            server_id=server_id,
            command=cmd.command,
            output=output_str,
            error=error_str,
            exit_status=exit_status
        )
        await db["command_logs"].insert_one(log_entry.model_dump())
        
        return {
            "command": cmd.command,
            "output": output_str,
            "error": error_str,
            "exit_status": exit_status
        }
        
    except Exception as e:
        # Log failure as well?
        raise HTTPException(status_code=500, detail=f"SSH connection failed: {str(e)}")
