from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Veritabanı bağlantısı için yardımcı fonksiyon
def get_db_connection():
    conn = sqlite3.connect('gym_management_system.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        # Form verilerini al
        name = request.form['name']
        gender = request.form['gender']
        contact_number = request.form['contact_number']
        joining_date = request.form['joining_date']
        date_of_birth = request.form['date_of_birth']
        membership_type = request.form['membership_type']
        emergency_contact_name = request.form['emergency_contact_name']
        emergency_contact_number = request.form['emergency_contact_number']

        # Veritabanına ekle
        conn = sqlite3.connect('gym_management_system.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Members (name, gender, joining_date, contact_number, date_of_birth, membership_type, emergency_contact_name, emergency_contact_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, gender, joining_date, contact_number, date_of_birth, membership_type, emergency_contact_name, emergency_contact_number))
        conn.commit()
        conn.close()

        # Listeleme sayfasına yönlendir
        return redirect(url_for('view_members'))

    # Sayfa ilk kez GET ile açılırsa formu göster
    return render_template('add_member.html')
@app.route('/delete_member/<int:member_id>', methods=['POST'])
def delete_member(member_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Members WHERE member_id = ?', (member_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_members'))

@app.route('/edit_member/<int:member_id>', methods=['GET', 'POST'])
def edit_member(member_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # Formdan gelen değerleri al
        name = request.form['name']
        gender = request.form['gender']
        joining_date = request.form['joining_date']
        contact_number = request.form['contact_number']
        date_of_birth = request.form['date_of_birth']
        membership_type = request.form['membership_type']
        emergency_contact_name = request.form['emergency_contact_name']
        emergency_contact_number = request.form['emergency_contact_number']

        # Veriyi güncelle
        cursor.execute('''
            UPDATE Members 
            SET name = ?, gender = ?, joining_date = ?, contact_number = ?, 
                date_of_birth = ?, membership_type = ?, emergency_contact_name = ?, 
                emergency_contact_number = ?
            WHERE member_id = ?
        ''', (name, gender, joining_date, contact_number, date_of_birth,
              membership_type, emergency_contact_name, emergency_contact_number, member_id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_members'))
    
    # GET isteği ile mevcut veriyi çek
    cursor.execute('SELECT * FROM Members WHERE member_id = ?', (member_id,))
    member = cursor.fetchone()
    conn.close()
    return render_template('edit_member.html', member=member)


@app.route('/view_members')
def view_members():
    conn = sqlite3.connect('gym_management_system.db')
    conn.row_factory = sqlite3.Row  # Satırları sözlük olarak döndürür
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Members")  # Tüm sütunları getir
    members = cursor.fetchall()
    conn.close()
    return render_template('view_members.html', members=members)

@app.route('/search_members', methods=['GET'])
def search_members():
    query = request.args.get('query')  # Arama sorgusunu al
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Members WHERE name LIKE ? OR membership_type LIKE ?", (f"%{query}%", f"%{query}%"))
    members = cursor.fetchall()
    conn.close()
    return render_template('view_members.html', members=members)
@app.route('/view_trainers')
def view_trainers():
    conn = sqlite3.connect('gym_management_system.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Trainers')
    trainers = cursor.fetchall()
    conn.close()
    return render_template('view_trainers.html', trainers=trainers)
@app.route('/view_workouts')
def view_workouts():
    conn = sqlite3.connect('gym_management_system.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Workout_Routines')
    workouts = cursor.fetchall()
    conn.close()
    return render_template('view_workouts.html', workouts=workouts)
@app.route('/view_equipment')
def view_equipment():
    conn = sqlite3.connect('gym_management_system.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Gym_Equipment')
    equipment = cursor.fetchall()
    conn.close()
    return render_template('view_equipment.html', equipment=equipment)
@app.route('/search_equipment', methods=['GET'])
def search_equipment():
    query = request.args.get('query')
    conn = sqlite3.connect('gym_management_system.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Gym_Equipment WHERE name LIKE ?", (f"%{query}%",))
    equipment = cursor.fetchall()
    conn.close()
    return render_template('view_equipment.html', equipment=equipment)
@app.route('/add_equipment', methods=['GET', 'POST'])
def add_equipment():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        manufacturer = request.form['manufacturer']
        maintenance_date = request.form['maintenance_date']

        conn = sqlite3.connect('gym_management_system.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Gym_Equipment (name, quantity, price, manufacturer, maintenance_date) VALUES (?, ?, ?, ?, ?)',
                       (name, quantity, price, manufacturer, maintenance_date))
        conn.commit()
        conn.close()
        return redirect(url_for('view_equipment'))
    return render_template('add_equipment.html')
@app.route('/edit_equipment/<int:item_id>', methods=['GET', 'POST'])
def edit_equipment(item_id):
    conn = sqlite3.connect('gym_management_system.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        manufacturer = request.form['manufacturer']
        maintenance_date = request.form['maintenance_date']

        cursor.execute('''
            UPDATE Gym_Equipment 
            SET name = ?, quantity = ?, price = ?, manufacturer = ?, maintenance_date = ?
            WHERE item_id = ?
        ''', (name, quantity, price, manufacturer, maintenance_date, item_id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_equipment'))

    cursor.execute('SELECT * FROM Gym_Equipment WHERE item_id = ?', (item_id,))
    equipment = cursor.fetchone()
    conn.close()
    return render_template('edit_equipment.html', equipment=equipment)
@app.route('/delete_equipment/<int:item_id>', methods=['POST'])
def delete_equipment(item_id):
    conn = sqlite3.connect('gym_management_system.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Gym_Equipment WHERE item_id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_equipment'))
@app.route('/add_workout', methods=['GET', 'POST'])
def add_workout():
    if request.method == 'POST':
        routine_name = request.form['routine_name']
        description = request.form['description']
        duration = request.form['duration']
        difficulty_level = request.form['difficulty_level']

        conn = sqlite3.connect('gym_management_system.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Workout_Routines (routine_name, description, duration, difficulty_level) VALUES (?, ?, ?, ?)',
                       (routine_name, description, duration, difficulty_level))
        conn.commit()
        conn.close()
        return redirect(url_for('view_workouts'))
    return render_template('add_workout.html')
@app.route('/edit_workout/<int:routine_id>', methods=['GET', 'POST'])
def edit_workout(routine_id):
    conn = sqlite3.connect('gym_management_system.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == 'POST':
        routine_name = request.form['routine_name']
        description = request.form['description']
        duration = request.form['duration']
        difficulty_level = request.form['difficulty_level']

        cursor.execute('''
            UPDATE Workout_Routines 
            SET routine_name = ?, description = ?, duration = ?, difficulty_level = ?
            WHERE routine_id = ?
        ''', (routine_name, description, duration, difficulty_level, routine_id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_workouts'))

    cursor.execute('SELECT * FROM Workout_Routines WHERE routine_id = ?', (routine_id,))
    workout = cursor.fetchone()
    conn.close()
    return render_template('edit_workout.html', workout=workout)
@app.route('/delete_workout/<int:routine_id>', methods=['POST'])
def delete_workout(routine_id):
    conn = sqlite3.connect('gym_management_system.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Workout_Routines WHERE routine_id = ?', (routine_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_workouts'))
@app.route('/search_workouts', methods=['GET'])
def search_workouts():
    query = request.args.get('query')  # Kullanıcıdan gelen arama sorgusunu al
    conn = sqlite3.connect('gym_management_system.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Arama sorgusu: workout ismi veya açıklamasında geçen değerleri bul
    cursor.execute("""
        SELECT * FROM Workout_Routines 
        WHERE routine_name LIKE ? OR description LIKE ?
    """, (f"%{query}%", f"%{query}%"))
    
    workouts = cursor.fetchall()
    conn.close()
    
    # Sonuçları view_workouts.html şablonuna gönder
    return render_template('view_workouts.html', workouts=workouts)
@app.route('/search_trainers', methods=['GET'])
def search_trainers():
    query = request.args.get('query')
    conn = sqlite3.connect('gym_management_system.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM Trainers 
        WHERE name LIKE ? OR role LIKE ?
    """, (f"%{query}%", f"%{query}%"))
    trainers = cursor.fetchall()
    conn.close()
    return render_template('view_trainers.html', trainers=trainers)
@app.route('/add_trainer', methods=['GET', 'POST'])
def add_trainer():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        contact_number = request.form['contact_number']
        role = request.form['role']
        experience = request.form['experience']
        specialty = request.form['specialty']

        conn = sqlite3.connect('gym_management_system.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Trainers (name, gender, contact_number, role, experience, specialty) VALUES (?, ?, ?, ?, ?, ?)',
                       (name, gender, contact_number, role, experience, specialty))
        conn.commit()
        conn.close()
        return redirect(url_for('view_trainers'))
    return render_template('add_trainer.html')
@app.route('/edit_trainer/<int:trainer_id>', methods=['GET', 'POST'])
def edit_trainer(trainer_id):
    conn = sqlite3.connect('gym_management_system.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        contact_number = request.form['contact_number']
        role = request.form['role']
        experience = request.form['experience']
        specialty = request.form['specialty']

        cursor.execute('''
            UPDATE Trainers 
            SET name = ?, gender = ?, contact_number = ?, role = ?, experience = ?, specialty = ?
            WHERE trainer_id = ?
        ''', (name, gender, contact_number, role, experience, specialty, trainer_id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_trainers'))

    cursor.execute('SELECT * FROM Trainers WHERE trainer_id = ?', (trainer_id,))
    trainer = cursor.fetchone()
    conn.close()
    return render_template('edit_trainer.html', trainer=trainer)
@app.route('/delete_trainer/<int:trainer_id>', methods=['POST'])
def delete_trainer(trainer_id):
    conn = sqlite3.connect('gym_management_system.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Trainers WHERE trainer_id = ?', (trainer_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_trainers'))







if __name__ == '__main__':
    app.run(debug=True)
