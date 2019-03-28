# -*- coding: utf-8 -*-
import json
import os
import time
import unittest
from configparser import ConfigParser

from kb_cobrapy.kb_cobrapyImpl import kb_cobrapy
from kb_cobrapy.kb_cobrapyServer import MethodContext
from kb_cobrapy.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace


class kb_cobrapyTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_cobrapy'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'kb_cobrapy',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = kb_cobrapy(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_ContigFilter_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa
        cls.fba_model = json.load(open('test_fba_model.json'))
        info = cls.wsClient.save_objects({
            "workspace": cls.wsName,
            "objects": [{
                "type": "KBaseFBA.FBAModel",
                "data": cls.fba_model,
                "name": "test_fba_model"
            }]
        })[0]
        cls.fba_model_ref = f"{info[6]}/{info[0]}/{info[4]}"

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def test_make_sbml(self):
        ret = self.serviceImpl.model_to_sbml_file(self.ctx, {'input_ref': self.fba_model_ref,
                                                             'destination_dir': self.scratch})

    def test_export_sbml(self):
        ret = self.serviceImpl.export_model_as_sbml(self.ctx, {'input_ref': self.fba_model_ref})

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            ret = self.serviceImpl.model_to_sbml_file(self.ctx, {'input_ref': self.fba_model_ref})

        with self.assertRaises(ValueError):
            ret = self.serviceImpl.model_to_sbml_file(self.ctx, {'destination_dir': self.scratch})

        with self.assertRaises(ValueError):
            ret = self.serviceImpl.export_model_as_sbml(self.ctx, {})
