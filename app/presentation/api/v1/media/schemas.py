from pydantic import BaseModel


class UploadFileResponseSchema(BaseModel):
    file_path: str
    bucket_name: str
    message: str = "File uploaded successfully"
