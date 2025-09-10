#!/bin/python3

bits=8
def uni(data):
	print("Unipolar NRZ Encoding: ")
	for i in data:
		if i=='0':
			print("0", end=" ")
		elif i=='1':
			print("+1", end=" ")
	print()

def pol(data):
	print("Polar NRZ-L Encoding: ")
	for i in data:
		if i=='1':
			print("-1", end=" ")
		elif i=='0':
			print("+1", end=" ")
	print()

data = (input("Enter data: "))
pol(data)
uni(data)
