import numpy as np
from pandas import DataFrame, read_csv
import pandas as pd
from sklearn import linear_model 
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

file = r"crowd_density_time.xlsx"

#read the file
df = pd.read_excel(file)
x_name = df.columns[0]
y_name = df.columns[1]

data = np.array(df)


class LinearReg_Model:
    def __init__(self, data, x_index, y_index, size, seed):
        
        x = data[:,[x_index]]
        #Pre-process the data
        y = np.log(data[:,[y_index]])
        
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y, test_size = size, random_state = seed)
        
        self.regr = linear_model.LinearRegression()
        self.regr.fit(self.x_train, self.y_train)
        self.y_pred = self.regr.predict(self.x_test)
    
    def __str__(self):
        #get information of the graph
        self.coefficient = self.regr.coef_
        self.intercept = self.regr.intercept_
        
        #compute the error
        self.error = mean_squared_error(self.y_test, self.y_pred)
        self.r2 = r2_score(self.y_test, self.y_pred)
        
        #save all values in a dictionary
        model_info = ""
        model_info += "==Model Description==\n"
        model_info += "This model predicts the {} using {}. \n\n".format(y_name.lower(), x_name.lower())
        model_info += "==Model Information==\n"
        model_info += "Coefficient: {:.2f}\n".format(self.coefficient[0][0])
        model_info += "Y-intercept: {:.2f}\n".format(self.intercept[0])
        model_info += "Mean squared error: {:.6f}\n".format(self.error)
        model_info += "R2 error: {:.2f}\n".format(self.r2)
        
        return model_info
        
    def plot_graph(self):
        #plot the graph
        plt.scatter(self.x_test,self.y_test, color = "black")
        plt.plot(self.x_test, self.y_pred, color = "blue")
        plt.xlabel(x_name)
        plt.ylabel(y_name)
        plt.show()
        
    def predict(self, x_val):
        result = self.regr.predict([[10]])
        
        #convert the prediction to correct unit and return prediction in a string
        return "The time taken for the bin to be full when crowd density is {} is {:.2f} minutes".format(x_val, (np.exp(result)[0][0]))
        
    
model = LinearReg_Model(data, 0, 1, 0.4, 42)
print(model)
result = model.predict(10)
print(result)

model.plot_graph()