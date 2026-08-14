
import pandas as pd
import ezodf

text_cols=['conceptUri','preferredLabel','altLabels','description']

def load_skills():

    doc = ezodf.opendoc("data/skills_en.ods")
    sheet = doc.sheets[0]

    data = [
        [cell.value for cell in row]
        for row in sheet.rows()
    ]

    df=pd.DataFrame(
        data[1:],
        columns=data[0]
    )

    df["altLabels"] = (
        df["altLabels"]
        .fillna("")
        .str.replace("\r\n", "; ", regex=False)
        .str.replace("\n", "; ", regex=False)
        .str.replace("\r", "; ", regex=False)
    )


    return df.loc[:,text_cols]


def load_occupations():

    doc = ezodf.opendoc("data/occupations_en.ods")
    sheet = doc.sheets[0]

    data = [
        [cell.value for cell in row]
        for row in sheet.rows()
    ]

    df=pd.DataFrame(
        data[1:],
        columns=data[0]
    )

    df["altLabels"] = (
        df["altLabels"]
        .fillna("")
        .str.replace("\r\n", "; ", regex=False)
        .str.replace("\n", "; ", regex=False)
        .str.replace("\r", "; ", regex=False)
    )

    return df.loc[:,text_cols]

def load_relations():
    df = pd.read_excel(
        "data/occupationSkillRelations_en.ods",
        engine="odf"
    )

    return df

def load_skill_relations():
    df = pd.read_excel(
        "data/skillSkillRelations_en.ods",
        engine="odf"
    )

    return df