import pandas as pd
from pandas.api.types import is_numeric_dtype
import keyboard
from flask import Flask, jsonify, request, redirect
from flask_restful import Resource, Api, reqparse
import numpy as np
import json
import requests
import random
import os
import urllib.request
from app import *
from werkzeug.utils import secure_filename


path=input("Specify a path to the tabular file (the same path twice): ")
data=pd.read_csv(path)
#E:\C++\MOCK_DATA.csv
#E:\C++\data.csv
app = Flask(__name__)
api = Api(app)


@app.route('/files',methods=["POST","GET"])
def read_file():
    return path


@app.route('/columns',methods=["GET","POST"])
def columns():
    filename = read_file()
    return jsonify({'Number of columns': json.loads(str(len(data.columns))), ' File': filename})


@app.route('/rows',methods=["GET","POST"])
def rows():
    filename=read_file()
    return jsonify({'Number of rows': json.loads(str(len(data))),' File': filename})


@app.route('/mins',methods=["GET","POST"])
def mins():
    mins = {}
    filename=read_file()
    for name in list(data.columns):
        if is_numeric_dtype(data[name]):
            tmp=data[name].min()
            if tmp==None:
                s = set(data[name])
                mins[f"Column name: {name}"] = f'Minimal value: {sorted(s)[1]}'
            else:
                mins[f"Column name: {name}"] = f'Minimal value: {tmp}'
    mins[" File "] = filename
    print("mins: \n")
    print(mins)
    return mins


@app.route('/mins/<ID>',methods=['GET','POST'])
def get_mins(ID):
    if int(ID)<len(data):
        filename=read_file()
        min=mins()
        return jsonify({'ID':ID,'Column name':list(min)[int(ID)],'': list(min.values())[int(ID)], ' File': filename})


@app.route('/means',methods=["GET","POST"])
def means():
    means = {}
    filename=read_file()
    for name in list(data.columns):
        if is_numeric_dtype(data[name]):
            means[f"Column name: {name}"] = f'Mean value: {data[name].mean()}'
    means[" File "] = filename
    return means


@app.route('/means/<ID>',methods=['GET','POST'])
def get_means(ID):
    if int(ID)<len(data):
        filename=read_file()
        mean=means()
        return jsonify({'ID': ID, '*': list(mean)[int(ID)], '-': list(mean.values())[int(ID)],' File': filename})


@app.route('/maxes',methods=["GET","POST"])
def maxes():
    maxes={}
    filename = read_file()
    for name in list(data.columns):
        if is_numeric_dtype(data[name]):
            maxes[f"Column name: {name}"]=f'Maximal value: {data[name].max()}'
    maxes[" File "] = filename
    return maxes


@app.route('/maxes/<ID>',methods=['GET','POST'])
def get_columns(ID):
    if int(ID)<=len(data):
        filename=read_file()
        ma = maxes()
        return jsonify({'ID': ID, '*': list(ma)[int(ID)], '-': list(ma.values())[int(ID)], ' File': filename})


@app.route('/10th',methods=["GET","POST"])
def tenth():
    tenth={}
    filename = read_file()
    for name in list(data.columns):
        if is_numeric_dtype(data[name]):
            tenth[f"Column name: {name}"]=f'Tenth percentile: {data[name].quantile(0.1)}'
    tenth[" File "] = filename
    return tenth


@app.route('/10th/<ID>',methods=['GET','POST'])
def get_tenth(ID):
    if int(ID)<=len(data):
        filename=read_file()
        t = tenth()
        return jsonify({'ID': ID, '*': list(t)[int(ID)], '-': list(t.values())[int(ID)], ' File': filename})


@app.route('/90th',methods=["GET","POST"])
def ninetieth():
    ninetieth={}
    filename = read_file()
    for name in list(data.columns):
        if is_numeric_dtype(data[name]):
            ninetieth[f"Column name: {name}"]=f'Tenth percentile: {data[name].quantile(0.9)}'
    ninetieth[" File "] = filename
    return ninetieth


@app.route('/90th/<ID>',methods=['GET','POST'])
def get_ninetieth(ID):
    if int(ID)<=len(data):
        filename=read_file()
        n = ninetieth()
        return jsonify({'ID': ID, '*': list(n)[int(ID)], '-': list(n.values())[int(ID)], ' File': filename})


@app.route('/percent',methods=["GET","POST"])
def percent():
    percent={}
    filename = read_file()
    for name in list(data.columns):
        p=round(100 * data[name].isna().sum() / len(data[name]), 2)
        percent[f"Column name: {name}"]=f'Percentage of missing values {p}%'
    percent[" File: "] = filename
    return percent


@app.route('/percent/<ID>',methods=['GET','POST'])
def get_percent(ID):
    if int(ID)<=len(data):
        filename=read_file()
        p = percent()
        return jsonify({'ID': ID, '*': list(p)[int(ID)], '-': list(p.values())[int(ID)], ' File': filename})


#Simulate null values in the file
for i in range(1, random.randint(2,12)):
    column=data.columns[random.randint(0,len(data.columns)-1)]
    row=random.randint(0,len(data)-1)
    data.at[row,column]=None


data_arg = reqparse.RequestParser()
data_arg.add_argument("ID", type=int, help="Enter ID")
data_arg.add_argument("Name", type=str, help="Enter Name")
data_arg.add_argument("Language", type=str, help="Enter Language")
data_arg.add_argument("Age", type=int, help="Enter Age")


class Read(Resource):
    def __init__(self):
        self.data = data

    def get(self,ID):
        data_out = self.data.loc[self.data['ID'] == ID].to_json(orient="records")
        return jsonify({'message': json.loads(data_out)})

api.add_resource(Read, '/<int:ID>')


class Post(Resource):
    def __init__(self):
        self.data = data

    def post(self):
        ar = data_arg.parse_args()
        # if the object is already present:
        if ((self.data['ID'] == ar.ID).any()):
            return jsonify({"message": 'Object already present'})
        else:
            self.data = self.data.append(ar, ignore_index=True)
            self.data.to_csv(path, index=False)
            return jsonify({"message": 'Operation successful'})

api.add_resource(Post, '/')


@app.route('/',methods=["GET","POST"])
def starter():
    max_id=rows()
    return jsonify({"For displaying rows of the file ":"/rows",
                    "For displaying columns of the file ":"/columns",
                    "For displaying mean values of specific columns ":"/means",
                    "For displaying minimal values of specific columns ":"/mins",
                    "For displaying maximal values of specific columns ":"/maxes",
                    "For displaying values equal to the tenth percentile of specific columns ":"/10th",
                    "For displaying values equal to the ninetieth percentile of specific columns ":"/90th",
                   "For displaying the percentage of missing values in specific columns ":"/percent",
                    "To access a singular element from the file simply follow the address with /ID_of_the_element (e.g. http://127.0.0.1:5000/1 for accessing first element)":f'The IDs range from 1 to {json.loads(str(len(data)))}'})


target_folder = 'E:\C++'
app.config['target_folder'] = target_folder
ext = set(['csv'])


def allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ext


@app.route('/upload', methods=['GET','POST'])
def upload():
    if 'file' not in request.files:
        res = jsonify({'Error': '"File" should be chosen as upload type'})
        res.status_code = 400
        return res
    file = request.files['file']
    if file.filename == '':
        res = jsonify({'Error': 'No file selected for uploading'})
        res.status_code = 400
        return res
    if file and allowed(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['target_folder'], filename))
        res = jsonify({'Success': 'File has been uploaded'})
        res.status_code = 201
        global csv_name
        csv_name = file.filename
        return res
    else:
        res = jsonify({'Accepted file extenstions': 'csv'})
        res.status_code = 400
        return res


if __name__ == '__main__':
    app.run(debug=True)
