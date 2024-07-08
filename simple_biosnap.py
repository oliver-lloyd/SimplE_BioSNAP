import pandas as pd

class Embeds:

    def __init__(self, embeds_path='data/ent_embeds.csv', drug_info_path='data/pubchem_info.csv', rel_embeds_path='data/rel_embeds.csv'):
        
        self.ent_embed_path = embeds_path
        self.rel_embed_path = rel_embeds_path
        
        self.drug_info = pd.read_csv(drug_info_path)
        self.load_raw()


    def load_raw(self):
        ent_raw_df = pd.read_csv(self.ent_embed_path)
        self.ent_index = ent_raw_df[['selfloops_index','Pubchem_ID', 'Drug']]
        self._format_drug_IDs()

        rel_raw_df = pd.read_csv(self.rel_embed_path)
        self.rel_index = rel_raw_df[['relation', 'description']]

        self.full_dim = int(ent_raw_df.columns[-1])
        self.emb_colnames = [str(i) for i in range(self.full_dim)]

        self.ent_emb_ = ent_raw_df[self.emb_colnames].to_numpy()
        self.rel_emb_ = rel_raw_df[self.emb_colnames].to_numpy()
        

    def pca(self, n_dim=3):
        from sklearn.decomposition import PCA

        self.pca_dim = n_dim
        self.pca_obj = PCA(n_dim).fit(self.ent_emb_.T)
        self.pca_emb_ = self.pca_obj.components_.T
        cols = [f'Component {n+1}' for n in range(n_dim)]
        pca_df = pd.DataFrame(self.pca_emb_, columns=cols)
        pca_df = pd.concat(
            [self.ent_index['Drug'], pca_df], 
            axis=1
        )
        self.pca_df = pca_df.merge(self.drug_info, on='Drug')


    def _format_drug_IDs(self):
        raw_strs = [d.split('CID')[1] for d in self.ent_index['Pubchem_ID'].values]
        IDs = [int(st) for st in raw_strs]
        formatted_drugs = [f'CID{id}' for id in IDs]
        self.ent_index['Pubchem_ID'] = formatted_drugs
        self.drug_info['Pubchem_ID'] = formatted_drugs


    def SimplE_scorer(self, ent1, rel, ent2):
        from numpy import dot, multiply

        id1 = self.ent_index.query('Drug == @ent1').index[0]
        id2 = self.ent_index.query('Drug == @ent2').index[0]
        rel_id = self.rel_index.query('description == @rel').index[0]

        vec1 = self.ent_emb_[id1]
        vec2 = self.ent_emb_[id2]
        rel_vec = self.rel_emb_[rel_id]

        return dot(multiply(vec1, rel_vec), vec2)
    