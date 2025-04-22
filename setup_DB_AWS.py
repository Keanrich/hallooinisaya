import mysql.connector

conn = mysql.connector.connect(
    host="database-1-ken.cnywe662esx7.us-east-1.rds.amazonaws.com",
    user="admin",
    password="Smart321!!"
)
cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS carrental")
cursor.execute("CREATE DATABASE carrental")
cursor.execute("USE carrental")

#USER TABLE
cursor.execute('''
    CREATE TABLE user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nama_asli VARCHAR(255),
        password VARCHAR(255),
        email VARCHAR(255),
        date_of_birth DATE,
        sim_nomor VARCHAR(50),
        mode ENUM('admin', 'user'),
        biography TEXT
    )
''')

#CAR TABLE
cursor.execute('''
    CREATE TABLE mobil (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nomor_plat VARCHAR(50) UNIQUE,
        merek VARCHAR(255),
        availability BOOLEAN,
        jenis VARCHAR(255),
        harga DECIMAL(10,2),
        stnk VARCHAR(50),
        description TEXT,
        filepath VARCHAR(255)
    )
''')

#HISTORY TABLE
cursor.execute('''
    CREATE TABLE history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        nama_asli VARCHAR(255),
        tanggal_peminjaman DATE,
        tanggal_pengembalian DATE,
        status ENUM('rejected', 'pending', 'accepted'),
        FOREIGN KEY (user_id) REFERENCES user(id)
    )
''')

#APPROVAL TABLE
cursor.execute('''
    CREATE TABLE approval (
    approval_id INT AUTO_INCREMENT PRIMARY KEY,
    mode ENUM('rejected', 'accepted', 'pending'),
    mobil_id INT,
    id_user INT,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (mobil_id) REFERENCES mobil(id),
    FOREIGN KEY (id_user) REFERENCES user(id)
    )
''')

#LOG TABLE
cursor.execute('''
    CREATE TABLE log (
    log_id INT AUTO_INCREMENT PRIMARY KEY, 
    user_id INT,
    activity ENUM('add', 'delete', 'update', 'accept', 'reject'),
    date_changed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    obj VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES user(id)
    )
''')

#INSERT DATA USER
cursor.executemany('''
    INSERT INTO user (nama_asli, password, email, date_of_birth, sim_nomor, mode, biography) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
''', [
    ("Budi Santoso", "pass123", "budi@example.com", "1990-05-15", "SIM12345", "user", "Budi Santoso is a responsible and diligent individual who enjoys traveling and discovering new places. Born on May 15, 1990, he has a strong passion for cars and often rents vehicles for his road trips. With a background in logistics, Budi values efficiency and reliability in his daily life."),
    ("Siti Aminah", "secure456", "siti@example.com", "1995-08-22", "SIM67890", "admin", "A dedicated administrator, Siti Aminah is known for her leadership and organizational skills. Born on August 22, 1995, she has a keen eye for detail and ensures smooth operations in any workplace. She enjoys reading and mentoring young professionals in her free time."),
    ("Paulina Devina Wijaya", "adminpass1", "paulina@example.com", "2002-04-10", "SIM98765", "admin", "Paulina is a determined and ambitious individual, born on April 10, 2002. As an administrator, she excels in multitasking and problem-solving. She is passionate about technology and frequently explores new software and tools to improve efficiency."),
    ("Reuben Zachary Susanto", "adminpass2", "reuben@example.com", "1998-12-03", "SIM87654", "admin", "Reuben, born on December 3, 1998, is a tech-savvy administrator with a passion for data management and system optimization. Outside of work, he enjoys playing chess and analyzing business strategies."),
    ("Keanrich Cordana", "adminpass3", "keanrich@example.com", "1996-07-19", "SIM76543", "admin", "Keanrich is a dedicated professional with expertise in administrative management. Born on July 19, 1996, he enjoys tackling complex problems and streamlining processes. During his free time, he engages in photography and outdoor adventures."),
    ("Andi Wijaya", "userpass1", "andi@example.com", "1988-06-12", "SIM10001", "user", "A hardworking individual, Andi Wijaya is known for his reliability and discipline. Born on June 12, 1988, he has a strong background in sales and customer service. He enjoys playing badminton and spending time with his family."),
    ("Rina Kartika", "userpass2", "rina@example.com", "1991-09-25", "SIM10002", "user", "Rina is an enthusiastic and friendly person who enjoys helping others. Born on September 25, 1991, she works in the service industry and has excellent interpersonal skills. She has a passion for baking and often shares her creations with friends."),
    ("Eka Pratama", "userpass3", "eka@example.com", "1985-04-08", "SIM10003", "user", "Eka Pratama, born on April 8, 1985, is a dedicated and hardworking professional with a passion for automobiles. He enjoys working on car modifications and learning about new automotive technologies."),
    ("Dewi Anggraini", "userpass4", "dewi@example.com", "1993-11-30", "SIM10004", "user", "Dewi is a kind and approachable individual, born on November 30, 1993. She has a background in finance and is highly detail-oriented. In her free time, she enjoys gardening and yoga."),
    ("Fajar Nugroho", "userpass5", "fajar@example.com", "1989-07-15", "SIM10005", "user", "Born on July 15, 1989, Fajar is an adventure seeker with a love for road trips. He has experience in project management and is known for his problem-solving skills. He enjoys hiking and exploring nature."),
    ("Hana Fitriani", "userpass6", "hana@example.com", "1996-02-19", "SIM10006", "user", "Hana, born on February 19, 1996, is a cheerful and energetic individual with a background in hospitality. She enjoys meeting new people and creating meaningful connections. In her free time, she practices painting."),
    ("Gilang Saputra", "userpass7", "gilang@example.com", "1990-12-05", "SIM10007", "user", "Gilang is a knowledgeable and hardworking professional, born on December 5, 1990. He has a strong interest in mechanics and frequently works on his own car. He also enjoys traveling and photography."),
    ("Lisa Permata", "userpass8", "lisa@example.com", "1992-08-18", "SIM10008", "user", "Lisa, born on August 18, 1992, is a compassionate and caring person who works in customer service. She loves helping people and always goes the extra mile. She is passionate about music and plays the piano."),
    ("Yusuf Ramadhan", "userpass9", "yusuf@example.com", "1987-03-22", "SIM10009", "user", "Yusuf is a practical and analytical thinker, born on March 22, 1987. With a background in engineering, he enjoys working on technical projects and finding innovative solutions."),
    ("Sari Kusuma", "userpass10", "sari@example.com", "1994-05-10", "SIM10010", "user", "Sari, born on May 10, 1994, is a dedicated professional with a passion for marketing. She loves creative storytelling and enjoys writing in her free time."),
    ("Dimas Rahmat", "userpass11", "dimas@example.com", "1986-07-27", "SIM10011", "user", "Dimas is a reliable and disciplined individual, born on July 27, 1986. He has extensive experience in logistics and operations. During his leisure time, he enjoys fishing and outdoor activities."),
    ("Putri Indah", "userpass12", "putri@example.com", "1995-09-14", "SIM10012", "user", "Putri, born on September 14, 1995, is a warm and charismatic individual with a strong passion for fashion and design. She enjoys creating new clothing styles and staying updated with trends."),
    ("Agus Supriyadi", "userpass13", "agus@example.com", "1990-01-03", "SIM10013", "user", "Agus, born on January 3, 1990, is a skilled technician with a love for fixing things. Whether it's electronics or automobiles, he enjoys solving problems and improving functionality."),
    ("Wulan Sari", "userpass14", "wulan@example.com", "1989-11-17", "SIM10014", "user", "Wulan, born on November 17, 1989, is an empathetic and kind-hearted individual who enjoys working with children. She is an educator who believes in lifelong learning and personal growth."),
    ("Bayu Prasetyo", "userpass15", "bayu@example.com", "1992-06-21", "SIM10015", "user", "Bayu, born on June 21, 1992, is an energetic and passionate individual who loves sports and fitness. He works in the health industry and enjoys motivating others to maintain a healthy lifestyle."),
    ("Nina Cahyani", "userpass16", "nina@example.com", "1988-12-30", "SIM10016", "user", "Nina, born on December 30, 1988, is a detail-oriented and organized person. She has a background in administration and enjoys planning events. She is also an avid reader.")
])

#INSERT DATA CAR
cursor.executemany('''
    INSERT INTO mobil (nomor_plat, merek, availability, jenis, harga, stnk, description, filepath) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
''', [
    ("B1234XYZ", "Toyota Avanza", True, "MPV", 300000.00, "STNK123", "A reliable and spacious MPV, ideal for family trips and daily commutes.", "images/dataset_gambar_mobil/Toyota_Avanza.jpeg"),
    ("D5678ABC", "Honda Civic", False, "Sedan", 500000.00, "STNK456", "A sporty and stylish sedan with excellent fuel efficiency and performance.", "images/dataset_gambar_mobil/Honda_Civic.jpeg"),
    ("F9101DEF", "Suzuki Ertiga", True, "MPV", 350000.00, "STNK789", "A practical MPV with a comfortable cabin and smooth driving experience.", "images/dataset_gambar_mobil/Suzuki_Ertiga.jpeg"),
    ("G2345GHI", "Mitsubishi Xpander", True, "MPV", 375000.00, "STNK012", "A modern MPV with stylish design and great safety features.", "images/dataset_gambar_mobil/Mitsubishi_Xpander.jpeg"),
    ("H6789JKL", "Toyota Fortuner", False, "SUV", 700000.00, "STNK345", "A rugged SUV with powerful performance, suitable for all terrains.", "images/dataset_gambar_mobil/Toyota_Fortuner.jpeg"),
    ("J1011MNO", "Honda BR-V", True, "SUV", 400000.00, "STNK678", "A versatile SUV with spacious interiors and efficient fuel consumption.", "images/dataset_gambar_mobil/Honda_BR-V.jpeg"),
    ("K1213PQR", "Nissan Livina", False, "MPV", 320000.00, "STNK901", "A compact MPV with smooth handling and family-friendly features.", "images/dataset_gambar_mobil/Nissan_Livina.jpeg"),
    ("L1415STU", "Daihatsu Terios", True, "SUV", 450000.00, "STNK234", "A budget-friendly SUV with off-road capabilities and a sleek design.", "images/dataset_gambar_mobil/Daihatsu_Terios.jpeg"),
    ("M1617VWX", "Mazda CX-5", False, "SUV", 800000.00, "STNK567", "A premium SUV with sporty handling and luxurious interiors.", "images/dataset_gambar_mobil/Mazda_CX-5.jpeg"),
    ("N1819YZA", "BMW X1", True, "Luxury SUV", 1200000.00, "STNK890", "A stylish and high-performance luxury SUV with cutting-edge technology.", "images/dataset_gambar_mobil/BMW_X1.jpeg"),
    ("P2021BCD", "Mercedes-Benz GLA", False, "Luxury SUV", 1500000.00, "STNK111", "A sophisticated luxury SUV offering a smooth and comfortable ride.", "images/dataset_gambar_mobil/Mercedes-Benz_GLA.jpeg"),
    ("Q2223EFG", "Hyundai Creta", True, "SUV", 375000.00, "STNK222", "A compact SUV with a bold design and advanced safety features.", "images/dataset_gambar_mobil/Hyundai_Creta.jpeg"),
    ("R2425HIJ", "Kia Seltos", False, "SUV", 390000.00, "STNK333", "A stylish and modern SUV with a feature-rich interior.", "images/dataset_gambar_mobil/Kia_Seltos.jpeg"),
    ("S2627KLM", "Ford Everest", True, "SUV", 850000.00, "STNK444", "A robust SUV designed for both urban and off-road adventures.", "images/dataset_gambar_mobil/Ford_Everest.jpeg"),
    ("T2829NOP", "Chevrolet Trailblazer", False, "SUV", 880000.00, "STNK555", "A rugged SUV with excellent towing capacity and powerful performance.", "images/dataset_gambar_mobil/Chevrolet_Trailblazer.jpeg"),
    ("U3031QRS", "Jeep Wrangler", True, "Off-road SUV", 2000000.00, "STNK666", "An iconic off-road SUV with exceptional durability and 4x4 capability.", "images/dataset_gambar_mobil/Jeep_Wrangler.jpeg"),
    ("V3233TUV", "Lexus RX", False, "Luxury SUV", 1800000.00, "STNK777", "A premium luxury SUV with refined interiors and a smooth driving experience.", "images/dataset_gambar_mobil/Lexus_RX.jpeg"),
    ("W3435WXY", "Tesla Model X", True, "Electric SUV", 2500000.00, "STNK888", "A high-tech electric SUV with autopilot features and outstanding range.", "images/dataset_gambar_mobil/Tesla_Model_X.jpeg"),
    ("X3637YZA", "Toyota Alphard", False, "Luxury MPV", 1700000.00, "STNK999", "A premium MPV with plush interiors and advanced entertainment features.", "images/dataset_gambar_mobil/Toyota_Alphard.jpeg"),
    ("Y3839BCD", "Honda CR-V", True, "SUV", 450000.00, "STNK000", "A reliable and fuel-efficient SUV, perfect for city driving and road trips.", "images/dataset_gambar_mobil/Honda_CR-V.jpeg")
])

#INSERT DATA HISTORY
cursor.executemany('''
    INSERT INTO history (user_id, nama_asli, tanggal_peminjaman, tanggal_pengembalian, status) 
    VALUES (%s, %s, %s, %s, %s)
''', [
    (1, "Budi Santoso", "2025-03-10", "2025-03-12", "accepted"),
    (2, "Siti Aminah", "2025-03-15", "2025-03-18", "accepted"),
    (3, "Andi Wijaya", "2025-04-01", "2025-04-05", "accepted"),
    (4, "Rina Kartika", "2025-04-10", "2025-04-12", "rejected"),
    (5, "Eka Pratama", "2025-04-15", "2025-04-18", "accepted"),
    (6, "Dewi Anggraini", "2025-04-20", "2025-04-25", "accepted"),
    (7, "Fajar Nugroho", "2025-05-01", "2025-05-04", "accepted"),
    (8, "Hana Fitriani", "2025-05-10", "2025-05-15", "rejected"),
    (9, "Gilang Saputra", "2025-05-18", "2025-05-20", "accepted"),
    (10, "Lisa Permata", "2025-05-25", "2025-05-30", "rejected"),
    (11, "Yusuf Ramadhan", "2025-06-01", "2025-06-05", "accepted"),
    (12, "Sari Kusuma", "2025-06-10", "2025-06-15", "rejected"),
    (13, "Dimas Rahmat", "2025-06-18", "2025-06-20", "accepted"),
    (14, "Putri Indah", "2025-06-25", "2025-06-28", "rejected"),
    (15, "Agus Supriyadi", "2025-07-01", "2025-07-05", "accepted"),
    (16, "Wulan Sari", "2025-07-10", "2025-07-12", "accepted"),
    (17, "Bayu Prasetyo", "2025-07-15", "2025-07-18", "accepted"),
    (18, "Nina Cahyani", "2025-07-20", "2025-07-22", "rejected"),
    (19, "Bambang Haryanto", "2025-07-25", "2025-07-30", "accepted"),
    (20, "Ratna Sari", "2025-08-01", "2025-08-05", "rejected"),
    (21, "Eko Widodo", "2025-08-10", "2025-08-12", "accepted")
])

# cursor.execute("SELECT * FROM user")
# users = cursor.fetchall()
# print("\nTabel User:")
# for user in users:
#     print(user)

# cursor.execute("SELECT * FROM mobil")
# cars = cursor.fetchall()
# print("\nTabel Mobil:")
# for car in cars:
#     print(car)

# cursor.execute("SELECT * FROM history")
# history = cursor.fetchall()
# print("\nTabel History:")
# for record in history:
#     print(record)

conn.commit()
cursor.close()
conn.close()
