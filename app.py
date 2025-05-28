import streamlit as st

st.title("📚 Word Helper")

# Input field
word = st.text_input("Enter a word you want to explore:")

# Placeholder output
if word:
    st.subheader("🔍 Results for:")
    st.write(f"**Word:** {word}")
    
    st.markdown("**Etymology:** *Coming soon...*")
    st.markdown("**Related Words:** *Coming soon...*")
    st.markdown("**Semantic Matches:** *Coming soon...*")
    st.markdown("**Example Sentences:** *Coming soon...*")