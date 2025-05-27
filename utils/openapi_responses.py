from constants.code import Code


class Response200:
    @classmethod
    def response(cls, properties=None, *examples):

        if examples == []:
            examples = [{'code': 100200}]
        if properties is None:
            properties = {"code": {
                "type": "string",
                "description": "成功提示码",
            }}

        examples = {f"jsonExample{index+1}": example for index, example in enumerate(examples)}

        return {
            "description": "成功返回",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": properties,
                    },
                    "examples": examples
                }
            }
        }


class Response201(Response200):
    @classmethod
    def response(cls, properties=None, *examples):
        return super().response(properties, *examples)


class Response204:
    NO_CONTENT = {"content": {"text/plain": {"schema": {"type": "string", "example": "No Content"}}}}


class Response401:
     UNAUTHORIZED = {"content": {"application/json": {"schema": {"type": "object", "example":"{'message': '请先登录后再请求', 'code': 100401}"}}}}


class Response403:
    @classmethod
    def response(cls, *args):
        examples = dict()
        for index, code in enumerate(args):
            examples.update({
                f"jsonExample{index+1}": {
                    "description": "权限报错提示",
                    "value": {'message': Code.message(code), 'code': code}
                }
            })

        return {
            "description": "权限报错提示",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "权限相关的错误提示信息",
                            },
                            "code": {
                                "type": "integer",
                                "description": "权限相关的错误代码",
                            }
                        }
                    },
                    "examples": examples,
                }
            },
        }


class Response400:
    @classmethod
    def response(cls, *args):
        examples = dict()
        for index, code in enumerate(args):
            examples.update({
                f"jsonExample{index+1}": {
                    "description": "400报错提示",
                    "value": {'message': Code.message(code), 'code': code}
                }
            })

        return {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "错误提示信息",
                            },
                            "code": {
                                "type": "integer",
                                "description": "错误代码",
                            }
                        }
                    },
                    "examples": examples,
                }
            },
            "description": "400报错提示",
        }
