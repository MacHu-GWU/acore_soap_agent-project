# -*- coding: utf-8 -*-

from acore_soap_agent import api


def test():
    _ = api
    _ = api.SoapRequestLoader
    _ = api.SoapResponseDumper


if __name__ == "__main__":
    from acore_soap_agent.tests import run_cov_test

    run_cov_test(__file__, "acore_soap_agent.api", preview=False)
