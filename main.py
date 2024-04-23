import pandas as pd


class Serializer:
    def __init__(self, document_path_netto: str, document_path_brutto: str):
        self.data = None
        self.data_netto = pd.read_csv(document_path_netto, delimiter=";", thousands=".", decimal=",")
        self.data_brutto = pd.read_csv(document_path_brutto, delimiter=";", thousands=".", decimal=",")

    def run(self):
        self.data = self.calculate_percentage()
        self.data['Anteil (Mittelwert)'] = self.data.iloc[:, 1:].mean(axis=1).round(2)
        self.data["Anteil Eigenbedarf (Mittelwert)"] = self.calculate_mean_of_energy_usage()
        self.txt_table(self.data, "result.txt")

    def calculate_percentage(self):
        percentage_df = pd.DataFrame(self.data_netto["Art"])

        for column_name, column in self.data_netto.items():
            if column_name != "Art":
                percentage_df.insert(len(percentage_df.columns), column_name, round((column / column.sum() * 100), 2),
                                     True)

        return percentage_df

    def calculate_mean_of_energy_usage(self):
        difference_df = pd.DataFrame(self.data_netto["Art"])
        mean_df = pd.DataFrame(self.data_brutto["Art"])

        for column_name, column in self.data_netto.items():
            if column_name != "Art":
                difference_df[column_name] = self.data_brutto[column_name] - self.data_netto[column_name]
                mean_df[column_name] = difference_df[column_name] / self.data_brutto[column_name] * 100
        return mean_df.mean(axis=1, numeric_only=True, skipna=True).round(2)

    def txt_table(self, data, filename):
        df = pd.DataFrame(data)
        with open(filename, 'w') as file:
            file.write(df.to_string(index=False))


if __name__ == "__main__":
    serializer = Serializer("./netto.csv", "./brutto.csv")
    serializer.run()
