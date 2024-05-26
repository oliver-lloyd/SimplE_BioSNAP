from simple_biosnap import Embeds
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt

# Header
st.title('SimplE embeddings of BioSNAP drugs')
st.link_button(
    'Full 256-dimension data avilable here',
    url='https://github.com/oliver-lloyd/SimplE_BioSNAP/blob/master/data/raw_embed_df.csv'
)

# User input
n = st.slider(
    'Desired number of dimensions in projection', 
    min_value=1,
    max_value=8
)

# Load and prep embedding data
emb = Embeds()
emb.pca(n)
st.dataframe(
    emb.pca_df, 
    hide_index=True,
    use_container_width=True
)

# Visualise if in R2 or below 
if n <= 2:
    if n == 1:
        chart = alt.Chart(emb.pca_df).mark_circle(size=60).encode(
            x='Component 1',
            tooltip=['Drug']
        )
    elif n == 2:
        chart = alt.Chart(emb.pca_df).mark_circle(size=60).encode(
            x='Component 1',
            y='Component 2',
            tooltip=['Drug']
        )
    st.altair_chart(
        chart.interactive(),
        use_container_width=True
    )
elif n == 3:
    st.write(f'3D visualisation is a work in progress. For the time being, enjoy this non-interactable pyplot figure:')
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection='3d')
    ax.scatter(
        xs='Component 1',
        ys='Component 2',
        zs='Component 3',
        data=emb.pca_df, 
        marker='x'
    )
    ax.set_xlabel('Component 1')
    ax.set_ylabel('Component 2')
    ax.set_zlabel('Component 3')
    st.pyplot(fig, use_container_width=True)
else:
    st.write(f'Cannot visualise in {n} dimensions.')

# Footer
gap_lines = 5
for _ in range(gap_lines):
    st.write('')
st.subheader('Sources:')
st.write('- BioSNAP dataset: http://snap.stanford.edu/decagon')
st.write('- Decagon paper: https://doi.org/10.1093/bioinformatics/bty294')
st.write('- LibKGE: https://github.com/uma-pi1/kge')
st.write('- SimplE paper: https://doi.org/10.48550/arXiv.1802.04868')
st.write('')
st.write('Contact: oliver.lloyd@bristol.ac.uk, https://github.com/oliver-lloyd')