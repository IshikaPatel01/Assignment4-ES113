
from  flask import Flask, render_template, send_from_directory, request
from flask_mysqldb import MySQL
import numpy as np


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ishik@_1245'
app.config['MYSQL_DB'] = 'ES113'
# app.jinja_options["autoescape"] = lambda _: False
mysql = MySQL(app)




@app.get("/")
def Home():
    bond_number=request.args.get("bond-number")
    bond_no_data=None
    def tuple2list(tup):
        return [list(inner_tuple) for inner_tuple in tup]
    cur=mysql.connection.cursor()
    cur.execute("""use ES113;""")
    
    if bond_number:
        headers = (("Sr No.","Encashment Date", "political party","acc no",
                    "prefix", "bond no", "denominations","pay branch","pay teller"),
                   ("sr no","ref no","journal date","purchase date","exp. date",
                    "name","prefix","bond no","denominations","pay branch","pay teller"))
        cur.execute("""Select * from pp where bondno = {num};""".format(num=bond_number)) 
        bond_data=cur.fetchall() 
        cur.execute("""select * from pd where bond = {num}; """. format(num=bond_number)) 
        purchasedata= cur.fetchall()
        
        bond_no_data = [{"headers": headers[0], "data" : bond_data},
                        {"headers": headers[1], "data":purchasedata}]
        
        
# Question 2
        
    company=request.args.get("name_of_purchaser")
    companydata=None 
  
    
    if company:
        cur.execute("""select extract(year from purchase), count(bond),sum(denom) from pd where name_of_purchaser = '{name}' group by extract(year from purchase) ;""".format(name=company.upper()))
                    
        companydata=tuple2list(cur.fetchall())
    # return render_template("index.html",bond_data=bond_no_data, companydata=companydata)
        
    #Question3    
    politicalpartyname=request.args.get("political-party-name")
    politicalpartydata=None
    
    if politicalpartyname:
        cur.execute("""select extract(year from doe),count(bondno),sum(deno) from pp where partu = '{name}' group by extract(year from doe);""".format(name=politicalpartyname.upper()))
        politicalpartydata=tuple2list(cur.fetchall())
    # return render_template("index.html",bond_data=bond_no_data, companydata=companydata, politicalpartydata=politicalpartydata )
        
# #quetsion 4
    politicaldonations=request.args.get("political_donations_name")
    politicaldonationsdata=None
    
    if politicaldonations:
        cur.execute("""select i.name_of_purchaser, sum(i.denom) from pd as i, (select bondno from pp where partu = '{name}') as j where i.bond = j.bondno group by i.name_of_purchaser;""".format(name=politicaldonations.upper()))
        politicaldonationsdata=tuple2list(cur.fetchall())
    # return render_template("index.html",bond_data=bond_no_data, companydata=companydata, politicalpartydata=politicalpartydata,politicaldonationsdata=politicaldonationsdata)
 
 #question 5

    companydonations=request.args.get("companydonationsname")
    companydonationsdata=None
    
    if companydonations:
        cur.execute("""select P.partu, sum(P.deno) from pp as P, (select bond from pd where name_of_purchaser = '{name}') as E where P.bondno = E.bond group by P.partu;""".format(name=companydonations.upper()))
        companydonationsdata=tuple2list(cur.fetchall())
    # return render_template("index.html",bond_data=bond_no_data, companydata=companydata, politicalpartydata=politicalpartydata,politicaldonationsdata=politicaldonationsdata,companydonationsdata=companydonationsdata)

#question6
    totaldonationsdata=None
    cur.execute("""select partu, sum(deno) from pp group by partu;""")
    totaldonationsdata=tuple2list(cur.fetchall())
    return render_template("index.html",bond_data=bond_no_data, companydata=companydata, politicalpartydata=politicalpartydata,politicaldonationsdata=politicaldonationsdata,companydonationsdata=companydonationsdata,total_donations_data=totaldonationsdata)