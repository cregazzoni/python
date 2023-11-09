# import sys
import os

def runCommand(command, path):

    RSP_STDOUT = "stdout"
    RSP_STDERR = "stderr"
    RSP_RETCODE = "ret_code"
    RSP_EXCEPTION = "exception"
    execResponse = {}

    try:
        execResponse[RSP_STDOUT] = \
            subprocess.check_output(
                command,
                encoding="utf-8",
                stderr=subprocess.STDOUT,
                cwd=path,
                shell=True)
        execResponse[RSP_RETCODE] = 0
    except subprocess.CalledProcessError as e:
        execResponse[RSP_RETCODE] = e.returncode
        # Note that because stderr has been redirected to stdout, all output is contained in stdout
        execResponse[RSP_STDOUT] = e.stdout
    except Exception as e:
        execResponse[RSP_EXCEPTION] = e.strerror
    finally:
        outcome = True
        if execResponse[RSP_RETCODE] == 0:
            pass
        else:
            outcome = False
        if RSP_EXCEPTION in execResponse:
            return execResponse[RSP_EXCEPTION], False
        return execResponse[RSP_STDOUT], outcome


# This function simply use runCommand
def execute_commands(commands, stdout):

    for command in commands:
        result, outcome = runCommand(command, path=".")
        # if command succeded (outcome = True)
        if outcome:
            if stdout:
                logger.success(f"# command: {command} | succeed: [{outcome}] | result: {result}")
            else:
                logger.debug(f"# command: {command} | succeed: [{outcome}] | result: {result}")
        # if command failed (outcome = False)
        else:
            logger.error(f"# command: {command} | succeed: [{outcome}] | result: {result}")
        if not outcome:
            sys.exit()


# This will use only runCommand function (if I need to run just one single commmand)
command = f"export KUBECONFIG=../kube/kubeconfig; oc get pods > /dev/null 2>&1; oc get deployments -n my_namespace"
deploymentList, outcome = runCommand(command, path=".")

# If I need to execute two or more commands, I can use execute_commands - must declare an array first
commands = [None] * 2
commands[0] = "ansible-playbook python.yml -i inventory"
commands[1] = "ansible-playbook terraform.yml -i inventory"
execute_commands(commands, True)
