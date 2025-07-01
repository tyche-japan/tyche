from flask import Flask, render_template, request
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def create_pie_chart(labels, sizes):
    sorted_df = pd.DataFrame({"label": labels, "size": sizes})
    sorted_df = sorted_df.sort_values(by="size", ascending=False)

    top_n = 10
    top_labels = sorted_df["label"].iloc[:top_n]
    top_sizes = sorted_df["size"].iloc[:top_n]
    other_size = sorted_df["size"].iloc[top_n:].sum()

    final_labels = list(top_labels) + ["기타"]
    final_sizes = list(top_sizes) + [other_size]

    fig, ax = plt.subplots()
    ax.pie(final_sizes, labels=final_labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    chart = base64.b64encode(buf.getvalue()).decode()
    buf.close()
    plt.close()

    sorted_df["비율(%)"] = sorted_df["size"] / sorted_df["size"].sum() * 100
    top_list = sorted_df.iloc[:top_n][["label", "비율(%)"]].to_dict(orient="records")

    return chart, top_list

@app.route("/", methods=["GET", "POST"])
def index():
    quantity_chart = None
    quantity_list = None
    price_chart = None
    price_list = None

    if request.method == "POST":
        file = request.files["file"]
        if file:
            df = pd.read_excel(file)

            if "BRAND" not in df.columns or "数量" not in df.columns or "値段合計" not in df.columns:
                return "엑셀에 'BRAND', '数量', '値段合計' 컬럼이 있어야 합니다."

            # 数量 기준
            quantity_group = df.groupby("BRAND")["数量"].sum()
            quantity_chart, quantity_list = create_pie_chart(quantity_group.index, quantity_group.values)

            # 値段合計 기준
            price_group = df.groupby("BRAND")["値段合計"].sum()
            price_chart, price_list = create_pie_chart(price_group.index, price_group.values)

    return render_template("index.html", 
                           quantity_chart=quantity_chart, quantity_list=quantity_list,
                           price_chart=price_chart, price_list=price_list)

if __name__ == "__main__":
    app.run(debug=True)
