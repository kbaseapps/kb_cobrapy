import cobra
import optlang
import cobrakbase
# old method
from cobra.core import Model
from cobrakbase.core.model import KBaseFBAModel
from cobrakbase.core import KBaseGenome
from cobrakbase.core.converters import KBaseFBAModelToCobraBuilder

kbase = cobrakbase.KBaseAPI('UMPOM5SWM3S3KN3DUZ6UPKVEVZYOOILT')

model_object = kbase.get_object('MS1.mdl.gf', 'filipeliu:narrative_1612368108584')

super_long_id = 'SUPER_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOG'
print(len(super_long_id))

model_object['modelreactions'][0]['id'] = super_long_id

fbamodel = KBaseFBAModel(model_object)
builder = KBaseFBAModelToCobraBuilder(fbamodel)
if 'genome_ref' in model_object and False:
    #logging.info(f"Annotating model with genome information: {model_object['genome_ref']}")
    genome_object = kbase.get_object('80971/3/1', None)
    #adding Genome to the Builder
    builder.with_genome(KBaseGenome(genome_object))

model = builder.build()

cobra.io.write_sbml_model(model, 'sbml.txt')
