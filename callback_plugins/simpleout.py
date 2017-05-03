"""
Render std err/out outside of the rest of the result which it prints with
indentation.
"""
from ansible.plugins.callback.default import CallbackModule as CallbackModule_default
from ansible import constants as C

class CallbackModule(CallbackModule_default):
    '''
    Override for the default callback module.

    Render std err/out outside of the rest of the result which it prints with
    indentation.
    '''
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'simpleout'

    def _dump_results(self, result):
        '''Return the text to output for a result.'''

        # Enable JSON identation
        result['_ansible_verbose_always'] = True

        save = {}
        for key in ['stdout', 'stdout_lines', 'stderr', 'stderr_lines', 'msg']:
            if key in result:
                save[key] = result.pop(key)

        output = CallbackModule_default._dump_results(self, result)

        output += "\n".join([save[key] for key in ['stdout', 'stderr', 'msg'] \
                                     if key in save and save[key]])

        for key, value in save.items():
            result[key] = value

        return output

    def v2_runner_retry(self, result):
        if result._result['stdout']:
            self._display.display(result._result['stdout'], color=C.COLOR_OK)

    def v2_runner_item_on_skipped(self, result):
        pass
