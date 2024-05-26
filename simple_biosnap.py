import pandas as pd

class Embeds:

    def __init__(self, embeds_path='data/raw_embed_df.csv'):
        
        self.raw_path = embeds_path
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
        self.pca_df = pd.concat(
            [self.index['Drug'], pca_df], 
            axis=1
        )


    def _format_drugnames(self):
        raw_strs = [d.split('CID')[1] for d in self.index['Drug'].values]
        IDs = [int(st) for st in raw_strs]
        self.index['Drug'] = [f'CID{id}' for id in IDs]