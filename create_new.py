import pandas as pd
original = pd.read_csv("./pdf_links/CIF_AND_DOI_DISTINCT.csv")
pdfed = pd.read_csv("./pdf_links/CIF_AND_DOI_DISTINCT_with_links.csv")

pdfed.set_index("DOI",inplace=True)

for index, row in original.iloc[1:].iterrows():
    doi = row["DOI"]
    try:
        new_row = pdfed.loc[doi]
        print(new_row["pdf_link"])
        if (not pd.isna(new_row["pdf_link"])):
            original.at[index,"pdf_link"] = new_row["pdf_link"]

    except Exception as e:
        print(e)
        pass
    if (index % 1000 == 0):
        print(index)
original.to_csv("./CIF_AND_DOI_DISTINCT_LINKS.csv", index=False)
