import streamlit as st
import pandas as pd
import altair as alt
from openalex_api import get_author, get_works_by_author, get_related_concepts, get_coauthors
from utils import generate_wordcloud

st.set_page_config(page_title="Academic Portfolio", layout="wide")
st.title("🎓 Academic Portfolio")

author_id = st.text_input("Enter OpenAlex Author ID (e.g. A1969205036)", "A1969205036")

if author_id:
    author = get_author(author_id)
    works = get_works_by_author(author_id)

    st.header(f"👤 {author['display_name']}")
    institutions = author.get('last_known_institutions', [])
    if institutions:
        inst_names = ", ".join([inst['display_name'] for inst in institutions])
    else:
        inst_names = "N/A"
    st.markdown(f"**Institution(s)**: {inst_names}")

    st.subheader("📚 Publications")
    df = pd.DataFrame([{
        "Title": w["title"],
        "Year": w["publication_year"],
        "Citations": w["cited_by_count"],
        "DOI": w.get("doi", ""),
    } for w in works])
    st.dataframe(df)

    st.subheader("📈 Citation Analytics")
    yearly = df.groupby("Year")["Citations"].sum().reset_index()
    chart = alt.Chart(yearly).mark_line(point=True).encode(
        x="Year:O", y="Citations:Q"
    ).properties(width=600, height=300)
    st.altair_chart(chart)

    st.subheader("🧠 Fields of Study")
    all_concepts = []
    for w in works:
        all_concepts.extend(get_related_concepts(w))
    fig = generate_wordcloud(all_concepts)
    st.pyplot(fig)

    st.subheader("👥 Co-authorship Network")
    coauthors = get_coauthors(works, author_id)
    co_df = pd.DataFrame(list(coauthors.items()), columns=["Name", "Count"]).sort_values("Count", ascending=False)
    st.dataframe(co_df)

