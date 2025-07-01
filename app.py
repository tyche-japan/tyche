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
            labels = df.iloc[:, 0]  # 첫 번째 열: 항목 이름
            sizes = df.iloc[:, 1]   # 두 번째 열: 값

            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%')

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            chart = base64.b64encode(buf.getvalue()).decode('utf-8')
            buf.close()
            plt.close()

    return render_template('index.html', chart=chart)

if __name__ == '__main__':
    app.run(debug=True)
