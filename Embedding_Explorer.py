from simple_biosnap import Embeds
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt


# Load and prep embedding data
st.session_state.emb = Embeds()
st.session_state.emb.pca()

# Header
st.title('SimplE embeddings of BioSNAP drugs')
st.write('This page allows you to project the data down to 3 or fewer dimensions, in order to visualise the drug embeddings')

# Show Zitnik et al's figure
st.image(
    'fig/zitnik_et_al_schema.jpeg', 
    caption='Sample snapshot of the input data, taken from Zitnik et al\'s paper, \
        available at: https://doi.org/10.1093/bioinformatics/bty294'
)

# User input
st.link_button(
    'Full 256-dimension dataset avilable here',
    url='https://github.com/oliver-lloyd/SimplE_BioSNAP/blob/master/data/raw_embed_df.csv'
)

n = st.slider(
    'Desired number of dimensions in projection.', 
    min_value=1,
    max_value=3
)

# Project and show
st.session_state.emb.pca(n)
cols_to_show = ['Drug'] + [f'Component {i+1}' for i in range(n)]
st.dataframe(
    st.session_state.emb.pca_df[cols_to_show], 
    hide_index=True,
    use_container_width=True
)

# Visualise if in R3 or below 
tooltips = ['Drug', 'Pubchem_ID', 'formula', 'molecular_weight', 'URL']
if n <= 2:
    if n == 1:
        chart = alt.Chart(st.session_state.emb.pca_df).mark_circle(size=60).encode(
            x='Component 1',
            tooltip=tooltips
        )
    elif n == 2:
        chart = alt.Chart(st.session_state.emb.pca_df).mark_circle(size=60).encode(
            x='Component 1',
            y='Component 2',
            tooltip=tooltips
        )
    st.altair_chart(
        chart.interactive(),
        use_container_width=True
    )
elif n == 3:
    st.write(f'3D visualisation is a work in progress. For the time being, enjoy this ugly pyplot figure:')
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection='3d')
    ax.scatter(
        xs='Component 1',
        ys='Component 2',
        zs='Component 3',
        data=st.session_state.emb.pca_df, 
        marker='x'
    )
    ax.set_xlabel('Component 1')
    ax.set_ylabel('Component 2')
    ax.set_zlabel('Component 3')
    st.pyplot(fig, use_container_width=True)
else:
    st.write(f'Cannot visualise in {n} dimensions.')
