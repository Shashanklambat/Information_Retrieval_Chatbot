from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=5000,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)

with open("./material/information.txt") as f:
    content = f.read()
    

texts = text_splitter.create_documents([content])

print(*texts, sep="\n")