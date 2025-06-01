import streamlit as st
from utils.etymology_fetcher import get_etymology
from utils.root_extractor import extract_latin_roots
from utils.find_word_from_roots import find_words_with_latin_root
from dotenv import load_dotenv
import os
import cohere

# Load environment variables
load_dotenv()
api_key = os.getenv("COHERE_API_KEY")

# Initialize Cohere
co = cohere.Client(api_key)

st.title("📚 Word Helper")

# Text input
word = st.text_input("Enter a word you want to explore:")

if word:
    st.subheader("🔍 Results for:")
    st.write(f"**Word:** {word}")

    # Etymology
    etym = get_etymology(word)
    st.markdown(f"**Etymology:** {etym}")

    # Extract Latin roots
    latin_roots = extract_latin_roots(word)
    st.subheader("Latin Roots")
    if latin_roots:
        for root in latin_roots:
            st.markdown(f"- {root}")

            try:
                st.markdown("**AI Output:**")
                response = co.chat(
                    model="command-r-plus",
                    message="What are all the forms of the latin root '{}'?".format(root)
                )
                ai_text = response.text
                st.markdown(ai_text)
                print("[DEBUG] Cohere response:", ai_text)

            except Exception as e:
                st.error(f"API error: {e}")
                print("[DEBUG] API error:", e)


        # Related words
        st.write("Words with the same Latin root:")
        related_words = find_words_with_latin_root(latin_roots[-1])
        for w in related_words:
            st.markdown(f"- {w}")
    else:
        st.markdown("_No Latin roots found._")

    # Placeholder sections
    st.markdown("**Related Words:** *Coming soon...*")
    st.markdown("**Semantic Matches:** *Coming soon...*")
    st.markdown("**Example Sentences:** *Coming soon...*")
