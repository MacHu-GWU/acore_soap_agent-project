# -*- coding: utf-8 -*-

"""
todo: docstring
"""

import typing as T
import json

from .utils import get_object, put_object

import acore_soap.api as acore_soap

if T.TYPE_CHECKING:  # pragma: no cover
    from mypy_boto3_s3.client import S3Client

SOAPRequest = acore_soap.SOAPRequest
SOAPResponse = acore_soap.SOAPResponse


def remove_none(kwargs: T.Dict[str, T.Any]) -> dict:
    return {k: v for k, v in kwargs.items() if v is not None}


class SoapRequestLoader:
    """
    Load ``SOAPRequest`` from different sources.
    """

    @classmethod
    def from_command(self, command: str) -> SOAPRequest:
        """
        Example:

            >>> command = ".server info"
        """
        return SOAPRequest(command=command)

    @classmethod
    def from_dict(cls, dct: dict) -> SOAPRequest:
        """
        Example:

            >>> dct = {"command": ".server info"}
        """
        return SOAPRequest.from_dict(dct)

    @classmethod
    def from_command_or_dict(cls, command_or_dict: T.Union[str, dict]) -> SOAPRequest:
        """
        Example:

            >>> command_or_dict = ".server info"
            # or
            >>> command_or_dict = {"command": ".server info"}
        """
        if isinstance(command_or_dict, str):
            return cls.from_command(command_or_dict)
        elif isinstance(command_or_dict, dict):
            return cls.from_dict(command_or_dict)
        else:  # pragma: no cover
            raise TypeError(
                f"command_or_dict must be str or dict, not {type(command_or_dict)}"
            )

    @classmethod
    def from_list(cls, lst: list) -> T.List[SOAPRequest]:
        """
        Example:

            >>> lst = [".server info"]
            # or
            >>> lst = [{"command": ".server info"}]
        """
        return [cls.from_command_or_dict(item) for item in lst]

    @classmethod
    def from_object(cls, obj: T.Union[str, dict, list]) -> T.List[SOAPRequest]:
        """
        Combination of :meth:`from_command`, :meth:`from_dict` and :meth:`from_list`.

        :return: list of ``SOAPRequest``.
        """
        if isinstance(obj, str):
            return [cls.from_command(obj)]
        elif isinstance(obj, dict):
            return [cls.from_dict(obj)]
        elif isinstance(obj, list):
            return cls.from_list(obj)
        else:  # pragma: no cover
            raise TypeError(f"obj must be str, dict or list, not {type(obj)}")

    @classmethod
    def from_string(
        cls,
        s: str,
        s3_client: T.Optional["S3Client"] = None,
        username: T.Optional[str] = None,
        password: T.Optional[str] = None,
        host: T.Optional[str] = None,
        port: T.Optional[int] = None,
    ) -> T.List[SOAPRequest]:
        """
        从字符串中加载 ``SOAPRequest``. 该方法总是返回一个列表. 这个方法常用于 CLI 场景下,
        从一个字符串中加载多个 GM 命令.

        :param s: 输入的字符串. 如果是以 s3:// 开头, 那么就去 S3 读数据, 此时需要给定
            ``s3_client`` 参数. 否则就视为单个 GM 命令.
        :param username: 默认的用户名, 只有当 request.username 为 None 的时候才会用到.
        :param password: 默认的密码, 只有当 request.password 为 None 的时候才会用到.
        :param host: 默认的 host, 只有当 request.host 为 None 的时候才会用到.
        :param port: 默认的 port, 只有当 request.port 为 None 的时候才会用到.
        :param s3_client: boto3.client("s3")
        """
        kwargs = dict(
            username=username,
            password=password,
            host=host,
            port=port,
        )
        kwargs = remove_none(kwargs)

        if s.startswith("s3://"):
            data = json.loads(get_object(s3_client=s3_client, s3uri=s))
            requests = cls.from_object(obj=data)
        else:
            requests = [cls.from_command(s)]

        for request in requests:
            for k, v in kwargs.items():
                setattr(request, k, v)

        return requests


class SoapResponseDumper:
    """
    Dump ``SOAPResponse`` to different destinations.
    """

    @classmethod
    def to_stdout(
        cls,
        responses: T.List[SOAPResponse],
    ):
        """
        Dump ``SOAPResponse`` to stdout.
        """
        print(json.dumps([res.to_dict() for res in responses]))

    @classmethod
    def to_s3(
        cls,
        responses: T.List[SOAPResponse],
        s3_client: "S3Client",
        s3uri: str,
    ):
        """
        Dump ``SOAPResponse`` to S3.
        """
        put_object(
            s3_client=s3_client,
            s3uri=s3uri,
            body=json.dumps([res.to_dict() for res in responses]),
        )
