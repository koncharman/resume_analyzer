
from utils.data_loader import load_skills, load_occupations


skills = load_skills()
occupations = load_occupations()


print(skills.head())
print(skills.columns)

print(occupations.head())
print(occupations.columns)

