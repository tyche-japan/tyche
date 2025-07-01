from flask import Flask, render_template, request
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    chart = None
    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = pd.read_excel(file)
            plt.figure(figsize=(6, 6))
            df.sum().plot.pie(autopct='%1.1f%%')
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            chart = base64.b64encode(img.getvalue()).decode()
            plt.close()
    return render_template('index.html', chart=chart)

if __name__ == '__main__':
    app.run(debug=True)
