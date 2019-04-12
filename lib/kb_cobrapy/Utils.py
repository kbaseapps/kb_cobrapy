import logging
import os
import uuid
import shutil

import cobra
import cobrakbase

from installed_clients.DataFileUtilClient import DataFileUtil


class Utils:
    def __init__(self, config):
        self.ws_url = config["workspace-url"]
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.shock_url = config['shock-url']
        self.srv_wiz_url = config['srv-wiz-url']
        self.scratch = config['scratch']
        self.dfu = DataFileUtil(self.callback_url)

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
                logging.warning("Unexpected parameter {} supplied".format(param))

    def _ws_obj_to_cobra(self, ref):
        ret = self.dfu.get_objects({'object_refs': [ref]})['data'][0]
        name = ret['info'][1]
        model = cobrakbase.convert_kmodel(ret['data'])

        if 'genome_ref' in ret['data']:
            logging.info(f"Annotating model with genome information: {ret['data']['genome_ref']}")
            genome = self.dfu.get_objects(
                {'object_refs': [ret['data']['genome_ref']]})['data'][0]['data']
            cobrakbase.annotate_model_with_genome(model, genome)

        modelseed = cobrakbase.modelseed.from_local('/kb/module/data/ModelSEEDDatabase-dev')
        print(cobrakbase.annotate_model_with_modelseed(model, modelseed))

        return name, model

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
