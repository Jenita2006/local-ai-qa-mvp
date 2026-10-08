import streamlit as st

from modules.document_loader import load_documents
from modules.vector_store import VectorStore
from modules.llm import ask_llm, check_ollama
from modules.reliability import calculate_reliability


st.set_page_config(
    page_title="Local Q&A System",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 Local Q&A System")

st.write(
    "Upload your documents, ask questions, "
    "and get answers supported by your documents."
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "vector_store" not in st.session_state:
    st.session_state.vector_store = VectorStore()

if "documents" not in st.session_state:
    st.session_state.documents = []

if "indexed" not in st.session_state:
    st.session_state.indexed = False


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.header("Document Upload")

uploaded_files = st.sidebar.file_uploader(
    "Upload documents",
    type=["pdf", "txt", "docx", "csv"],
    accept_multiple_files=True
)


# ---------------------------------------------------------
# PROCESS DOCUMENTS
# ---------------------------------------------------------

if uploaded_files:

    import os

    os.makedirs(
        "data/documents",
        exist_ok=True
    )

    for uploaded_file in uploaded_files:

        file_path = os.path.join(
            "data/documents",
            uploaded_file.name
        )

        with open(file_path, "wb") as file:

            file.write(
                uploaded_file.getbuffer()
            )


    if st.sidebar.button("Process Documents"):

        with st.spinner(
            "Processing documents..."
        ):

            documents = load_documents()

            st.session_state.documents = documents

            st.session_state.vector_store.build(
                documents
            )

            st.session_state.indexed = True

        st.sidebar.success(
            f"{len(documents)} document sections indexed."
        )


# ---------------------------------------------------------
# SYSTEM STATUS
# ---------------------------------------------------------

st.sidebar.divider()

if check_ollama():

    st.sidebar.success(
        "Local answer system ready"
    )

else:

    st.sidebar.error(
        "Local answer system unavailable"
    )


# ---------------------------------------------------------
# QUESTION
# ---------------------------------------------------------

st.header("Ask Your Question")

question = st.text_input(
    "Enter your question",
    placeholder="Example: How many students are there?"
)


if st.button("Get Answer"):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    elif not st.session_state.indexed:

        st.warning(
            "Please upload and process your documents first."
        )

    elif not check_ollama():

        st.error(
            "The local answer system is not running."
        )

    else:

        with st.spinner(
            "Searching your documents..."
        ):

            results = (
                st.session_state.vector_store.search(
                    question,
                    top_k=3
                )
            )


        if not results:

            st.warning(
                "No relevant information was found."
            )

        else:

            context = "\n\n".join(
                document["text"]
                for document in results
            )


            with st.spinner(
                "Generating answer..."
            ):

                try:

                    answer = ask_llm(
                        question,
                        context
                    )

                    reliability = (
                        calculate_reliability(
                            answer,
                            results
                        )
                    )


                    # -------------------------------------------------
                    # ANSWER
                    # -------------------------------------------------

                    st.subheader("Answer")

                    st.write(answer)


                    # -------------------------------------------------
                    # RELIABILITY
                    # -------------------------------------------------

                    st.subheader(
                        "Reliability Score"
                    )

                    score = reliability["score"]

                    st.progress(
                        score / 100
                    )

                    st.metric(
                        "Reliability",
                        f"{score}/100"
                    )

                    st.write(
                        reliability["label"]
                    )

                    st.caption(
                        reliability["details"]
                    )


                    # -------------------------------------------------
                    # EVIDENCE
                    # -------------------------------------------------

                    st.subheader(
                        "Supporting Evidence"
                    )

                    for document in results:

                        source = document.get(
                            "source",
                            "Unknown"
                        )

                        page = document.get(
                            "page"
                        )

                        if page:

                            location = (
                                f"Page {page}"
                            )

                        else:

                            location = document.get(
                                "file_type",
                                ""
                            )


                        with st.expander(
                            f"{source} — {location}"
                        ):

                            st.write(
                                document["text"]
                            )


                except Exception as error:

                    st.error(
                        f"Error: {error}"
                    )
