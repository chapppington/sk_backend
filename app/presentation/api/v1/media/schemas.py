from pydantic import BaseModel


class UploadFileResponseSchema(BaseModel):
    file_path: str
    bucket_name: str
    file_url: str | None
    message: str = "File uploaded successfully"
