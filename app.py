import streamlit as st
from utils.etymology_fetcher import get_etymology
from utils.root_extractor import extract_latin_roots
from utils.find_word_from_roots import find_words_with_latin_root

st.title("📚 Word Helper")

word = st.text_input("Enter a word you want to explore:")

if word:
    st.subheader("🔍 Results for:")
    st.write(f"**Word:** {word}")

    etym = get_etymology(word)
    latin_roots = extract_latin_roots(word)
    st.markdown(f"**Etymology:** {etym}")
    st.subheader("Latin Roots")
    if latin_roots:
        for root in latin_roots:
            st.markdown(f"- {root}")
        st.write("Words with the same Latin root:")
        related_words = find_words_with_latin_root(latin_roots[-1])
        for w in related_words:
            st.markdown(f"- {w}")
    else:
        st.markdown("_No Latin roots found._")
    st.markdown("**Related Words:** *Coming soon...*")
    st.markdown("**Semantic Matches:** *Coming soon...*")
    st.markdown("**Example Sentences:** *Coming soon...*")