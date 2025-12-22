from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import get_current_user
from app.database import get_database
from app.models import ProfileCreate, ProfileUpdate, ProfileResponse, UserInDB

router = APIRouter()

@router.post("/profile", response_model=ProfileResponse)
async def create_profile(profile: ProfileCreate, current_user: UserInDB = Depends(get_current_user), db = Depends(get_database)):
    existing_profile = await db["profiles"].find_one({"email": current_user.email})
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists")
    
    # Ensure the profile email matches the user email or allow it to be different? 
    # The prompt asks for email in profile. I'll assume it can be different or same.
    # But for simplicity, let's link it to the current_user.
    
    profile_data = profile.model_dump()
    profile_data["user_id"] = current_user.username # Link to user
    
    new_profile = await db["profiles"].insert_one(profile_data)
    created_profile = await db["profiles"].find_one({"_id": new_profile.inserted_id})
    return ProfileResponse(**created_profile)

@router.get("/profile", response_model=ProfileResponse)
async def get_profile(current_user: UserInDB = Depends(get_current_user), db = Depends(get_database)):
    profile = await db["profiles"].find_one({"user_id": current_user.username})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return ProfileResponse(**profile)

@router.put("/profile", response_model=ProfileResponse)
async def update_profile(profile_update: ProfileUpdate, current_user: UserInDB = Depends(get_current_user), db = Depends(get_database)):
    profile = await db["profiles"].find_one({"user_id": current_user.username})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    update_data = {k: v for k, v in profile_update.model_dump().items() if v is not None}
    
    if update_data:
        await db["profiles"].update_one({"user_id": current_user.username}, {"$set": update_data})
    
    updated_profile = await db["profiles"].find_one({"user_id": current_user.username})
    return ProfileResponse(**updated_profile)

@router.delete("/profile")
async def delete_profile(current_user: UserInDB = Depends(get_current_user), db = Depends(get_database)):
    result = await db["profiles"].delete_one({"user_id": current_user.username})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"detail": "Profile deleted"}
