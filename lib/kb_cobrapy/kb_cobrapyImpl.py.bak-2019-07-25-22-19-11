# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os

from kb_cobrapy.Utils import Utils
#END_HEADER


class kb_cobrapy:
    '''
    Module Name:
    kb_cobrapy

    Module Description:
    A KBase module: kb_cobrapy
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/kbaseapps/kb_cobrapy.git"
    GIT_COMMIT_HASH = "064ad3d44ccce212e6e59d0d549991da48a3094c"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config
        self.config['SDK_CALLBACK_URL'] = os.environ['SDK_CALLBACK_URL']
        self.config['KB_AUTH_TOKEN'] = os.environ['KB_AUTH_TOKEN']
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        self.scratch = config['scratch']
        self.utils = Utils(self.config)
        #END_CONSTRUCTOR
        pass


    def model_to_sbml_file(self, ctx, params):
        """
        :param params: instance of type "ModelToSBMLFileParams" -> structure:
           parameter "input_ref" of type "obj_ref" (An X/Y/Z style reference
           @id ws), parameter "destination_dir" of String
        :returns: instance of type "ModelToSBMLFileOutput" -> structure:
           parameter "file_path" of String
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN model_to_sbml_file
        logging.info("Starting 'model_to_sbml_file' with params:{}".format(params))
        self.utils.validate_params(params, ("destination_dir", "input_ref"))
        params['destination_dir'] = self.scratch
        am_id, result = self.utils.to_sbml(params)
        #END model_to_sbml_file

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method model_to_sbml_file return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]

    def export_model_as_sbml(self, ctx, params):
        """
        :param params: instance of type "ExportParams" -> structure:
           parameter "obj_ref" of type "obj_ref" (An X/Y/Z style reference
           @id ws)
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN export_model_as_sbml
        logging.info("Starting 'export_model_as_sbml' with params:{}".format(params))
        self.utils.validate_params(params, ("input_ref",))
        params['destination_dir'] = self.scratch
        am_id, files = self.utils.to_sbml(params)
        result = self.utils.export(files['file_path'], am_id, params['input_ref'])
        #END export_model_as_sbml

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method export_model_as_sbml return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
