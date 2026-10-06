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

def get_all_students():
    response = supabase.table('students').select("*").execute()
    return response.data

def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {"name": new_name, "face_embedding": face_embedding, "voice_embedding": voice_embedding}
    res = supabase.table("students").insert(data).execute()
    return res.data

def create_subject(subject_code, name, section, teacher_id):
    data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
    response = supabase.table("subjects").insert(data).execute()
    return response.data

def get_teacher_subjects(teacher_id):
    response = supabase.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects = response.data


    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance_logs', [])
        unique_sessions = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_sessions


        sub.pop('subject_student', None)
        sub.pop('attendance_logs', None)

    return subjects