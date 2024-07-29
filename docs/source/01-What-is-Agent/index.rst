What is Agent
==============================================================================


Overview
------------------------------------------------------------------------------
本项目本身是一个可安装的 Python 库, 同时也是一个需要再 EC2 游戏服务器上安装的 CLI 程序. 它对 SOAP 的 HTTP Request 和 XML input / output 进行了封装, 提供了一套 CLI 接口用于在服务器上执行 GM 命令. 它是所有需要远程执行 GM 命令的外部程序的代理. 有了它, 我们就可以通过 `AWS SSM Run Command <https://docs.aws.amazon.com/systems-manager/latest/userguide/run-command.html>`_ 这个服务安全地在 EC2 执行任何远程命令. 强调一下, Agent 必须要在 EC2 游戏服务器上安装.


Agent
------------------------------------------------------------------------------
.. important::

    Agent 只能在 EC2 上使用. Agent 在本地电脑上是无法运行的, 因为 SOAP server 是运行在 EC2 上的, 且 SOAP server 不对 public network 开放.

    如果我们要远程使用 Agent 的功能, 请使用 `acore_soap_remote <https://github.com/MacHu-GWU/acore_soap_remote-project>`_ 项目.

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

Agent 的核心命令是 ``acoresoapagent gm "{gm command}"``, 该命令由 :meth:`acore_soap_agent.cli.main.Command.gm` 方法实现. 它不仅能运行 GM 命令, 还能将返回的信息写入到 AWS S3 上以方便读取.

Agent 的底层是两个对象 :class:`~acore_soap_agent.request.SoapRequestLoader` 和 :class:`~acore_soap_agent.request.SoapResponseDumper`. 前者负责从一个表示具体命令的字符串或是一个表示 S3 uri 的字符串批量构造 SOAP 请求. 后者负责解析将 SOAP 响应写入到 stdout 或是 S3 中.

在我们这个项目中, 我们的 ``acoresoapagent`` CLI 可执行文件会被放在 ubuntu 服务器上的 ``/home/ubuntu/git_repos/acore_soap_agent-project/.venv/bin/acoresoapagent`` 这个位置.

下面列出了部分常用 Agent 的 CLI 命令的功能和语法. 至于详细的命令和参数列表, 请参考 :mod:`~acore_soap_agent.cli.main` 模块的文档.

查看服务器状态. 在 EC2 上安装了这个库之后, 你可以用这个命令来测试:

.. code-block:: bash

    /home/ubuntu/git_repos/acore_soap_agent-project/.venv/bin/acoresoapagent gm ".server info"

创建新账号:

.. code-block:: bash

    /home/ubuntu/git_repos/acore_soap_agent-project/.venv/bin/acoresoapagent gm ".account create myusername mypassword"
