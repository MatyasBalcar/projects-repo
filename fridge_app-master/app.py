import csv
from flask import Flask, render_template, request, redirect, url_for
import datetime
import uuid

app = Flask(__name__)

def read_data():
    with open('scans.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header
        return list(reader)

def write_data(data):
    with open('scans.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Code', 'Date', 'Open', 'Expiry Date', 'Id'])
        writer.writerows(data)

@app.route('/')
def index():
    data = read_data()
    return render_template('index.html', data=data)

@app.route('/update_open', methods=['POST'])
def update_open():
    id_to_update = request.form['id']
    data = read_data()
    for row in data:
        if row[4] == id_to_update:
            if row[2] != 'Ne':
                row[2] = 'Ne'  # Set to 'Ne' if it's not 'Ne' already
            else:
                row[2] = datetime.datetime.now().date().strftime("%Y-%m-%d")  # Set to current date otherwise
    write_data(data)
    return redirect(url_for('index'))

@app.route('/remove', methods=['POST'])
def remove():
    id_to_remove = request.form['id']
    data = read_data()
    updated_data = [row for row in data if row[4] != id_to_remove]
    write_data(updated_data)
    return redirect(url_for('index'))
    
@app.route('/update_expiry', methods=['POST'])
def update_expiry():
    id_to_update = request.form['id']
    expiry_date = request.form['expiry_date']
    data = read_data()
    for row in data:
        if row[4] == id_to_update:
            row[3] = expiry_date
            break
    write_data(data)
    return redirect(url_for('index'))
if __name__ == "__main__":
    app.run(debug=True)
