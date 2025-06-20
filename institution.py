# academic_portfolio.py
import streamlit as st
import requests
import pandas as pd
import altair as alt

# 🔧 CONFIG: Put your OpenAlex Institution ID here
INSTITUTION_ID = "I130218214"  # Example: Indonesia University of Education


# Function to get data from OpenAlex
def get_openalex_data(institution_id):
    inst = requests.get(f"https://api.openalex.org/institutions/{institution_id}").json()
    works = requests.get(f"https://api.openalex.org/works?filter=institutions.id:{institution_id}&per-page=20&sort=cited_by_count:desc").json()
    return inst, works['results']


# Load data
institution, publications = get_openalex_data(INSTITUTION_ID)

# Institution info
st.set_page_config(page_title="Academic Portfolio", layout="wide")
st.title("🎓 Institutional Academic Portfolio")

st.header("🏛️ Institution Overview")
st.markdown(f"**{institution['display_name']}**")
st.markdown(f"- ROR: {institution.get('ror', 'N/A')}")
st.markdown(f"- Country: {institution.get('country_code', 'N/A')}")
st.markdown(f"- Type: {institution.get('type', 'N/A')}")
st.markdown(f"- Homepage: [{institution.get('homepage_url', 'N/A')}]({institution.get('homepage_url', '#')})")

# Metrics (mocked for now — OpenAlex does not provide total citation count directly)
st.header("📊 At a Glance")
col1, col2 = st.columns(2)
with col1:
    st.metric("Publications Loaded", len(publications))
with col2:
    total_citations = sum([w.get("cited_by_count", 0) for w in publications])
    st.metric("Citations (Top 20)", total_citations)

# Publications Table
st.header("📚 Most Cited Publications")
pub_df = pd.DataFrame([{
    "Title": p["title"],
    "Authors": ", ".join([a["author"]["display_name"] for a in p.get("authorships", [])]),
    "Year": p.get("publication_year"),
    "Citations": p.get("cited_by_count"),
    "Field": ", ".join([c["display_name"] for c in p.get("concepts", [])[:2]]),
    "DOI": p.get("doi", ""),
    "OpenAlex ID": p["id"]
} for p in publications])

st.dataframe(pub_df)

# Field distribution
st.header("📌 Fields of Study (Top 20 Publications)")
field_counts = pub_df["Field"].str.split(", ").explode().value_counts().reset_index()
field_counts.columns = ["Field", "Count"]
chart = alt.Chart(field_counts).mark_bar().encode(
    x="Field:N",
    y="Count:Q",
    tooltip=["Field", "Count"]
).properties(width=800)
st.altair_chart(chart)

# Footer
st.markdown("---")
st.markdown("Powered by [OpenAlex](https://openalex.org) • Made with ❤️ using Streamlit")
