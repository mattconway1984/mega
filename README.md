# mega
My first flask app

# Development Installation:
1. Install development requirements:
11. `pip install -r requirements.txt`
1. Create the Migration Repository.  
11. `flask db init`
1. The First Database Migration
11. `flask db migrate -m "users table"`
11. `flask db upgrade`

# Modifying The Database Models:
If any changes to the database are required, then a new database migration needs to be generated:

1. `flask db migrate -m "<NAME OF TABLE>"
1. `flask db upgrade`
