import pandas as pd
import openai
import requests
import xml.etree.ElementTree as ET
import json
from flask import Flask
from flask_cors import CORS
from flask import jsonify
import numpy as np
openai.api_key = "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"

class SubjectData:
    def __init__(self, csv):
        self.results = pd.read_csv(csv)

    def get_subject_data(self, subject_id):
        result_df = self.results[self.results['subject_id'] == subject_id]
        result_df['charttime'] = pd.to_datetime(result_df['charttime'], errors='coerce')
        result_df_max = result_df.loc[result_df.groupby("label")['charttime'].idxmax()]
        result_df_max = result_df_max.dropna(subset=['valuenum'])
        result_df_max['charttime'] = result_df_max['charttime'].dt.strftime('%Y-%m-%d %H:%M:%S')
        return result_df_max
    
    

    def query_medlineplus(self, term, language='English', retmax=3):
        db = 'healthTopics' if language == 'English' else 'healthTopicsSpanish'
        url = f"https://wsearch.nlm.nih.gov/ws/query?db={db}&term={term}&retmax={retmax}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            root = ET.fromstring(response.text)
            summary = ""
            for item in root.findall(".//document"):
                title = None
                snippet = None
                for content in item.findall(".//content"):
                    if content.attrib.get("name") == "title":
                        title = content.text
                    if content.attrib.get("name") == "snippet":
                        snippet = content.text
            
                # If no title or snippet found, provide default text
                title = title if title else "No title available"
                snippet = snippet if snippet else "No snippet available"
                
                # Append to the summary
                summary += f"\nTitle: {title}\nSnippet: {snippet}\n{'-'*50}\n"
            if not summary:
                summary = "No relevant information found."
            return summary

        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except Exception as e:
            print(f"An error occurred: {e}")
            return "No data found."
    
    def interpret_blood_test(self, result_df):
        prompt = """Interpret these blood test results in a way that an averagre adult can understnad. Ive also given you data 
        on each blood test to reference for each blood test. Can you format your string ouput as a dictionary 
        structure like this: "{"Overview":"a brief intuitive paragraph overview of the patient's results and potential 
        conditions/issues", "Absolute Basophil Count": {"Metric Description": "Breif overview of what the test is for", 
        "Metric Interpretation": "avoid numbers, give qualitative results that are understandable for patients (2-5 sentences)",
        "Absolute Eosinophil Count": {"Metric Description": "Breif overview of what the test is for", "Metric Interpretation": "avoid 
        numbers, give qualitative results that are understandable by non-educated patients" (2-5 sentences)}"...so on and so on for 
        each blood test in the data make sure to do each blood test} for the order of the metrics, show the metrics that require the most 
        attention first (do not use alphabetical order). I only want the string in the output no extra text. Do not change the name of the metrics in your output!!"""
        header = ', '.join(result_df.columns) 
        big_string = '\n'.join(result_df.apply(lambda row: ', '.join(row.astype(str)), axis=1)) 
        prompt += header + '\n' + big_string

        for label in result_df.iloc[:, 0]:  
            query = self.query_medlineplus(label) 
            prompt += query

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
        # print(interpretation)
        #interpretation = interpretation[7:-3]
        #print(interpretation)
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
        new_order = list(interpretations.keys())[1:]
        user_data = {key: user_data[key] for key in new_order}
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
        return output

app = Flask(__name__)
CORS(app)
subject_data = SubjectData("/Users/taylorrampersaud/Documents/InsightMed/flask-server/blood_results2.csv")

@app.route("/subject/<subjectID>")
def get_test_data(subjectID):
    print(subjectID)
    result = subject_data.merge_data(int(subjectID))
    def clean_data(obj):
            if isinstance(obj, dict):
                return {key: clean_data(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [clean_data(item) for item in obj]
            elif isinstance(obj, (float, int)) and (np.isnan(obj) or np.isinf(obj)):
                return None
            return obj

    result = clean_data(result)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

