
import pandas as pd

text_cols=['conceptUri','preferredLabel','altLabels','description']

def load_skills():
    df = pd.read_excel(
        "data/skills_en.ods",
        engine="odf"
    )

    return df.loc[:,text_cols]


def load_occupations():
    df = pd.read_excel(
        "data/occupations_en.ods",
        engine="odf"
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