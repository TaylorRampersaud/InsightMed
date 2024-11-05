from flask import Flask, render_template, request
import pandas as pd
import openai
import requests
openai.api_key = "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"

# The class to handle CSV and subject ID filtering
class SubjectData:
    def __init__(self, csv_file, JSON_file):
        """Initialize with CSV file and JSON"""
        self.results = pd.read_csv(csv_file)
        self.defintions = pd.read_json(JSON_file)

    def get_subject_data(self, subject_id):
        """Return all rows matching the subject_id"""
        result_df = self.results[self.results['subject_id'] == subject_id]
        result_df = result_df.loc[result_df.groupby("label")['charttime'].idxmax()]
        result_df = result_df.dropna(subset=['valuenum'])
        return result_df

    def query_medlineplus(self, term, language='English', retmax=10):
        db = 'healthTopics' if language == 'English' else 'healthTopicsSpanish'

        
        url = f"https://wsearch.nlm.nih.gov/ws/query?db={db}&term={term}&retmax={retmax}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses

            # Return the XML content
            return response.text

        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except Exception as e:
            print(f"An error occurred: {e}")
    
                

    def interpret_blood_test(self, result_df):
        prompt = """Interpret these blood test results in a way that a 15-year-old can understand. Use the structure below:\nMetric Name: ____\n
                    Metric Description: (easy to understand version)\nMetric Test Result Interpretation: (avoid numbers, give qualitative results 
                    that are understandable by non-educated patients)\nDO NOT ADD ANYTHING ELSE IN YOUR OUTPUT!!!!!!!!\nYOUR output string should 
                    be wellformated HTML code according to the format before. """
        # prompt = """Interpret these blood test results in a way that a 15-year-old can understand. Use the structure below:\nMetric Name: ____\n
        #             Metric Description: (easy to understand version)\nMetric Test Result Interpretation: (avoid numbers, give qualitative results 
        #             that are understandable by non-educated patients)\nDO NOT ADD ANYTHING ELSE IN YOUR OUTPUT!!!!!!!!\nYOUR output string should 
        #             be wellformated JSON that contains a list of objects that have the test name and interpretation."""

        for index, row in result_df.iterrows():
            row_details = " | ".join([f"{col}: {str(row[col])}" for col in result_df.columns])
            prompt += f"{index + 1}. {row_details}\n" 
        print(prompt)

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a friendly assistant who simplifies information."},
                {"role": "user", "content": prompt}
            ]
        )
        
        interpretation = response['choices'][0]['message']['content']
        return interpretation
        

# Initialize Flask application
app = Flask(__name__)    

# Initialize SubjectData with the CSV file
subject_data = SubjectData('blood_results2.csv', "blood_test_definitions.json")

# Route for the home page with the form
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the search and display results
@app.route('/search', methods=['POST'])
def search():
    # Get the subject_id from the form
    subject_id = request.form['subject_id']
    
    # Convert subject_id to appropriate type if necessary (int here)
    try:
        subject_id = int(subject_id)
    except ValueError:
        return "Invalid Subject ID, must be a number."

    # Get the matching rows from the CSV
    result_df = subject_data.get_subject_data(subject_id)
    test_interpretation = subject_data.interpret_blood_test(result_df)
    interpretations = test_interpretation.split("\n")
    for i in interpretations:
        i = "<p>"+i+"</p>"
    interpretations = "".join(interpretations)
    
    #parse interpretation into individual tests
    #integrate that into result_df (create column)


    # Convert the result DataFrame to HTML table for display
    if not result_df.empty:
        # result_json = result_df.to_json(orient='records') #+ interpretations
        result_json = result_df.to_html(classes='table table-striped', index=False) + interpretations
    else:
        result_json = "No results found for subject_id: {}".format(subject_id)

    # Render the result on the page
    return render_template('results.html', table=result_json)

if __name__ == '__main__':
    app.run(debug=True)