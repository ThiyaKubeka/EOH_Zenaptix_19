from pymongo import MongoClient

client = MongoClient('localhost', 27017) 
print(client)
db =client['SSI']
print(db) 
courses =db.courses
print(courses)


Steward = {'name':'steward'}
courses.insert_one(Steward)


Steward =  courses.find_one()

did = Steward['name']

print(Steward)