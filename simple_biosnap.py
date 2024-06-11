import pandas as pd

class Embeds:

    def __init__(self, embeds_path='data/raw_embed_df.csv', drug_info_path='data/pubchem_info.csv'):
        
        self.raw_path = embeds_path
        self.drug_info = pd.read_csv(drug_info_path)
        self.load_raw()


    def load_raw(self):
        self.raw_df = pd.read_csv(self.raw_path)
        self.index = self.raw_df[['selfloops_index','Drug']]
        self._format_drugnames()

        self.full_dim = int(self.raw_df.columns[-1])
        self.emb_colnames = [str(i) for i in range(self.full_dim)]
        self.emb_ = self.raw_df[self.emb_colnames].to_numpy()
        

    def pca(self, n_dim=3):
        from sklearn.decomposition import PCA

        self.pca_dim = n_dim
        self.pca_obj = PCA(n_dim).fit(self.emb_.T)
        self.pca_emb_ = self.pca_obj.components_.T
        cols = [f'Component {n+1}' for n in range(n_dim)]
        pca_df = pd.DataFrame(self.pca_emb_, columns=cols)
        pca_df = pd.concat(
            [self.index['Drug'], pca_df], 
            axis=1
        )
        self.pca_df = pca_df.merge(self.drug_info, on='Drug')


    def _format_drugnames(self):
        raw_strs = [d.split('CID')[1] for d in self.index['Drug'].values]
        IDs = [int(st) for st in raw_strs]
        formatted = [f'CID{id}' for id in IDs]
        self.index['Drug'] = formatted
        self.drug_info['Drug'] = formatted


    def SimplE_scorer(self, ent1, rel, ent2):
        from numpy import dot, multiply
        id1 = self.index.query('Drug == @ent1').index[0]
        id2 = self.index.query('Drug == @ent2').index[0]
        #rel_id = self.rel_emb_.query('SE == @rel').index[0]

        vec1 = self.emb_[id1]
        vec2 = self.emb_[id2]
        #rel_vec = self.rel_emb_[rel_id]

        #return np.dot(np.multiply(vec1, rel_vec), vec2)
        return dot(multiply(vec1, vec2), vec2)  # Delete line when have proper rel embeds
    