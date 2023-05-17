import datetime
import math
import altair as alt

# Other Libs
import pandas as pd
import streamlit as st


df_family_sizes = pd.read_pickle("family-sizes.pickle")
df_state_sizes = pd.read_pickle("state-sizes.pickle")

"""
## Statistics collected using AR synthesis method implemented in [PAYNT](https://github.com/randriu/synthesis/)
"""

chart_families = alt.Chart(df_family_sizes).mark_boxplot(extent='min-max').encode(
    x="family_size:O",
    y=alt.Y(
        'time_sec',
        scale=alt.Scale(type="log")  # Here the scale is applied
    )
)


chart_states = alt.Chart(df_state_sizes).mark_boxplot(extent='min-max').encode(
    x="mdp_size:O",
    y=alt.Y(
        'time_sec',
        scale=alt.Scale(type="log")  # Here the scale is applied
    )
)

tab1, tab2 = st.tabs(["design-space sizes", "quotient MDP size"])

with tab1:
    st.altair_chart(chart_families, theme="streamlit", use_container_width=True)
with tab2:
    st.altair_chart(chart_states, theme="streamlit", use_container_width=True)

