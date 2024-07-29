How it Works
==============================================================================


Overview
------------------------------------------------------------------------------
本项目本身是一个可安装的 Python 库, 同时也是一个需要再 EC2 游戏服务器上安装的 CLI 程序. 它对 SOAP 的 HTTP Request 和 XML input / output 进行了封装, 提供了一套 CLI 接口用于在服务器上执行 GM 命令. 它是所有需要远程执行 GM 命令的外部程序的代理. 有了它, 我们就可以通过 `AWS SSM Run Command <https://docs.aws.amazon.com/systems-manager/latest/userguide/run-command.html>`_ 这个服务安全地在 EC2 执行任何远程命令.

.. important::

    强调一下, Agent 必须要在 EC2 游戏服务器上安装. Agent 的 CLI 只能在 EC2 上使用. Agent 在本地电脑上是无法运行的, 因为 SOAP server 是运行在 EC2 上的, 且 SOAP server 不对 public network 开放.

    如果我们要远程使用 Agent 的功能, 请使用 `acore_soap_remote <https://github.com/MacHu-GWU/acore_soap_remote-project>`_ 项目.


Use CLI Command
------------------------------------------------------------------------------
用户可以在游戏服务器的 EC2 上使用 ``acoresoapagent gm "{gm command}"`` 这样的 CLI 命令来执行 GM 命令. Agent 的 CLI 命令是 ``acoresoapagent``, 这个命令是在 ``setup.py`` 文件中注册的.

.. dropdown:: setup.py

    .. code-block:: python

        setup(
            ...,
            entry_points={
                "console_scripts": [
                    "acoresoapagent=acore_soap_agent.cli.main:run",
                ],
            },
        )

Agent 的核心命令是 ``acoresoapagent gm "{gm_command_here}"``, 该命令由 :meth:`acore_soap_agent.cli.main.Command.gm` 方法实现. 它有以下几大功能:

1. 总是将输入视为一个 gm command 的列表.
2. 以字符串的形式 ``--cmd {gm_command_here}`` 传递参数.
3. 从 S3 中批量读取 gm 命令, ``--cmd s3://bucket/key_to_your_gm_command_list.json``
4. 如果没有指定 ``--s3uri ...``, 则将 `SoapResponse <https://acore-soap.readthedocs.io/en/latest/acore_soap/request.html#acore_soap.request.SOAPResponse>`_ 打印到 stdout, 以便被人类所阅读, 或被 AWS SSM API 中的 ``StandardOutputContent`` 所捕获. 该命令总是打印一个列表.
5. 如果指定了 ``--s3uri ...``, 则将 ``SoapResponse`` 序列化为 JSON 并保存到 S3 上. 以便其他程序读取.

下面给出了一个实际的例子 (请确保你是在 EC2 游戏服务器上运行的)::

    $ /home/ubuntu/git_repos/acore_soap_agent-project/.venv/bin/acoresoapagent gm ".server info"
    [{"body": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<SOAP-ENV:Envelope xmlns:SOAP-ENV=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:SOAP-ENC=\"http://schemas.xmlsoap.org/soap/encoding/\" xmlns:xsi=\"http://www.w3.org/1999/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/1999/XMLSchema\" xmlns:ns1=\"urn:AC\"><SOAP-ENV:Body><ns1:executeCommandResponse><result>AzerothCore rev. 278ee2a72836 2024-06-13 21:52:22 +0200 (master branch) (Unix, RelWithDebInfo, Static)&#xD;\nConnected players: 0. Characters in world: 0.&#xD;\nConnection peak: 1.&#xD;\nServer uptime: 2 day(s) 2 hour(s) 9 minute(s) 57 second(s)&#xD;\nUpdate time diff: 1ms. Last 500 diffs summary:&#xD;\n- Mean: 1ms&#xD;\n- Median: 1ms&#xD;\n- Percentiles (95, 99, max): 2ms, 10ms, 12ms&#xD;\n</result></ns1:executeCommandResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>", "message": "AzerothCore rev. 278ee2a72836 2024-06-13 21:52:22 +0200 (master branch) (Unix, RelWithDebInfo, Static)\r\nConnected players: 0. Characters in world: 0.\r\nConnection peak: 1.\r\nServer uptime: 2 day(s) 2 hour(s) 9 minute(s) 57 second(s)\r\nUpdate time diff: 1ms. Last 500 diffs summary:\r\n- Mean: 1ms\r\n- Median: 1ms\r\n- Percentiles (95, 99, max): 2ms, 10ms, 12ms", "succeeded": true}]


在我们这个项目中, 我们的 ``acoresoapagent`` CLI 可执行文件会被放在 ubuntu 服务器上的 ``/home/ubuntu/git_repos/acore_soap_agent-project/.venv/bin/acoresoapagent`` 这个位置.

下面列出了部分常用 Agent 的 CLI 命令的功能和语法. 至于详细的命令和参数列表, 请参考 :mod:`~acore_soap_agent.cli.main` 模块的文档.

查看服务器状态. 在 EC2 上安装了这个库之后, 你可以用这个命令来测试:

.. code-block:: bash

    /home/ubuntu/git_repos/acore_soap_agent-project/.venv/bin/acoresoapagent gm ".server info"

创建新账号:

.. code-block:: bash

    /home/ubuntu/git_repos/acore_soap_agent-project/.venv/bin/acoresoapagent gm ".account create myusername mypassword"


Use It As a Python Library
------------------------------------------------------------------------------
Agent 的底层是两个对象 :class:`~acore_soap_agent.request.SoapRequestLoader` 和 :class:`~acore_soap_agent.request.SoapResponseDumper`. 前者负责从一个表示具体命令的字符串或是一个表示 S3 uri 的字符串批量构造 SOAP 请求. 后者负责解析将 SOAP 响应写入到 stdout 或是 S3 中. 这两个对象可以单独被当做一个库类来使用.

类似地, :func:`~acore_soap_agent.cli.impl.gm` 函数是 ``acoresoapagent gm`` CLI 命令的底层实现, 你也可以单独把它当做一个函数来使用.


How to Debug
------------------------------------------------------------------------------
1. 如果你想要在 EC2 上调试这个 Agent, 你可以参考 `tests_int/README.rst <https://github.com/MacHu-GWU/acore_soap_agent-project/blob/main/tests_int/README.rst>`_ 中的教程.

2. 如果你在 EC2 上安装完 Agent 之后, 想要验证它是否能正常工作, 你可以用下面的命令测试. 如果看到一些例如 ``Server uptime: ...`` 的信息就表示成功了.

.. code-block:: bash

    /home/ubuntu/git_repos/acore_soap_agent-project/.venv/bin/acoresoapagent gm ".server info"
