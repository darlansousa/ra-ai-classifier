
def ResponseModel(data, message):
    if type(data) is list:
        data = [data]

    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
