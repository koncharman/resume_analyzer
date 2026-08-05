

def get_occupation_skills(
    occupation_uri,
    relations,
    skills
):

    # Find skills connected to occupation
    occupation_relations = relations[
        relations["occupationUri"] == occupation_uri
    ]

    # Get skill URIs
    skill_uris = occupation_relations[
        "skillUri"
    ].tolist()


    # Retrieve skill information
    matched_skills = skills[
        skills["conceptUri"].isin(skill_uris)
    ]

    return matched_skills


def get_skill_occupations(
    skill_uri,
    relations,
    occupations
):
    skill_relations = relations[
        relations["skillUri"] == skill_uri
        ]

    occupation_uris = skill_relations[
        "occupationUri"
    ].tolist()

    matched_occupations = occupations[
        occupations["conceptUri"].isin(
            occupation_uris
        )
    ]

    return matched_occupations

def get_skill_skills(
    skill_uri,
    relations,
    skills
):
    skill_relations_org = relations[
        relations["originalSkillUri"] == skill_uri
        ]

    skill_relations_rel = relations[
        relations["relatedSkillUri"] == skill_uri
        ]

    uris_skills=skill_relations_rel['originalSkillUri'].to_list()+skill_relations_org["relatedSkillUri"].to_list()

    # Retrieve skill information
    matched_skills = skills[
        skills["conceptUri"].isin(uris_skills)
    ]

    return matched_skills
