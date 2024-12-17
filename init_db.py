import sqlite3

def init_db():
    conn = sqlite3.connect('gym_management_system.db')
    cursor = conn.cursor()

    # Members tablosu oluştur
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Members (
        member_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        gender TEXT,
        joining_date DATE,
        contact_number TEXT,
        date_of_birth DATE,
        membership_type TEXT,
        emergency_contact_name TEXT,
        emergency_contact_number TEXT
    )
    ''')

    # Trainers tablosu oluştur
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Trainers (
        trainer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        gender TEXT,
        contact_number TEXT,
        role TEXT,
        experience INTEGER,
        specialty TEXT
    )
    ''')

    # Gym Equipment tablosu oluştur
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Gym_Equipment (
        item_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        quantity INTEGER,
        price REAL,
        manufacturer TEXT,
        maintenance_date DATE
    )
    ''')

    # Workout Routines tablosu oluştur
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Workout_Routines (
        routine_id INTEGER PRIMARY KEY,
        routine_name TEXT NOT NULL,
        description TEXT,
        duration INTEGER,
        difficulty_level TEXT
    )
    ''')

    # Örnek veriler ekleme
    members_data = [
        ('John Doe', 'Male', '2023-01-15', '555-1234', '1990-05-20', 'Gold', 'Jane Doe', '555-5678'),
        ('Alice Smith', 'Female', '2023-02-10', '555-2345', '1985-08-12', 'Silver', 'Bob Smith', '555-6789'),
        ('Bob Johnson', 'Male', '2023-03-05', '555-3456', '1992-11-30', 'Platinum', 'Sue Johnson', '555-7890'),
        ('Clara Lee', 'Female', '2023-04-22', '555-4567', '1995-02-25', 'Gold', 'Tom Lee', '555-8901'),
        ('David Brown', 'Male', '2023-05-18', '555-5678', '1988-07-14', 'Silver', 'Lisa Brown', '555-9012'),
        ('Ella White', 'Female', '2023-06-12', '555-6789', '1993-09-19', 'Platinum', 'Mark White', '555-0123'),
        ('Frank Green', 'Male', '2023-07-03', '555-7890', '1991-03-11', 'Gold', 'Nancy Green', '555-1230'),
        ('Grace Hall', 'Female', '2023-08-01', '555-8901', '1987-10-07', 'Silver', 'Henry Hall', '555-2340'),
        ('Harry King', 'Male', '2023-09-09', '555-9012', '1994-01-23', 'Platinum', 'Olivia King', '555-3450'),
        ('Isla Scott', 'Female', '2023-10-15', '555-0123', '1996-06-17', 'Gold', 'Peter Scott', '555-4560')
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO Members (name, gender, joining_date, contact_number, date_of_birth, membership_type, emergency_contact_name, emergency_contact_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', members_data)

    # Trainers tablosu için örnek veri
    trainers_data = [
        ('Mike Ross', 'Male', '555-1010', 'Personal Trainer', 5, 'Weightlifting'),
        ('Rachel Zane', 'Female', '555-2020', 'Group Trainer', 3, 'Yoga')
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO Trainers (name, gender, contact_number, role, experience, specialty)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', trainers_data)

        # Workout Routines örnek veriler
    workouts_data = [
        ('Full Body Workout', 'A comprehensive workout for the whole body', 60, 'Intermediate'),
        ('Cardio Blast', 'High-intensity cardio routine', 45, 'Advanced'),
        ('Strength Training', 'Focus on building muscle strength', 50, 'Beginner'),
        ('Yoga Flow', 'Relaxing yoga sequence', 30, 'Beginner'),
        ('HIIT Session', 'High-Intensity Interval Training', 40, 'Advanced')
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO Workout_Routines (routine_name, description, duration, difficulty_level)
        VALUES (?, ?, ?, ?)
    ''', workouts_data)


    # Gym Equipment tablosu için örnek veri
    equipment_data = [
        ('Treadmill', 5, 1200.00, 'FitCo', '2023-01-01'),
        ('Dumbbell Set', 10, 500.00, 'IronWorks', '2023-02-15')
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO Gym_Equipment (name, quantity, price, manufacturer, maintenance_date)
        VALUES (?, ?, ?, ?, ?)
    ''', equipment_data)

    conn.commit()
    conn.close()
    print("Database initialized and sample data inserted successfully!")

if __name__ == '__main__':
    init_db()

