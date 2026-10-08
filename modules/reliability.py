import re


def calculate_reliability(answer, retrieved_documents):

    # No evidence found
    if not retrieved_documents:
        return {
            "score": 0,
            "label": "No Evidence",
            "details": "No supporting information was found in the uploaded documents."
        }

    # ---------------------------------------------------------
    # 1. RETRIEVAL STRENGTH
    # ---------------------------------------------------------

    similarity_scores = [
        doc.get("score", 0)
        for doc in retrieved_documents
    ]

    best_similarity = max(similarity_scores)

    # FAISS cosine similarity is approximately -1 to 1.
    # Convert the strongest retrieved evidence to 0-100.
    retrieval_score = max(
        0,
        min(100, best_similarity * 100)
    )


    # ---------------------------------------------------------
    # 2. ANSWER-EVIDENCE MATCH
    # ---------------------------------------------------------

    answer_text = answer.lower()

    evidence_text = " ".join(
        doc.get("text", "")
        for doc in retrieved_documents
    ).lower()


    # ---------------------------------------------------------
    # 3. CHECK IMPORTANT FACTS / NUMBERS
    # ---------------------------------------------------------

    answer_numbers = re.findall(
        r"\b\d+(?:\.\d+)?\b",
        answer_text
    )

    evidence_numbers = re.findall(
        r"\b\d+(?:\.\d+)?\b",
        evidence_text
    )

    number_match = False

    if answer_numbers:

        number_match = all(
            number in evidence_numbers
            for number in answer_numbers
        )


    # ---------------------------------------------------------
    # 4. WORD OVERLAP
    # ---------------------------------------------------------

    answer_words = set(
        re.findall(
            r"\b[a-zA-Z0-9]+\b",
            answer_text
        )
    )

    evidence_words = set(
        re.findall(
            r"\b[a-zA-Z0-9]+\b",
            evidence_text
        )
    )

    if answer_words:

        overlap = (
            len(answer_words & evidence_words)
            / len(answer_words)
        )

    else:

        overlap = 0


    overlap_score = overlap * 100


    # ---------------------------------------------------------
    # 5. FINAL SCORE
    # ---------------------------------------------------------

    # Strong factual match
    if number_match and answer_numbers:

        final_score = max(
            95,
            round(
                retrieval_score * 0.6
                + overlap_score * 0.4
            )
        )

    else:

        final_score = round(
            retrieval_score * 0.6
            + overlap_score * 0.4
        )


    final_score = max(
        0,
        min(100, final_score)
    )


    # ---------------------------------------------------------
    # 6. LABEL
    # ---------------------------------------------------------

    if final_score >= 90:

        label = "Highly Reliable"

    elif final_score >= 75:

        label = "Reliable"

    elif final_score >= 50:

        label = "Partially Supported"

    else:

        label = "Low Support"


    # ---------------------------------------------------------
    # 7. EXPLANATION
    # ---------------------------------------------------------

    if number_match and answer_numbers:

        details = (
            "The answer contains factual information "
            "directly supported by the uploaded document."
        )

    elif final_score >= 75:

        details = (
            "The answer is strongly supported by "
            "the retrieved document evidence."
        )

    elif final_score >= 50:

        details = (
            "The answer has some supporting evidence, "
            "but the retrieved information is not fully conclusive."
        )

    else:

        details = (
            "Only limited supporting evidence was found "
            "for this answer."
        )


    return {
        "score": final_score,
        "label": label,
        "details": details
    }
