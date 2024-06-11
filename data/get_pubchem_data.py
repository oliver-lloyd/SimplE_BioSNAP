import pandas as pd
import pubchempy as pcp
from pathlib import Path
from time import sleep

out_path = Path('pubchem_info.csv')

if not out_path.exists():
    out_df = pd.DataFrame()

    # Load drugs
    drug_df = pd.read_csv('raw_embed_df.csv')[['Drug']]
    pubchem_ids = [drug[3:] for drug in drug_df.Drug.values]

    # Create compound objects
    print('Contacting PubChem API, this might take a moment..')
    compounds = []
    for pcp_id in pubchem_ids:
        compounds.append(pcp.Compound.from_cid(pcp_id))
        sleep(0.1)
    drug_df['formula'] = [comp.molecular_formula for comp in compounds]
    drug_df['molecular_weight'] = [comp.molecular_weight for comp in compounds]
    print('Finished. Saving..')

    # Add PubChem URLs
    url_prefix = 'https://pubchem.ncbi.nlm.nih.gov/compound/'
    urls = [url_prefix + drug[3:] for drug in drug_df.Drug.values]
    drug_df['URL'] = urls

    # Save
    drug_df.to_csv(out_path.name, index=False)
