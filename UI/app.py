from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dl_results')
def dl_results():
    dl_df = pd.read_csv('dl_results.csv')
    return render_template('dl_results.html', dl_results=dl_df.to_dict(orient='records'))

@app.route('/ml_results')
def ml_results():
    ml_df = pd.read_csv('ml_results.csv')
    print(ml_df.to_dict(orient='records'))
    return render_template('ml_results.html', ml_results=ml_df.to_dict(orient='records'))


@app.route('/model/<model_type>/<model_name>')
def model_detail(model_type, model_name):
    if model_type == 'ml':
        df = pd.read_csv('ml_results.csv')
    elif model_type == 'dl':
        df = pd.read_csv('dl_results.csv')
    else:
        return "Invalid model type", 404
    df['Model_lower'] = df['Model'].str.lower()
    model_data = df[df['Model_lower'] == model_name.lower()]
    
    if model_data.empty:
        return "Model not found", 404

    return render_template('model_detail.html', model=model_data.iloc[0].to_dict(), model_type=model_type)

if __name__ == '__main__':
    app.run(debug=True)