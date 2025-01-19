import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

class CourseManager:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.faculty = self.faculty_df(df)
        self.courses = self.courses_catalog(df)

    def verify_faculty(self, s: str) -> bool:
        words = s.split()
        return len(words) == 1 and words[0].isalpha()

    def faculty_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop(df.columns[0], axis=1)
        df = pd.concat([df[column] for column in df.columns], ignore_index=True)
        df = df.dropna()
        df = df.str.split('-', n=1, expand=True)
        df.iloc[:, 0] = df.iloc[:, 0].apply(lambda s: s.strip())
        df = df[df.iloc[:, 0].apply(lambda s: self.verify_faculty(s))]
        df = df.rename(columns={0: 'code', 1: 'name'})
        df.loc[:, 'code'] = df.loc[:, 'code'].apply(lambda s: s.strip())
        df.loc[:, 'name'] = df.loc[:, 'name'].apply(lambda s: s.strip())

        new_row = pd.DataFrame([{'code': 'TBA', 'name': 'To be announced'}])
        df = pd.concat([df, new_row], ignore_index=True)

        return df

    def courses_catalog(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop(df.columns[0], axis=1)
        df = pd.concat([df[column] for column in df.columns], ignore_index=True)
        df = df.dropna()

        pattern = r'([A-Z]{3} \d{3}.*)'
        df = df.str.extract(pattern)

        df = df.dropna()
        df = df.iloc[:, 0].str.split('-', expand=True)
        df.iloc[:, 3] = df.iloc[:, 3].apply(lambda s: s.split()[0])
        df = df.drop(df.columns[[2, 4]], axis=1)
        df.rename(columns={0: 'cc', 1: 'section', 3: 'faculty'}, inplace=True)
        df = df.applymap(lambda s: s.strip())
        df.loc[:, 'section'] = df.loc[:, 'section'].apply(lambda s: s.lstrip('0'))
        df.loc[:, 'section'] = df.loc[:, 'section'].apply(lambda s: s.rstrip('L'))

        return df

    def faculty_finder(self, cc: str, sec: str) -> str:
        row = self.courses[(self.courses['cc'] == cc) & (self.courses['section'] == sec)].loc[:, 'faculty']
        if row.empty:
            return "Faculty not found"
        row = row.iloc[0]
        fac = self.faculty.loc[self.faculty.loc[:, 'code'] == row].loc[:, 'name'].item()

        return fac

# Usage example
# df = pd.read_excel("data.xlsx")
# course_manager = CourseManager(df)
#
# cc = "EEE 1102"
# sec = "4L"
# faculty_name = course_manager.faculty_finder(cc, sec)
# print(faculty_name)