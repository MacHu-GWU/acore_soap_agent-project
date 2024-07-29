How to run integration test in AWS EC2 where you run the worldserver:

SSH to the EC2 instance::

    sshec2 ssh

Delete existing code::

    rm -rf /home/ubuntu/git_repos/acore_soap_agent-project

Git clone latest repo::

    git clone https://github.com/MacHu-GWU/acore_soap_agent-project /home/ubuntu/git_repos/acore_soap_agent-project

Git pull latest changes::

    cd /home/ubuntu/git_repos/acore_soap_agent-project && git pull

CD to the repo dir::

    cd /home/ubuntu/git_repos/acore_soap_agent-project

Create virtualenv::

    virtualenv /home/ubuntu/git_repos/acore_soap_agent-project/.venv

Activate virutalenv::

    source /home/ubuntu/git_repos/acore_soap_agent-project/.venv/bin/activate

Pip install core dependencies::

    /home/ubuntu/git_repos/acore_soap_agent-project/.venv/bin/pip install -e /home/ubuntu/git_repos/acore_soap_agent-project

Pip install test dependencies::

    /home/ubuntu/git_repos/acore_soap_agent-project/.venv/bin/pip install -r /home/ubuntu/git_repos/acore_soap_agent-project/requirements-test.txt

Run integration test::

    /home/ubuntu/git_repos/acore_soap_agent-project/.venv/bin/acoresoapagent gm --cmd ".server info"
