"""
使用 JWK 进行 JWT 生成/验证, 以用于第三方验证

公钥可公开, 私钥务必保密
"""
import typing
import datetime
import traceback

import jwt
from jwt.algorithms import RSAAlgorithm

ISSUER = "la_xin"  # 拉新(拉新客户)
EXP_TIME = 1 * 24 * 60 * 60 * 60 - 1

# 或许需要改成从环境变量中读取
RSAPublicKey = RSAAlgorithm.from_jwk(
    '{ "kty": "RSA", "e": "AQAB", "alg": "RS256", "n": "saI0peWv6iVMZIA22DiEOM0cfZy0YUDHxN2BFqm8X1EyBkrBhS0dVRjsfg0oh_05o_TgC7QOC2UEWhC9M8wYGIiCEhfxGYJtwJjz7Ht6zTTW8FsTzD-8AwoPE9boGHgEAjaC4_GaFgfXGnVoVMztiXq81RB9_3-Uwr4LHWDeVhnHVTptu1AJ6tr-UlYZE1P8vdGl5dWI_41ReTkOGTnoccjnM6nckV6hqKtpT2e04TbPZ8GVN4MCiRQ3Z-1xFZs9DgWod81EnjvwAuwPptFZFlIGO3bau5eIka-89hGdOcchRbjoETKWHTKC-SkB41rBNCa5lO4hVm9JcBviQMC9Tw" }'
)
RSAPrivateKey = RSAAlgorithm.from_jwk(
    '{   "kty": "RSA",   "d": "L0Z-QJDKqsRWeoDtF8qi1gMwy_WCxEdbY3eYPZHbAns3lxkaO_lvzxAdEMcrvFWWm542aqb2_e1apSXDVR_CYfUiuPIKRsHBt_p9ILkUS7z-X2W99SQZQ63PqXYOu0RlvLkJSOUqHybjBrWsmLUZmvdBfmsvPWqVCudNSfpX8g3jx3BF0mkKfAc6y64NlrHrSYZEocu6o5Pq9-nZbkFSjO_8hb4DPQ2NC0alqNjgxRY4A07wDFo-tJUlbsaBUXqqTPpVPeHFFIGJMCarbvRjNPHdJyIUhMsWDCqLsgb4zrp79IczDzI9WZKA0rsdC6xJmQ2vxDXbQQZq7zEJnWw_kQ",   "e": "AQAB",   "alg": "RS256",   "n": "saI0peWv6iVMZIA22DiEOM0cfZy0YUDHxN2BFqm8X1EyBkrBhS0dVRjsfg0oh_05o_TgC7QOC2UEWhC9M8wYGIiCEhfxGYJtwJjz7Ht6zTTW8FsTzD-8AwoPE9boGHgEAjaC4_GaFgfXGnVoVMztiXq81RB9_3-Uwr4LHWDeVhnHVTptu1AJ6tr-UlYZE1P8vdGl5dWI_41ReTkOGTnoccjnM6nckV6hqKtpT2e04TbPZ8GVN4MCiRQ3Z-1xFZs9DgWod81EnjvwAuwPptFZFlIGO3bau5eIka-89hGdOcchRbjoETKWHTKC-SkB41rBNCa5lO4hVm9JcBviQMC9Tw" }'
)


def generate_jwt(
    mobile: typing.Optional[str]=None,
    openid: typing.Optional[str]=None,
    data: dict = None
) -> str:
    """
    根据指定数据创建一个JWT字符串
    """
    data = data or {}
    if mobile:
        data["mobile"] = mobile
    else:
        data["openid"] = openid
    data["aud"] = ISSUER
    data["iat"] = datetime.datetime.utcnow()
    data["exp"] = datetime.datetime.utcnow() + datetime.timedelta(seconds=EXP_TIME)
    return jwt.encode(data, key=RSAPrivateKey, algorithm="RS256")


def parse_jwt(jwt_str: str) -> typing.Optional[dict]:
    """
    解析JWT对应的信息，解析失败则返回None
    """
    try:
        data = jwt.decode(
            jwt_str, key=RSAPublicKey, algorithms="RS256", audience=ISSUER
        )
        return data
    except jwt.PyJWTError:
        return


if __name__ == "__main__":
    token = generate_jwt("aber")
    print(token)
    print(parse_jwt(token))
