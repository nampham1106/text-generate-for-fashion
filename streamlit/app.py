import streamlit as st
import json
import requests

from rank_bm25 import BM25Okapi
from footer import ft



def generate(input_text, max_length=200, k=3, on=3):
    
    url = "http://fastapi:8000/generate/"
    data = {
        "prompt": input_text,
        "max_length": max_length,
        "k": k,
        "on": on
    }

    response = requests.post(url, json=data)
    

    st.subheader("Generated Sequences:")
    for i in range(3):
        st.write(response.json()["generated_texts"][i])

with open('fashion_15_10_2022_train.txt', 'r', encoding='utf-8') as train_file:
    train_documents = [line.strip() for line in train_file]
with open('fashion_15_10_2022_test.txt', 'r', encoding='utf-8') as test_file:
    test_documents = [line.strip() for line in test_file]

all_documents = train_documents + test_documents
preprocessed_documents = [document.lower().split() for document in all_documents]
bm25 = BM25Okapi(preprocessed_documents)

# Streamlit UI



with st.sidebar:
    st.title('511 SOFTWARE')
    add_radio = st.radio(
        ":blue[Lựa chọn model] :sunglasses:",
        ("BM25", "BM25 - GPT 2 finetuned", "GPT2 finetuned")
    )
    input_text = st.text_input("Enter input text:", "áo khoác")
    if add_radio == 'GPT2 finetuned' :
        max_length = st.slider("Max Length", min_value=10, max_value=512, value=100)
        num_beams = st.slider("Num Beams", min_value=1, max_value=10, value=3)
        num_return_sequences = st.slider("Num Return Sequences", min_value=1, max_value=10, value=3)


if add_radio == "BM25":

    my_dict = {}
    st.header("Xếp hạng các văn bản theo độ phù hợp", divider='rainbow')
    if st.button("Tìm kiếm"):
        query = input_text.lower().split()
        scores = bm25.get_scores(query)
        ranked_documents = sorted(zip(range(len(all_documents)), scores), key=lambda x: x[1], reverse=True)[:3]
        st.write("Kết quả model BM-25:")
        for idx, score in ranked_documents:
            key = 'Document ' + str(idx + 1)
            start_index = all_documents[idx].find("<|beginofdes|>") + 14
            end_index = all_documents[idx].find("<|endofdes|>")
            desired_sentence = input_text + ': ' + (all_documents[idx])[start_index:end_index]
            my_dict[key] = desired_sentence
            with st.expander(f"Document {idx + 1}: Score = {score}"):
                st.write(desired_sentence)
                
        with open("my_dict.json", "w") as json_file:
            json.dump(my_dict, json_file)

elif add_radio == "BM25 - GPT 2 finetuned":
    st.header("GENERATE CONTENT", divider='rainbow')
    with open("my_dict.json", "r") as json_file:
        data_from_json = json.load(json_file)
    
    for key, value in data_from_json.items():
        st.write(f"{value}")
        if st.button(key + ' generate:'):
            generated_text = generate(value)
            st.subheader("Generated Sequences:")
            st.write(generated_text)

elif add_radio == "GPT2 finetuned":
    st.header('GENERATE CONTENT', divider='rainbow')
    if st.button("Generate"):
        generate(input_text + '<|beginofdes|>', max_length, num_beams, num_return_sequences)

st.markdown(ft, unsafe_allow_html=True)