import pandas as pd

def load_data(path = "dataset/spring_data.xlsx"):
    data = pd.read_excel(path)
    return data

def verify_faculty(s):
    words = s.split()
    return len(words) == 1 and words[0].isalpha()

def faculty_df(df):
    df.drop(df.columns[0], axis=1, inplace=True)
    df = pd.concat([df[column] for column in df.columns], ignore_index=True)
    df.dropna(inplace=True)
    df = df.str.split('-', n=1, expand=True)
    df.iloc[:, 0] = df.iloc[:, 0].apply(lambda s: s.strip())
    df = df[df.iloc[:, 0].apply(lambda s: verify_faculty(s))]
    df.rename(columns={0: 'code', 1: 'name'}, inplace = True)
    df.loc[:, 'code'] = df.loc[:, 'code'].apply(lambda s: s.strip())
    df.loc[:, 'name'] = df.loc[:, 'name'].apply(lambda s: s.strip())

    new_row = pd.DataFrame([{'code': 'TBA', 'name': 'To be announced'}])
    df = pd.concat([df, new_row], ignore_index=True)

    return df

def course_catalog (df):
    df = df.drop(df.columns[0], axis = 1)
    df = pd.concat([df[column] for column in df.columns], ignore_index=True)
    df = df.dropna()
    pattern = r'([A-Z]{3} \d{3}.*)'
    df = df.str.extract(pattern).dropna()
    df = df.iloc[:, 0].str.split('-', expand = True)
    df.iloc[:, 3] = df.iloc[:, 3].apply(lambda s: s.split()[0])
    df = df.drop(df.columns[[2,4]], axis = 1)
    df.rename(columns={0: 'cc',
                       1: 'section',
                       3: 'faculty'},
              inplace = True)
    df = df.map(lambda s: s.strip())
    df.loc[:, 'section'] = df.loc[:, 'section'].apply(lambda s: s.lstrip('0'))

    return df

def faculty_finder(courses: pd.DataFrame,
                   faculty: pd.DataFrame,
                   cc: str,
                   sec: str):
    row = courses[(courses['cc'] == cc) & (courses['section'] == sec)].loc[:, 'faculty']
    row = row.iloc[0]
    fac = faculty.loc[faculty.loc[:, 'code'] == row].loc[:, 'name'].item()

    return fac

def main():
    data = load_data()
    faculty = faculty_df(data)
    courses = course_catalog(data)

