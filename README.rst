
.. image:: https://readthedocs.org/projects/acore-soap-agent/badge/?version=latest
    :target: https://acore-soap-agent.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/acore_soap_agent-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/acore_soap_agent-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/acore_soap_agent-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/acore_soap_agent-project

.. image:: https://img.shields.io/pypi/v/acore-soap-agent.svg
    :target: https://pypi.python.org/pypi/acore-soap-agent

.. image:: https://img.shields.io/pypi/l/acore-soap-agent.svg
    :target: https://pypi.python.org/pypi/acore-soap-agent

.. image:: https://img.shields.io/pypi/pyversions/acore-soap-agent.svg
    :target: https://pypi.python.org/pypi/acore-soap-agent

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/acore_soap_agent-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/acore_soap_agent-project

------

.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://acore-soap-agent.readthedocs.io/en/latest/

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://acore-soap-agent.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/acore_soap_agent-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/acore_soap_agent-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/acore_soap_agent-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/acore-soap-agent#files


Welcome to ``acore_soap_agent`` Documentation
==============================================================================
.. image:: https://acore-soap-agent.readthedocs.io/en/latest/_static/acore_soap_agent-logo.png
    :target: https://acore-soap-agent.readthedocs.io/en/latest/

首先请阅读 `acore_soap-project <https://github.com/MacHu-GWU/acore_soap-project>`_ 的 README 的第一段来了解 acore soap 系列项目的背景.

该项目提供了一个部署在游戏服务器 EC2 上的命令行程序, 作为外部 API 调用的桥梁. 使得外部有权限的开发者可以通过 AWS SSM Run Command 远程调用这个命令行程序, 从而实现远程执行 GM 命令.


How to
------------------------------------------------------------------------------
1. 如果你想要在 EC2 上调试这个 Agent, 你可以参考 `tests_int/README.rst <https://github.com/MacHu-GWU/acore_soap_agent-project/blob/main/tests_int/README.rst>`_ 中的教程.

2. 如果你在 EC2 上安装完 Agent 之后, 想要验证它是否能正常工作, 你可以用下面的命令测试. 如果看到一些例如 ``Server uptime: ...`` 的信息就表示成功了.

.. code-block:: bash

    /home/ubuntu/git_repos/acore_soap_agent-project/.venv/bin/acoresoapagent gm ".server info"

3. 如果你想要利用这个 Agent 来远程执行 GM 命令, 请使用 `acore_soap_remote-project <https://github.com/MacHu-GWU/acore_soap_remote-project>`_ 这个工具.


.. _install:

Install
------------------------------------------------------------------------------

``acore_soap_agent`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install acore-soap-agent

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade acore-soap-agent
