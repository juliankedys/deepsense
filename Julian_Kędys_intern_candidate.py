import pandas as pd
from pandas.api.types import is_numeric_dtype
import keyboard
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import json


path=input("Specify a path to the tabular file (the same path twice): ")
data=pd.read_csv(path)
#data=pd.read_csv('E:\C++\MOCK_DATA.csv')
app = Flask(__name__)
api = Api(app)


@app.route('/files',methods=["POST","GET"])
def read_file():
    return path


@app.route('/columns',methods=["GET"])
def columns():
    return jsonify({'Number of columns': len(data.columns)})


@app.route('/rows',methods=["GET"])
def rows():
    return jsonify({'Number of rows': len(data)})


@app.route('/mins',methods=["GET"])
def mins():
    mins = {}
    for name in list(data.columns):
        if is_numeric_dtype(data[name]):
            mins[f"Column name: {name}"] = f'Minimal value: {data[name].min()}'
    return mins


@app.route('/means',methods=["GET"])
def mean():
    means = {}
    for name in list(data.columns):
        if is_numeric_dtype(data[name]):
            means[f"Column name: {name}"] = f'Mean value: {data[name].mean()}'
    return means


@app.route('/maxes',methods=["GET"])
def maxes():
    maxes={}
    for name in list(data.columns):
        if is_numeric_dtype(data[name]):
            maxes[f"Column name: {name}"]=f'Maximal value: {data[name].max()}'
    return maxes


@app.route('/10th',methods=["GET"])
def tenth():
    tenth={}
    for name in list(data.columns):
        if is_numeric_dtype(data[name]):
            tenth[f"Column name: {name}"]=f'Tenth percentile: {data[name].quantile(0.1)}'
    return tenth


@app.route('/90th',methods=["GET"])
def ninetieth():
    ninetieth={}
    for name in list(data.columns):
        if is_numeric_dtype(data[name]):
            tenth[f"Column name: {name}"]=f'Ninetieth percentile: {data[name].quantile(0.9)}'
    return ninetieth


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


if __name__ == '__main__':
    app.run(debug=True)