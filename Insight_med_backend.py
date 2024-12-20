import pandas as pd
import openai
import requests
import xml.etree.ElementTree as ET
import json

openai.api_key = "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"

class SubjectData:
    def __init__(self, csv_file):
        self.results = pd.read_csv(csv_file)

    def get_subject_data(self, subject_id):
        result_df = self.results[self.results['subject_id'] == subject_id]
        result_df_max = result_df.loc[result_df.groupby("label")['charttime'].idxmax()]
        result_df_max = result_df_max.dropna(subset=['valuenum'])
        return result_df_max

    def query_medlineplus(self, term, language='English', retmax=10):
        db = 'healthTopics' if language == 'English' else 'healthTopicsSpanish'
        url = f"https://wsearch.nlm.nih.gov/ws/query?db={db}&term={term}&retmax={retmax}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            root = ET.fromstring(response.text)
            summary = ""
            for item in root.findall(".//content"):
                title = item.find("title").text if item.find("title") is not None else "No Title"
                snippet = item.find("snippet").text if item.find("snippet") is not None else "No snippet available"
                summary += f"{title}: {snippet}\n"
            return summary

        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except Exception as e:
            print(f"An error occurred: {e}")
            return "No data found."
    
    def interpret_blood_test(self, result_df):
        prompt = """Interpret these blood test results in a way that a 15-year-old can understand. Ive also given you data 
        on each blood test as an XML file. Can you format your string ouput as a dictionary structure like this: 
        "{"Overview":"a very brief but intuitive overview of patient's potential blood condition",
        "Absolute Basophil Count": {"Metric Description": "Breif overview of what the test is for", "Metric Interpretation": "avoid numbers, give qualitative results that are understandable by non-educated patients",
        "Absolute Eosinophil Count": {"Metric Description": "Desc", "Metric Interpretation": "avoid numbers, give qualitative results that are understandable by non-educated patients"}"...so on and so on for each blood test in the data
        } I only want the string in the output no extra text"""
        
        
        
        # prompt = """Interpret these blood test results in a way that a 15-year-old can understand. Ive also given you data on each blood test as an XML file. Use the 
        #  structure below:\nMetric Name: ____\nMetric Description: (easy to understand version)\nMetric Test 
        #  Result Interpretation: (avoid numbers, give qualitative results that are understandable by non-educated patients)
        #  \nAs for the order of the metrics, show the metrics that require the most attention first (do not use alphabetical 
        #  order). you can combine metrics if they reflect the same conditions \n Also, give a very brief but 
        #  intuitive overview of patient's potential blood condition at the beginning\nDO NOT ADD ANYTHING ELSE IN YOUR 
        #  OUTPUT!!!!!!!!\nYOUR output string should be well-formated HTML code according to the format before.\n """
        
        for index, row in result_df.iterrows():
            row_details = " | ".join([f"{col}: {str(row[col])}" for col in result_df.columns])
            query = self.query_medlineplus(row[0])
            query = str(query)
            prompt += f"{index + 1}. {row_details}. {query}\n"
        
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a friendly assistant who simplifies information."},
                {"role": "user", "content": prompt}
            ]
        )
        
        interpretation = response['choices'][0]['message']['content']

        return interpretation


    def convert_interpretation(self, result_df):
        interpretation = self.interpret_blood_test(result_df)
        print(interpretation)
        interpretation = interpretation[8:-3]
        print(interpretation)
        interpretation = json.loads(interpretation)
        
        return interpretation
        
    
    def full_time_data(self, subject_id):
        df = self.results[self.results['subject_id'] == subject_id]
        df['charttime'] = pd.to_datetime(df['charttime'])
        df = df.sort_values(by=['label', 'charttime'])
        df = df.dropna(subset=['valuenum'])
        result = df.groupby('label').apply(lambda x: x.sort_values('charttime')['valuenum'].tolist()).to_dict()

        return result
    
    def merge_data(self, subject_id):
        data = []
        user_data = self.get_subject_data(subject_id)
        user_data = user_data.groupby('label').apply(lambda x: x.to_dict(orient='records')).to_dict()
        history = self.full_time_data(subject_id)
        for elem1 in user_data:
            for elem2 in history:
                if elem1 == elem2:
                    user_data[elem1][0]["history"] = history[elem2]
        interpretations  = self.convert_interpretation(self.get_subject_data(subject_id))
        for elem1 in user_data:
            for elem2 in interpretations:
                if elem1 == elem2:
                    user_data[elem1][0]["metric_description"] = interpretations[elem2]["Metric Description"]
                    user_data[elem1][0]["metric_interpretation"] = interpretations[elem2]["Metric Interpretation"]
        for key, val in user_data.items():
            data.append(val[0])
        
        output = {
            "data": data,
            "overview": interpretations["Overview"]
        }
        
        
        json_string = json.dumps(output, indent=4)

    
        return json_string
