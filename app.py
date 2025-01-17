# Flask Routes and functions adapted from and influenced by Source: https://github.com/osu-cs340-ecampus/flask-starter-app and OSU ed discussions 10/26/22 through 12/5/22

import os
from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
from flask import send_from_directory


# Configuration

app = Flask(__name__)

# database connection
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_clarkeab"
app.config["MYSQL_PASSWORD"] = "5328"
app.config["MYSQL_DB"] = "cs340_clarkeab"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Routes


@app.route('/')
def root():
    return render_template("home.j2")

# Pets page routes


@app.route('/search', methods=["POST"])
def search():
    if request.method == "POST":
        query = "SELECT Pets.pet_id, Shelters.name AS Shelter, Fosters.name AS Foster, type AS Type, weight AS Weight, is_kid_friendly AS KidFriendly, Pets.name AS Name, age AS Age, breed AS Breed, gender AS Gender, is_adopted AS Adopted FROM Pets JOIN Shelters ON Pets.shelter_id = Shelters.shelter_id LEFT JOIN Fosters ON Pets.foster_id = Fosters.foster_id WHERE Pets.name = '%s'" % (
            request.form['search'])
        cur = mysql.connection.cursor()
        cur.execute(query)
        results = cur.fetchall()

        query2 = "SELECT Pets.pet_id, Shelters.name AS Shelter, Fosters.name AS Foster, type AS Type, weight AS Weight, is_kid_friendly AS KidFriendly, Pets.name AS Name, age AS Age, breed AS Breed, gender AS Gender, is_adopted AS Adopted FROM Pets JOIN Shelters ON Pets.shelter_id = Shelters.shelter_id LEFT JOIN Fosters ON Pets.foster_id = Fosters.foster_id"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        data = cur.fetchall()

        query3 = "SELECT Shelters.shelter_id, Shelters.name AS Shelter from Shelters ORDER BY Shelters.name ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        shelter_data = cur.fetchall()

        query4 = "SELECT Fosters.foster_id, Fosters.name AS Foster FROM Fosters"
        cur = mysql.connection.cursor()
        cur.execute(query4)
        foster_data = cur.fetchall()

        return render_template("pets.j2", results=results, data=data, shelter_data=shelter_data, foster_data=foster_data)


@app.route('/pets', methods=["GET", "POST"])
def pets():
    if request.method == "GET":
        query = "SELECT Pets.pet_id, Shelters.name AS Shelter, Fosters.name AS Foster, type AS Type, weight AS Weight, is_kid_friendly AS KidFriendly, Pets.name AS Name, age AS Age, breed AS Breed, gender AS Gender, is_adopted AS Adopted FROM Pets JOIN Shelters ON Pets.shelter_id = Shelters.shelter_id LEFT JOIN Fosters ON Pets.foster_id = Fosters.foster_id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # dropdown
        query2 = "SELECT Shelters.shelter_id, Shelters.name AS Shelter from Shelters ORDER BY Shelters.name ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        shelter_data = cur.fetchall()

        # dropdown
        query3 = "SELECT Fosters.foster_id, Fosters.name AS Foster FROM Fosters"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        foster_data = cur.fetchall()

        # query to show available pets
        query4 = """SELECT Pets.pet_id, Shelters.name AS Shelter, Fosters.name AS Foster, type AS Type, weight AS Weight, is_kid_friendly AS KidFriendly, 
        Pets.name AS Name, age AS Age, breed AS Breed, gender AS Gender, is_adopted AS Adopted FROM Pets 
        JOIN Shelters ON Pets.shelter_id = Shelters.shelter_id 
        LEFT JOIN Fosters ON Pets.foster_id = Fosters.foster_id
        WHERE Pets.is_adopted = 0"""
        cur = mysql.connection.cursor()
        cur.execute(query4)
        available_data = cur.fetchall()

        # query to get adopted pets
        query5 = """SELECT Pets.pet_id, Shelters.name AS Shelter, Fosters.name AS Foster, type AS Type, weight AS Weight, is_kid_friendly AS KidFriendly, 
        Pets.name AS Name, age AS Age, breed AS Breed, gender AS Gender, is_adopted AS Adopted FROM Pets 
        JOIN Shelters ON Pets.shelter_id = Shelters.shelter_id 
        LEFT JOIN Fosters ON Pets.foster_id = Fosters.foster_id
        WHERE Pets.is_adopted = 1"""
        cur = mysql.connection.cursor()
        cur.execute(query5)
        adopted_data = cur.fetchall()

        return render_template("pets.j2", data=data, shelter_data=shelter_data, foster_data=foster_data, available_data=available_data, adopted_data=adopted_data)

    if request.method == "POST":
        if request.form.get("Add_Pet"):
            shelter_id = request.form["shelter"]
            foster_id = request.form["foster"]
            type = request.form["type"]
            weight = request.form["weight"]
            is_kid_friendly = request.form["is_kid_friendly"]
            name = request.form["name"]
            age = request.form["age"]
            breed = request.form["breed"]
            gender = request.form["gender"]
            is_adopted = 0

            # if pet does not have a foster
            if foster_id == "0":
                query = "INSERT INTO Pets (shelter_id, type, weight, is_kid_friendly, name, age, breed, gender, is_adopted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (shelter_id, type, weight,
                            is_kid_friendly, name, age, breed, gender, is_adopted))
                mysql.connection.commit()
            
            # if pet does not have breed
            elif breed == "":
                query = "INSERT INTO Pets (shelter_id, foster_id, type, weight, is_kid_friendly, name, age, gender, is_adopted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (shelter_id, foster_id, type, weight,
                            is_kid_friendly, name, age, gender, is_adopted))
                mysql.connection.commit()
            

            else:
                query = "INSERT INTO Pets (shelter_id, foster_id, type, weight, is_kid_friendly, name, age, breed, gender, is_adopted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (shelter_id, foster_id, type, weight,
                            is_kid_friendly, name, age, breed, gender, is_adopted))
                mysql.connection.commit()

        return redirect("/pets")


@app.route('/delete_pet/<int:pet_id>')
def delete_pet(pet_id):
    query = "DELETE FROM Pets WHERE pet_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (pet_id,))
    mysql.connection.commit()

    return redirect("/pets")


@app.route('/edit_pet/<int:pet_id>', methods=["POST", "GET"])
def edit_pet(pet_id):
    if request.method == "GET":
        query = "SELECT Pets.pet_id, Shelters.name AS Shelter, Fosters.name AS Foster, type AS Type, weight AS Weight, is_kid_friendly AS KidFriendly, Pets.name AS Name, age AS Age, breed AS Breed, gender AS Gender, is_adopted AS Adopted FROM Pets JOIN Shelters ON Pets.shelter_id = Shelters.shelter_id LEFT JOIN Fosters ON Pets.foster_id = Fosters.foster_id WHERE pet_id = %s" % (
            pet_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # query to get shelters and their id for dropdown in edit page
        query2 = "SELECT Shelters.shelter_id, CONCAT(Shelters.name, ', ID: ', Shelters.shelter_id) as Shelter FROM Shelters ORDER BY Shelters.name ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        shelter_data = cur.fetchall()

        # query to get fosters and their id for dropdown in edit page
        query3 = "SELECT Fosters.foster_id, CONCAT(Fosters.name, ', ID: ', Fosters.foster_id ) as Foster FROM Fosters"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        foster_data = cur.fetchall()

        # query to get unaliased data for edit page
        query4 = "SELECT * FROM Pets WHERE pet_id = %s" % (pet_id)
        cur = mysql.connection.cursor()
        cur.execute(query4)
        id_data = cur.fetchall()

        return render_template("edit_pet.j2", data=data, shelter_data=shelter_data, foster_data=foster_data, id_data=id_data)

    if request.method == "POST":
        if request.form.get("Edit_Pet"):
            pet_id = request.form["pet_id"]
            shelter_id = request.form["shelter"]
            foster_id = request.form["foster"]
            type = request.form["type"]
            weight = request.form["weight"]
            is_kid_friendly = request.form["is_kid_friendly"]
            name = request.form["name"]
            age = request.form["age"]
            breed = request.form["breed"]
            gender = request.form["gender"]
            

            # edit pet if pet doesn't have a foster
            if foster_id == "0":
                query = "UPDATE Pets SET Pets.shelter_id = %s, Pets.foster_id = NULL, type = %s, weight = %s, is_kid_friendly = %s, Pets.name = %s, age = %s, breed = %s, gender = %s WHERE Pets.pet_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (shelter_id, type, weight, is_kid_friendly,
                            name, age, breed, gender, pet_id))
                mysql.connection.commit()
            
            # edit pet if pet doesn't have a breed
            elif breed == "":
                query = "UPDATE Pets SET Pets.shelter_id = %s, Pets.foster_id = %s, type = %s, weight = %s, is_kid_friendly = %s, Pets.name = %s, age = %s, breed = NULL, gender = %s WHERE Pets.pet_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (shelter_id, foster_id, type, weight,
                            is_kid_friendly, name, age, gender))
                mysql.connection.commit()

            else:
                query = "UPDATE Pets SET Pets.shelter_id = %s, Pets.foster_id = %s, type = %s, weight = %s, is_kid_friendly = %s, Pets.name = %s, age = %s, breed = %s, gender = %s WHERE Pets.pet_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (shelter_id, foster_id, type, weight,
                            is_kid_friendly, name, age, breed, gender, pet_id))
                mysql.connection.commit()

            return redirect("/pets")


# Adopters page routes
@app.route('/adopters', methods=["POST", "GET"])
def adopters():
    if request.method == "POST":
        if request.form.get("Add_Adopter"):
            first_name = request.form["adopter_fname"]
            last_name = request.form["adopter_lname"]
            phone_number = request.form["adopter_phone"]
            email = request.form["adopter_email"]
            city = request.form["adopter_city"]
            state = request.form["adopter_state"]
            number_of_pets = request.form["number_of_pets"]
            has_kid = request.form["has_kid"]
            looking_for = request.form["looking_for"]

            query = "INSERT INTO Adopters (first_name, last_name, phone_number, email, city, state, number_of_pets, has_kid, looking_for) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

            cur = mysql.connection.cursor()
            cur.execute(query, (first_name, last_name, phone_number,
                        email, city, state, number_of_pets, has_kid, looking_for))
            mysql.connection.commit()

        return redirect("/adopters")

    if request.method == "GET":
        query = "SELECT * FROM Adopters"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

    return render_template("adopters.j2", data=data)

# edit an adopter


@app.route("/edit_adopter/<int:adopter_id>", methods=["POST", "GET"])
def edit_adopter(adopter_id):
    if request.method == "GET":
        query = "SELECT * FROM Adopters WHERE adopter_id = %s" % (adopter_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_adopter.j2", data=data)

    if request.method == "POST":
        if request.form.get("Edit_Adopter"):
            first_name = request.form["adopter_fname"]
            last_name = request.form["adopter_lname"]
            phone_number = request.form["adopter_phone"]
            email = request.form["adopter_email"]
            city = request.form["adopter_city"]
            state = request.form["adopter_state"]
            number_of_pets = request.form["number_of_pets"]
            has_kid = request.form["has_kid"]
            looking_for = request.form["looking_for"]

        query = "UPDATE Adopters SET Adopters.first_name = %s, Adopters.last_name = %s,Adopters.phone_number = %s, Adopters.email = %s, Adopters.city = %s, Adopters.state = %s, Adopters.number_of_pets = %s, Adopters.has_kid = %s, Adopters.looking_for = %s WHERE Adopters.adopter_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (first_name, last_name, phone_number, email,
                    city, state, number_of_pets, has_kid, looking_for, adopter_id))
        mysql.connection.commit()

        return redirect("/adopters")

# delete an adopter


@app.route("/delete_adopter/<int:adopter_id>")
def delete_adopter(adopter_id):

    query = "DELETE FROM Adopters WHERE adopter_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (adopter_id,))
    mysql.connection.commit()

    return redirect("/adopters")

# Fosters page routes

# Read and Create Routes


@app.route('/fosters', methods=["POST", "GET"])
def fosters():
    if request.method == "POST":
        if request.form.get("Add_Foster"):
            city = request.form["foster_city"]
            state = request.form["foster_state"]
            phone_number = request.form["foster_phone"]
            name = request.form["foster_name"]

            query = "INSERT INTO Fosters (city, state, phone_number, name) VALUES (%s, %s, %s, %s)"

            cur = mysql.connection.cursor()
            cur.execute(query, (city, state, phone_number, name))
            mysql.connection.commit()

        return redirect("/fosters")

    if request.method == "GET":
        query = "SELECT * FROM Fosters"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

    return render_template("fosters.j2", data=data)

# edit a foster


@app.route("/edit_foster/<int:foster_id>", methods=["POST", "GET"])
def edit_foster(foster_id):
    if request.method == "GET":
        query = "SELECT * FROM Fosters WHERE foster_id = %s" % (foster_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_foster.j2", data=data)

    if request.method == "POST":
        if request.form.get("Edit_Foster"):
            foster_id = request.form["foster_id"]
            city = request.form["foster_city"]
            state = request.form["foster_state"]
            phone_number = request.form["foster_phone"]
            name = request.form["foster_name"]

            query = "UPDATE Fosters SET Fosters.city = %s, Fosters.state = %s, Fosters.phone_number = %s, Fosters.name = %s WHERE Fosters.foster_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (city, state, phone_number, name, foster_id))
            mysql.connection.commit()

            return redirect("/fosters")

# delete a foster


@app.route("/delete_foster/<int:foster_id>")
def delete_foster(foster_id):

    query = "DELETE FROM Fosters WHERE foster_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (foster_id,))
    mysql.connection.commit()

    return redirect("/fosters")

# Shelters page routes


@app.route('/shelters', methods=["POST", "GET"])
def shelters():
    if request.method == "POST":
        if request.form.get("Add_Shelter"):
            city = request.form["shelter_city"]
            state = request.form["shelter_state"]
            phone = request.form["shelter_phone"]
            name = request.form["shelter_name"]

            query = "INSERT INTO Shelters (city, state, phone_number, name) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (city, state, phone, name))
            mysql.connection.commit()

        return redirect("/shelters")

    # automatically count number of pets in shelter and number of pets in foster home associated with shelter
    if request.method == "GET":
        query = """SELECT Shelters.shelter_id, Shelters.city, Shelters.state, Shelters.phone_number, Shelters.name, 
        COUNT(Pets.pet_id) AS number_of_pets,
        COUNT(case when Pets.foster_id then 1 else null end) AS number_of_pets_foster FROM Shelters
        LEFT JOIN Pets ON Pets.shelter_id = Shelters.shelter_id
        GROUP BY shelter_id"""
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

    return render_template("shelters.j2", data=data)

# edit a shelter


@app.route("/edit_shelter/<int:shelter_id>", methods=["POST", "GET"])
def edit_shelter(shelter_id):
    if request.method == "GET":
        query = "SELECT * FROM Shelters WHERE shelter_id = %s" % (shelter_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_shelter.j2", data=data)

    if request.method == "POST":
        if request.form.get("Edit_Shelter"):
            shelter_id = request.form["shelter_id"]
            city = request.form["shelter_city"]
            state = request.form["shelter_state"]
            phone_number = request.form["shelter_phone"]
            name = request.form["shelter_name"]

            query = "UPDATE Shelters SET Shelters.city = %s, Shelters.state = %s, Shelters.phone_number = %s, Shelters.name = %s WHERE Shelters.shelter_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (city, state, phone_number, name, shelter_id))
            mysql.connection.commit()

            return redirect("/shelters")

# delete a shelter


@app.route("/delete_shelter/<int:shelter_id>")
def delete_shelter(shelter_id):

    query = "DELETE FROM Shelters WHERE shelter_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (shelter_id,))
    mysql.connection.commit()

    return redirect("/shelters")

# Foster-shelters page routes


@app.route('/foster_shelters', methods=["POST", "GET"])
def foster_shelters():
    if request.method == "GET":
        query = """SELECT foster_shelter_id, Shelters.name AS Shelter, Fosters.name AS Foster FROM Foster_shelters 
        JOIN Shelters ON Foster_shelters.shelter_id = Shelters.shelter_id 
        JOIN Fosters ON Foster_shelters.foster_id = Fosters.foster_id ORDER BY Shelters.name ASC"""
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # query to get shelter and shelter id for dropdown
        query2 = "SELECT Shelters.shelter_id, CONCAT(Shelters.name, ',ID: ', Shelters.shelter_id) AS Shelter FROM Shelters ORDER BY Shelters.name ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        shelter_data = cur.fetchall()

        # query to get foster and foster id for dropdown
        query3 = "SELECT Fosters.foster_id, CONCAT(Fosters.name, ', ID: ', Fosters.foster_id ) as Foster FROM Fosters"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        foster_data = cur.fetchall()

        return render_template("foster_shelters.j2", data=data, shelter_data=shelter_data, foster_data=foster_data)

    if request.method == "POST":
        if request.form.get("Add_Foster_Shelter"):
            shelter_id = request.form["shelter"]
            foster_id = request.form["foster"]

            # checks to see if foster shelter relationship already exists, only adds if it doesn't (avoids duplicates)
            query_check = "SELECT * FROM Foster_shelters WHERE Foster_shelters.shelter_id = %s AND Foster_shelters.foster_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query_check, (shelter_id, foster_id))
            foster_shelter = cur.fetchall()

            if len(foster_shelter) == 0:
                query = "INSERT INTO Foster_shelters (shelter_id, foster_id) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (shelter_id, foster_id))
                mysql.connection.commit()

        return redirect("/foster_shelters")


@app.route('/delete_foster_shelter/<int:foster_shelter_id>')
def delete_foster_shelter(foster_shelter_id):
    query = "DELETE FROM Foster_shelters WHERE foster_shelter_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (foster_shelter_id,))
    mysql.connection.commit()

    return redirect("/foster_shelters")


@app.route('/edit_foster_shelter/<int:foster_shelter_id>', methods=["POST", "GET"])
def edit_foster_shelter(foster_shelter_id):
    if request.method == "GET":
        query = """SELECT foster_shelter_id, Shelters.name AS Shelter, Fosters.name AS Foster FROM Foster_shelters 
        JOIN Shelters ON Foster_shelters.shelter_id = Shelters.shelter_id 
        JOIN Fosters ON Foster_shelters.foster_id = Fosters.foster_id WHERE foster_shelter_id = %s ORDER BY Shelters.name ASC """ % (foster_shelter_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # query to get shelter and shelter id for dropdown
        query2 = "SELECT Shelters.shelter_id, CONCAT(Shelters.name, ', ID: ', Shelters.shelter_id) as Shelter FROM Shelters ORDER BY Shelters.name ASC"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        shelter_data = cur.fetchall()

        # query to get foster and foster id for dropdown
        query3 = "SELECT Fosters.foster_id, CONCAT(Fosters.name, ', ID: ', Fosters.foster_id ) as Foster FROM Fosters"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        foster_data = cur.fetchall()

        query4 = "SELECT * FROM Foster_shelters WHERE foster_shelter_id = %s" % (
            foster_shelter_id)
        cur = mysql.connection.cursor()
        cur.execute(query4)
        id_data = cur.fetchall()

        return render_template("edit_foster_shelter.j2", data=data, shelter_data=shelter_data, foster_data=foster_data, id_data=id_data)

    if request.method == "POST":
        if request.form.get("Edit_Foster_Shelter"):
            foster_shelter_id = request.form["foster_shelter_id"]
            shelter_id = request.form["shelter"]
            foster_id = request.form["foster"]

            # checks to see if foster shelter relationship already exists, only allows edit if it doesn't (avoids duplicates)
            query_check = "SELECT * FROM Foster_shelters WHERE Foster_shelters.shelter_id = %s AND Foster_shelters.foster_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query_check, (shelter_id, foster_id))
            foster_shelter = cur.fetchall()

            if len(foster_shelter) == 0:
                query = "UPDATE Foster_shelters SET Foster_shelters.shelter_id = %s, Foster_shelters.foster_id = %s WHERE Foster_shelters.foster_shelter_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (shelter_id, foster_id, foster_shelter_id))
                mysql.connection.commit()

            return redirect("/foster_shelters")


# adoption records page routes
@app.route('/adoption_records', methods=["GET", "POST"])
def adoption_records():
    if request.method == "GET":
        query = """SELECT Adoption_records.adoption_num, CONCAT(Adopters.first_name, ' ', Adopters.last_name) AS Adopter, CONCAT(Pets.type, ', ', 'Name: ', Pets.name) AS Pet,
        Adoption_records.date AS Date, Adoption_records.was_returned AS Returned FROM Adoption_records 
        JOIN Adopters ON Adoption_records.adopter_id = Adopters.adopter_id 
        JOIN Pets ON Adoption_records.pet_id = Pets.pet_id"""
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # query to get adopter full name and id for display
        query2 = """SELECT Adopters.adopter_id, CONCAT(Adopters.first_name, ' ', Adopters.last_name, ', ID: ', Adopters.adopter_id) as Adopter FROM Adopters 
        ORDER BY CONCAT(Adopters.last_name, Adopters.first_name) ASC"""
        cur = mysql.connection.cursor()
        cur.execute(query2)
        adopter_data = cur.fetchall()

        # query to get pet type, name, and id for display
        query3 = """SELECT Pets.pet_id, CONCAT(Pets.type, ', ', 'Name: ', Pets.name, ', ID: ', Pets.pet_id ) as Pet from Pets
        ORDER BY Pets.type ASC"""
        cur = mysql.connection.cursor()
        cur.execute(query3)
        pet_data = cur.fetchall()

        return render_template("adoption_records.j2", data=data, adopter_data=adopter_data, pet_data=pet_data)

    if request.method == "POST":
        if request.form.get("Add_Adoption_Record"):
            adopter_id = request.form["adopter"]
            pet_id = request.form["pet"]
            date = request.form["adoption_date"]
            was_returned = request.form["returned"]
            adopted = 1
            returned = 0

            # check if pet already has adoption records, set previous records to returned
            query_check = "SELECT * FROM Adoption_records WHERE Adoption_records.pet_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query_check, (pet_id,))
            pet_records = cur.fetchall()

            if len(pet_records) > 0:
                query = "UPDATE Adoption_records SET Adoption_records.was_returned = 1 WHERE Adoption_records.pet_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (pet_id,))
                mysql.connection.commit()

            # if pet was adopted (not returned) update Pets.is_adopted (true)
            if was_returned == "0":
                query = "UPDATE Pets SET Pets.is_adopted = %s WHERE Pets.pet_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (adopted, pet_id))
                mysql.connection.commit()
            
            # if pet was returned, update Pets.is_adopted (false)
            elif was_returned == "1":
                query = "UPDATE Pets SET Pets.is_adopted = %s WHERE Pets.pet_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (returned, pet_id))
                mysql.connection.commit()

            query = "INSERT INTO Adoption_records (pet_id, adopter_id, date, was_returned) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (pet_id, adopter_id, date, was_returned))
            mysql.connection.commit()

        return redirect("/adoption_records")


@app.route('/delete_adoption_record/<int:adoption_num>')
def delete_adoption_record(adoption_num):
    query = "DELETE FROM Adoption_records WHERE adoption_num = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (adoption_num,))
    mysql.connection.commit()

    return redirect("/adoption_records")


@app.route('/edit_adoption_record/<int:adoption_num>', methods=["POST", "GET"])
def edit_adoption_record(adoption_num):
    if request.method == "GET":
        query = """SELECT Adoption_records.adoption_num, CONCAT(Adopters.first_name, ' ', Adopters.last_name) AS Adopter, CONCAT(Pets.type, ', ', 'Name: ', Pets.name) AS Pet, 
        Adoption_records.date AS Date, Adoption_records.was_returned AS Returned FROM Adoption_records 
        JOIN Adopters ON Adoption_records.adopter_id = Adopters.adopter_id 
        JOIN Pets ON Adoption_records.pet_id = Pets.pet_id WHERE adoption_num = %s""" % (adoption_num)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # query to get adopter info for dropdown
        query2 = """SELECT Adopters.adopter_id, CONCAT(Adopters.first_name, ' ', Adopters.last_name, ', ID: ', Adopters.adopter_id) as Adopter FROM Adopters 
        ORDER BY CONCAT(Adopters.last_name, Adopters.first_name) ASC"""
        cur = mysql.connection.cursor()
        cur.execute(query2)
        adopter_data = cur.fetchall()

        # query to get pet info for dropdown
        query3 = """SELECT Pets.pet_id, CONCAT(Pets.type, ', ', 'Name: ', Pets.name, ', ID: ', Pets.pet_id ) as Pet from Pets
        ORDER BY Pets.type ASC"""
        cur = mysql.connection.cursor()
        cur.execute(query3)
        pet_data = cur.fetchall()

        query4 = "SELECT * FROM Adoption_records WHERE adoption_num = %s" % (
            adoption_num)
        cur = mysql.connection.cursor()
        cur.execute(query4)
        id_data = cur.fetchall()

        return render_template("edit_adoption_record.j2", data=data, adopter_data=adopter_data, pet_data=pet_data, id_data=id_data)

    if request.method == "POST":
        if request.form.get("Edit_Adoption_Record"):
            adoption_num = request.form["adoption_num"]
            adopter_id = request.form["adopter"]
            pet_id = request.form["pet"]
            date = request.form["adoption_date"]
            was_returned = request.form["returned"]
            adopted = 1
            returned = 0

            # if pet adopted, update pet availability status on pets page
            if was_returned == "0":
                query = "UPDATE Pets SET Pets.is_adopted = %s WHERE Pets.pet_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (adopted, pet_id))
                mysql.connection.commit()
            
            # if pet returned, update pet availability status on pets page
            elif was_returned == "1":
                query = "UPDATE Pets SET Pets.is_adopted = %s WHERE Pets.pet_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (returned, pet_id))
                mysql.connection.commit()

            query = """UPDATE Adoption_records SET Adoption_records.adopter_id = %s, Adoption_records.pet_id = %s, Adoption_records.date = %s, 
            Adoption_records.was_returned = %s WHERE Adoption_records.adoption_num = %s"""
            cur = mysql.connection.cursor()
            cur.execute(query, (adopter_id, pet_id, date,
                        was_returned, adoption_num))
            mysql.connection.commit()

            return redirect("/adoption_records")

# Listener


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 6968))
    app.run(port=port, debug=True)
