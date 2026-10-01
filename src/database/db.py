from src.database.config import supabase
import bcrypt

def hash_pass(password):
    # bcrypt.hashpw() returns bytes, and .decode() converts them into a string.
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_pass(password, hashed):
    # Does this password match this hashed password?
    return bcrypt.checkpw(password.encode(), hashed.encode())

def check_teacher_exists(username):
    # Check for unique username, returns false when username is already taken
    res = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(res.data) > 0 # returns boolean

def create_teacher(username, password, name):
    data = {"username": username, "password":hash_pass(password),"name":name}

    res = supabase.table("teachers").insert(data).execute()

    return res.data

def teacher_login(username, password):
    res = supabase.table("teachers").select("*").eq("username",username).execute()

    if res.data:
        teacher = res.data[0]
        if check_pass(password, teacher["password"]):
            return teacher

    return None