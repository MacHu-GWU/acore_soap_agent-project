# -*- coding: utf-8 -*-

"""
Command line low lever implementations.
"""

import typing as T

from simple_aws_ec2.api import EC2MetadataCache
from acore_soap.api import ensure_response_succeeded

from ..request import SoapRequestLoader, SoapResponseDumper

if T.TYPE_CHECKING:  # pragma: no cover
    from mypy_boto3_s3.client import S3Client


def gm(
    input_string: str,
    username: T.Optional[str] = None,
    password: T.Optional[str] = None,
    host: T.Optional[str] = None,
    port: T.Optional[int] = None,
    raises: bool = True,
    s3_client: T.Optional["S3Client"] = None,
    output_s3uri: T.Optional[str] = None,
):
    """
    运行一个或多个 GM 命令. 例如 ``.server info``.

    :param input_string: 输入的字符串. 如果是以 s3:// 开头, 那么就去 S3 读数据,
        此时需要给定 ``s3_client`` 参数. 否则就视为单个 GM 命令.
    :param username: 默认的用户名, 只有当 request.username 为 None 的时候才会用到.
    :param password: 默认的密码, 只有当 request.password 为 None 的时候才会用到.
    :param host: 默认的 host, 只有当 request.host 为 None 的时候才会用到.
    :param port: 默认的 port, 只有当 request.port 为 None 的时候才会用到.
    :param raises: 默认为 True. 如果为 True, 则在遇到错误时抛出异常. 反之则将
        failed SOAP Response 原封不动地返回.
    :param s3_client: 可选参数, 用于将结果保存到 S3 中.
    :param output_s3uri: 可选参数, 如果为 None, 则将结果打印到 stdout 中. 如果给定,
        则将结果保存到 S3 中. 常用于返回结果特别大的情况.
    """
    if input_string.startswith("s3://"):  # pragma: no cover
        if s3_client is None:
            boto_ses = EC2MetadataCache.load().get_boto_ses_from_ec2_inside()
            s3_client = boto_ses.client("s3")

    requests = SoapRequestLoader.from_string(
        s=input_string,
        username=username,
        password=password,
        host=host,
        port=port,
        s3_client=s3_client,
    )

    responses = list()
    for request in requests:
        response = request.send()
        ensure_response_succeeded(request, response, raises=raises)
        responses.append(response)

    if output_s3uri is None:
        SoapResponseDumper.to_stdout(responses=responses)
    else:
        if s3_client is None:  # pragma: no cover
            boto_ses = EC2MetadataCache.load().get_boto_ses_from_ec2_inside()
            s3_client = boto_ses.client("s3")

        SoapResponseDumper.to_s3(
            responses=responses,
            s3_client=s3_client,
            s3uri=output_s3uri,
        )
