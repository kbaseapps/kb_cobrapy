/*
A KBase module: kb_cobrapy
*/

module kb_cobrapy {
  /* A boolean - 0 for false, 1 for true.
    @range (0, 1)
  */
  typedef int boolean;

  /* An X/Y/Z style reference
    @id ws
  */
  typedef string obj_ref;

  typedef structure {
      obj_ref input_ref;
      string destination_dir;
   } ModelToSBMLFileParams;

  typedef structure {
      string file_path;
  } ModelToSBMLFileOutput;

  funcdef model_to_sbml_file(ModelToSBMLFileParams params)
      returns (ModelToSBMLFileOutput result) authentication required;

  typedef structure {
      obj_ref obj_ref;
  } ExportParams;

  typedef structure {
      string shock_id;
  } ExportOutput;

  funcdef export_model_as_sbml (ExportParams params) returns (ExportOutput result) authentication required;

};
