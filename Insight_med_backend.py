from flask import Flask, render_template, request
import pandas as pd
import openai
import requests
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import os

openai.api_key = "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"


class SubjectData:
    def __init__(self, csv_file):
        self.results = pd.read_csv(csv_file)
        self.static_folder = 'static/graphs'

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
        prompt = """Interpret these blood test results in a way that a 15-year-old can understand. Ive also given you data on each blood test as an XML file. Use the 
         structure below:\nMetric Name: ____\nMetric Description: (easy to understand version)\nMetric Test 
         Result Interpretation: (avoid numbers, give qualitative results that are understandable by non-educated patients)
         \nAs for the order of the metrics, show the metrics that require the most attention first (do not use alphabetical 
         order). you can combine metrics if they reflect the same conditions \n Also, give a very brief but 
         intuitive overview of patient's potential blood condition at the beginning\nDO NOT ADD ANYTHING ELSE IN YOUR 
         OUTPUT!!!!!!!!\nYOUR output string should be well-formated HTML code according to the format before.\n """
        
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
    
    def full_time_data(self, subject_id):
        result_df = self.results[self.results['subject_id'] == subject_id]
        return result_df
    
   

    def graphical_results(self, subject_id):
        result_df = self.full_time_data(subject_id)

        unique_labels = result_df['label'].unique()

        graph_paths = []
        for label in unique_labels:
            label_data = result_df[result_df['label'] == label]
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(label_data['charttime'], label_data['valuenum'], marker='o', linestyle='-', color='b')
            ax.set_title(f"{label} Over Time", fontsize=12)
            ax.set_xlabel("Time", fontsize=10)
            ax.set_ylabel("Value", fontsize=10)
            ax.tick_params(axis='x', rotation=45)

            img_path = os.path.join(self.static_folder, f"{subject_id}_{label}.png")
            fig.savefig(img_path, format='png', bbox_inches='tight')
            graph_paths.append(img_path)
            plt.close(fig)

        return graph_paths

app = Flask(__name__)    
subject_data = SubjectData('blood_results2.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    subject_id = request.form['subject_id']
    
    try:
        subject_id = int(subject_id)
    except ValueError:
        return "Invalid Subject ID, must be a number."

    result_df = subject_data.get_subject_data(subject_id)
    test_interpretation = subject_data.interpret_blood_test(result_df)
    interpretations = "".join([f"<p>{line}</p>" for line in test_interpretation.split("\n")])
    
    if not result_df.empty:
        result_html = result_df.to_html(classes='table table-striped', index=False)
    else:
        result_html = f"No results found for subject_id: {subject_id}"

    return render_template('results.html', table=result_html, interpretations=interpretations)

if __name__ == '__main__':
    app.run(debug=True)
