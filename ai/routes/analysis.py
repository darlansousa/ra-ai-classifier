from fastapi import APIRouter

from db.functions.analysis import (
    retrieve_all_analysis,
    add_analysis,
    retrieve_analysis,
    update_analysis,
    delete_analysis,
)
from db.model.analysis import (
    AnalysisSchema,
    InsertOrUpdateAnalysisModel,
)

from db.model.response import (
    ErrorResponseModel,
    ResponseModel,
)

router = APIRouter()
