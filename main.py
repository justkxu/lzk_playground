import pandas as pd


class Serializer:
    def __init__(self, document_path_netto: str, document_path_brutto: str):
        self.path_netto = document_path_netto
        self.path_brutto = document_path_brutto
        self.data_netto = pd.read_csv(self.path_netto, delimiter=";", thousands=".")
        self.data_brutto = pd.read_csv(self.path_brutto, delimiter=";", thousands=".")
        self.data = self.data_netto.astype("object")

    def run(self):
        for year, value in self.data.items():
            helper = 0
            if year != "Art":
                sum = value.sum()
                for zahl in value:
                    self.data.loc[helper, year] = round((zahl/sum)*100, 2)
                    helper += 1
        self.data['Anteil (Mittelwert)'] = self.data.iloc[:, 1:].mean(axis=1)
        self.txt_table(self.data, "result.txt")

    def txt_table(self, data, filename):
        df = pd.DataFrame(data)
        with open(filename, 'w') as file:
            file.write(df.to_string())


if __name__ == "__main__":
    serializer = Serializer("./netto.csv", "./brutto.csv")
    serializer.run()
