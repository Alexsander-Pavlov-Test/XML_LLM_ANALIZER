import pathlib
from fastapi import HTTPException, status

from api_v1.regex import check_xml_file
from api_v1.exeptions import ValidationError, APIFileNotFoundError


def correct_xml_path(path: str) -> pathlib.Path:
    if not path:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=dict(file='No data'))
    path = pathlib.Path(str(path))
    if not path.exists():
        raise APIFileNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=dict(file='File is not found'),
            )
    if not path.is_file():
        raise APIFileNotFoundError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=dict(file='Object is not file'),
            )
    file_ = path.name
    if not check_xml_file(file_):
        raise ValidationError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=dict(file='File is not XML'),
            )
    return path
