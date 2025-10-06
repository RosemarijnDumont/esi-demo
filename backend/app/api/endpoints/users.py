
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
import crud, schemas, models
from api.deps import get_db, get_current_user
import cloudinary
import cloudinary.uploader
from PIL import Image
import io

router = APIRouter()

# Configure Cloudinary (replace with your actual credentials or environment variables)
cloudinary.config(
    cloud_name="your_cloud_name",
    api_key="your_api_key",
    api_secret="your_api_secret"
)

@router.post("/me/avatar", response_model=schemas.User)
async def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if not file.content_type.startswith(('image/jpeg', 'image/png')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only JPG and PNG are allowed."
        )

    # Read image, resize, and optimize
    image = Image.open(io.BytesIO(await file.read()))
    image = image.resize((200, 200), Image.ANTIALIAS)
    
    # Save the processed image to a temporary buffer
    img_byte_arr = io.BytesIO()
    if file.content_type == 'image/jpeg':
        image.save(img_byte_arr, format='JPEG', quality=85)
    else:
        image.save(img_byte_arr, format='PNG', optimize=True)
    img_byte_arr.seek(0)

    # Upload to Cloudinary
    upload_result = cloudinary.uploader.upload(
        img_byte_arr,
        folder=f"user_avatars/{current_user.id}",
        public_id="avatar",
        overwrite=True
    )
    avatar_url = upload_result.get("secure_url")

    if not avatar_url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload avatar."
        )

    # Update user's avatar URL in the database
    current_user.avatar_url = avatar_url
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return current_user
