import logging
import os
import uuid
import shutil

import cobra
import modelseedpy
import cobrakbase
from cobrakbase.core.model import KBaseFBAModel
from cobrakbase.core import KBaseGenome
from cobrakbase.core.converters import KBaseFBAModelToCobraBuilder

from installed_clients.DataFileUtilClient import DataFileUtil

logger = logging.getLogger(__name__)


class Utils:
    def __init__(self, config):
        self.ws_url = config["workspace-url"]
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.shock_url = config['shock-url']
        self.srv_wiz_url = config['srv-wiz-url']
        self.scratch = config['scratch']
        self.dfu = DataFileUtil(self.callback_url)
        self.api = cobrakbase.KBaseAPI(config['KB_AUTH_TOKEN'], config)

    @staticmethod
    def validate_params(params, expected, opt_param=set()):
        """Validates that required parameters are present. Warns if unexpected parameters appear"""
        expected = set(expected)
        opt_param = set(opt_param)
        pkeys = set(params)
        if expected - pkeys:
            raise ValueError("Required keys {} not in supplied parameters"
                             .format(", ".join(expected - pkeys)))
        defined_param = expected | opt_param
        for param in params:
            if param not in defined_param:
                logger.warning("Unexpected parameter {} supplied".format(param))

    def _ws_obj_to_cobra(self, ref):
        logger.info(f'fetch model from ws: {ref}')
        model = self.api.get_from_ws(ref)

        modelseed = modelseedpy.biochem.from_local('/kb/module/data/')

        print(cobrakbase.annotate_model_with_modelseed(model, modelseed))

        return model.info.id, model

    def to_sbml(self, params):
        """Convert a FBAModel to a SBML file"""
        files = {}
        _id, cobra_model = self._ws_obj_to_cobra(params['input_ref'])
        files['file_path'] = os.path.join(params['destination_dir'], _id + ".xml")
        cobra.io.write_sbml_model(cobra_model, files['file_path'])

        return _id, files

    def export(self, file, name, input_ref):
        """Saves a set of files to SHOCK for export"""
        export_package_dir = os.path.join(self.scratch, name + str(uuid.uuid4()))
        os.makedirs(export_package_dir)
        shutil.move(file, os.path.join(export_package_dir, os.path.basename(file)))

        # package it up and be done
        package_details = self.dfu.package_for_download({
            'file_path': export_package_dir,
            'ws_refs': [input_ref]
        })

        return {'shock_id': package_details['shock_id']}
