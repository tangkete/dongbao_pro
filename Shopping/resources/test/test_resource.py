# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, request

class TestCase(Resource):
    def post(self):
        rq = reqparse.RequestParser()
        rq.add_argument('page_size', type=int, required=True)
        req = rq.parse_args()
        pageSize = req.page_size
        self.relCategory1Id = request.form.get('relCategory1Id')
        return {'msg': pageSize, 'data1': self.relCategory1Id}
