# -*- coding: utf-8 -*-
"""
Created on Sun May 29 14:15:09 2016

@author: Matt
"""
import pandas as pd
from unittest import TestCase

from Regression.Reg_Model import Reg_Model

class TestModel(TestCase):
    def test_ridge(self):
        model=Reg_Model()
        x = pd.DataFrame({'x1': [1,2,3,4]})
        y= [1, 2, 3, 4]
        ridge=model.ridge_reg(x,y)
        pred=int(ridge.predict(x)[0])
        
        expected_pred = 1
        
        self.assertEqual(pred, expected_pred)

    def test_gbm(self):
        model=Reg_Model()
        x = pd.DataFrame({'x1': [1,2,3,4]})
        y= [1, 2, 3, 4]
        gbm=model.gbm_reg(x,y)
        pred=int(gbm.predict(x)[0])
        
        expected_pred = 1
        
        self.assertEqual(pred, expected_pred)
    
    def test_pred(self):
        model=Reg_Model()
        x = pd.DataFrame({'x1': [1,2,3,4]})
        y= [1, 2, 3, 4]
        model.set_training(x,y)
        model.calc_model()
        pred = int(model.get_pred(x)[0])
        
        expected_pred = 1
        
        self.assertEqual(pred, expected_pred)

    def test_floor_x(self):
        model = Reg_Model()
        x = pd.DataFrame({'x1':[1,2,3,4,3,2,1,200], 'x2':[20,21,20, 21,20,20,20,24]})
        y = [1, 2, 3, 4, 4, 5, 4, 3]
        model.set_training(x,y)
        max_x1 = max(model.get_x()['x1'])

        exp_max_x1 = 200

        self.assertNotEqual(max_x1, exp_max_x1)

    def test_floor_y(self):
        model = Reg_Model()
        x = pd.DataFrame({'x1':[1,2,3,4,3,2,1,200], 'x2':[20,21,20, 21,20,20,20,24]})
        y = [1, 2, 3, 4, 4, 5, 4, 3]
        model.set_training(x,y)
        max_y = max(model.get_y())

        exp_max_y = 0

        self.assertNotEqual(max_y, exp_max_y)