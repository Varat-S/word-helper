import streamlit as st
from utils.etymology_fetcher import get_etymology
from utils.root_extractor import extract_latin_roots
from utils.find_word_from_roots import find_words_with_latin_root
from utils.examples_sentences_finder import get_example_sentences
from dotenv import load_dotenv
import os
import cohere
import time

# Load environment variables
load_dotenv()
api_key = os.getenv("COHERE_API_KEY")

# Initialize Cohere
co = cohere.Client(api_key)

st.title("📚 Word Helper")

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
            st.markdown("**AI Output (Forms):**")
            try:
                response = co.chat(
                    model="command-r-plus",
                    message=f"Tell me all the Latin forms of the root '{root}', separated by commas."
                )
                ai_text = response.text.strip()
                st.markdown(ai_text)
                print("[DEBUG] AI output:", ai_text)

                # Parse root forms safely
                if ai_text:
                    root_forms = [w.strip().lower() for w in ai_text.split(",") if w.strip()]
                else:
                    root_forms = [root.lower()]
            except Exception as e:
                st.error(f"API error: {e}")
                root_forms = [root.lower()]
                print("[DEBUG] API fallback root used:", root)

            # Find and display related words
            st.markdown(f"Words with the same Latin root as **{root}**:")
            related_words = find_words_with_latin_root(root_forms)
            if related_words:
                for w in related_words:
                    st.markdown(f"- {w}")
            else:
                st.markdown("_No related words found._")
    else:
        st.markdown("_No Latin roots found._")

    # Placeholder sections
    st.markdown("**Related Words:** *Coming soon...*")
    st.markdown("**Semantic Matches:** *Coming soon...*")
    st.markdown("**Example Sentences And Phrases:**")

    # Get examples from Wordnet and Tatoeba
    examples = get_example_sentences(word.strip())
    if examples:
        # Finding the best examples
        max_len = 500
        filtered_examples = [s for s in examples if 10 <= len(s) <= max_len]
        score_cal_examples = []
        batch_size = 500
        min_score = 0.005
        for i in range(0, len(filtered_examples), batch_size):
            batch = filtered_examples[i:i+batch_size]
            for attempt in range(10):
                try:
                    response = co.rerank(query=word, documents=batch, top_n=min(20, len(batch)), model="rerank-english-v3.0")
                    score_cal_examples.extend([
                (batch[r.index], r.relevance_score)
                for r in response.results if r.relevance_score > min_score
                ])
                    break
                except:
                    print(f"Rate limit hit, retry {attempt+1}/10. Waiting 60 seconds...")
                    time.sleep(60)
            if i>=batch_size*8:
                break
        for i, (sentence, score) in enumerate(sorted(score_cal_examples, key=lambda x: x[1], reverse=True)[:10]):
            st.markdown(f"{i+1}. {sentence}")
    else:
        st.write("- No example sentences found.")