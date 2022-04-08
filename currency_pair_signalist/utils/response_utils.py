from typing import Optional

from rest_framework import status as status_code

from currency_pair_signalist.constants.base_constants import BaseConstants


class ResponseUtils:
    @classmethod
    def get_final_response_result(
            cls,
            code: int = status_code.HTTP_400_BAD_REQUEST,
            status: str = BaseConstants.error,
            data: Optional[dict] = None) -> dict:

        if not data:
            data = {}

        return {
            BaseConstants.code: code,
            BaseConstants.status: status,
            BaseConstants.data: data,
        }
