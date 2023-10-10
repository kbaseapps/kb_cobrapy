import cobra
import optlang
import cobrakbase
# old method
from cobra.core import Reaction
from cobrakbase.core.model import KBaseFBAModel
from cobrakbase.core import KBaseGenome
from cobrakbase.core.converters import KBaseFBAModelToCobraBuilder

print(optlang.available_solvers)
config = cobra.Configuration()
print(f'selected solver: {config.solver}')

kbase = cobrakbase.KBaseAPI()

model = kbase.get_from_ws('MS1.mdl.gf', 'filipeliu:narrative_1612368108584')

super_long_id = "DEBUG_L" + 500 * "O" + "ONG_ID"
print(len(super_long_id))

long_name_reaction = Reaction(super_long_id, super_long_id, 'debug', 0, 0)
long_name_reaction.add_metabolites({
    model.metabolites.cpd00001_e0: -1,
    model.metabolites.cpd00001_c0: 1,
})

model.add_reactions([long_name_reaction])

cobra.io.write_sbml_model(model, 'sbml.xml')
