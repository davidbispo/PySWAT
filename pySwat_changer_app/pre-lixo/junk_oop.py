# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 21:50:49 2018

@author: david
"""

class Employee:
    
    serial = 0
    
    def __init__(self,name,email,phone, salary):
        self.name = name
        self.email = email
        self.phone = phone
        self.salary = salary
        
        Employee.serial +=1
        self.serial = Employee.serial
        
    def name_email(self):
        return '{} {}'.format(self.name, self.email)
    
    def __str__(self):
        return self.name

emp1 = Employee('bill','bill@aol.com','907-987-6545',3500)
emp2 = Employee('jorge','jorge@aol.com','503-998-7787',4500)

#emp1.__dict__# mostra combinacoes de objetos