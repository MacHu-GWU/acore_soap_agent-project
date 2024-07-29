# -*- coding: utf-8 -*-

import boto3
import json
import moto
from acore_soap.api import SOAPResponse
from acore_soap_agent.utils import put_object
from acore_soap_agent.request import SoapRequestLoader, SoapResponseDumper


@moto.mock_aws
def test():
    s3_client = boto3.client("s3")
    bucket = "mybucket-request"
    s3_client.create_bucket(Bucket=bucket)
    put_object(
        s3_client,
        f"s3://{bucket}/single_input.json",
        body=json.dumps({"command": ".server info"}),
    )
    put_object(
        s3_client,
        f"s3://{bucket}/multi_input.json",
        body=json.dumps([{"command": ".server info"}]),
    )

    requests = SoapRequestLoader.from_object(".server info")
    requests = SoapRequestLoader.from_object({"command": ".server info"})
    requests = SoapRequestLoader.from_object([".server info"])
    requests = SoapRequestLoader.from_object([{"command": ".server info"}])
    requests = SoapRequestLoader.from_string(".server info")
    requests = SoapRequestLoader.from_string(
        f"s3://{bucket}/single_input.json",
        password="admin",
        s3_client=s3_client,
    )
    requests = SoapRequestLoader.from_string(
        f"s3://{bucket}/multi_input.json",
        password="admin",
        s3_client=s3_client,
    )

    responses = [
        SOAPResponse(body="this is body", message="this is message", succeeded=True)
    ]

    SoapResponseDumper.to_stdout(responses)
    SoapResponseDumper.to_s3(
        responses,
        s3_client=s3_client,
        s3uri=f"s3://{bucket}/output.json",
    )


if __name__ == "__main__":
    from acore_soap_agent.tests import run_cov_test

    run_cov_test(__file__, "acore_soap_agent.request", preview=False)
