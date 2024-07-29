# -*- coding: utf-8 -*-

"""
SOAP Agent command line user interface.

See :class:`Command` for details.
"""

import typing as T
import fire

from .._version import __version__

from .impl import (
    gm,
)


class Command:
    """
    Acore Soap Agent command line interface. All these commands can only be
    used on EC2.
    """

    def hello(self):
        """
        Print welcome message.
        """
        print(f"Hello acore_soap_agent {__version__} user!")

    def version(self):
        """
        Print version number.
        """
        print(__version__)

    def gm(
        self,
        cmd: str,
        user: T.Optional[str] = None,
        pwd: T.Optional[str] = None,
        host: T.Optional[str] = None,
        port: T.Optional[int] = None,
        raises: bool = True,
        s3uri: T.Optional[str] = None,
    ):
        """
        Run single GM command. See :func:`acore_soap_app.cli.impl.gm` for implementation
        details.

        Example::

            acoresoapagent gm --help

            acoresoapagent gm ".server info"

            acoresoapagent gm ".server info" --user myuser --pwd mypwd

            acoresoapagent gm ".server info" --s3uri s3://bucket/output.json

        :param cmd: the GM command to run
        :param user: in game GM account username, if not given, then use "admin"
        :param pwd: in game GM account password, if not given, then use "admin"
        :param host: wow world server host, default "localhost"
        :param port: wow world server SOAP port, default 7878
        :param raises: raise error if any of the GM command failed.
        :param s3uri: if None, then return the response as JSON, otherwise, save
            the response to S3.
        """
        gm(
            input_string=cmd,
            username=user,
            password=pwd,
            host=host,
            port=port,
            raises=raises,
            s3_client=None,
            output_s3uri=s3uri,
        )


def run():
    fire.Fire(Command)
