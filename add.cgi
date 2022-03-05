#!/usr/bin/python

import cgi
import cgitb
cgitb.enable()

input_data=cgi.FieldStorage()

print 'Content-Type:text/html' #Envia o tipo HTML
print                          #deixa uma linha vazia entre o head e body
print '<h1>Resutados</h1>'
try:
  num1=int(input_data["num1"].value)
  num2=int(input_data["num2"].value)
except:
  print '<p>Desculpe não podemos converter os campos em números (integers).</p>'
  return 1
sum=num1+num2
print '<p>{0} + {1} = {2}</p>'.format(num1, num2, sum)
