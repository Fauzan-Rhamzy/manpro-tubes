DROP TABLE IF EXISTS SetoranPusat
DROP TABLE IF EXISTS SetoranMember
DROP TABLE IF EXISTS Pengguna
DROP TABLE IF EXISTS Harga
DROP TABLE IF EXISTS Sampah
DROP TABLE IF EXISTS TPA
DROP TABLE IF EXISTS Kelurahan
DROP TABLE IF EXISTS Kecamatan

-- CREATE TABLE KECAMATAN
CREATE TABLE Kecamatan(
	id_kecamatan INT IDENTITY(1,1) PRIMARY KEY,
	nama VARCHAR(50) UNIQUE NOT NULL,
)

-- CREATE TABLE KELURAHAN
CREATE TABLE Kelurahan(
	id_kelurahan INT IDENTITY(1,1) PRIMARY KEY,
	nama VARCHAR(50) UNIQUE NOT NULL,
	id_kecamatan INT NOT NULL FOREIGN KEY REFERENCES Kecamatan (id_kecamatan)
)

-- CREATE TABLE SAMPAH
CREATE TABLE Sampah(
	id_sampah INT IDENTITY(1,1) PRIMARY KEY,
	nama VARCHAR(50) UNIQUE NOT NULL,
	unit VARCHAR(10) NOT NULL
)

-- CREATE TABLE HARGA
CREATE TABLE Harga(
	id_perubahan INT IDENTITY(1,1) PRIMARY KEY,
	id_sampah INT NOT NULL FOREIGN KEY REFERENCES Sampah (id_sampah),
	harga MONEY NOT NULL,
	tanggal_perubahan DATE NOT NULL
)

-- CREATE TABLE PENGGUNA
CREATE TABLE Pengguna (
	id INT IDENTITY (1,1) PRIMARY KEY,
	nama VARCHAR(50) NOT NULL,
	email VARCHAR(50),
	username VARCHAR(50) UNIQUE NOT NULL,
	password VARCHAR(50) NOT NULL,
	peran VARCHAR(10) NOT NULL,
	no_telp VARCHAR(12) UNIQUE NOT NULL,
	alamat VARCHAR(50) NOT NULL,
	id_kelurahan INT FOREIGN KEY REFERENCES Kelurahan (id_kelurahan)
)

-- CREATE TABLE TPA
CREATE TABLE TPA(
	id_TPA INT IDENTITY(1,1) PRIMARY KEY,
	nama VARCHAR(50) UNIQUE NOT NULL
)

-- CREATE TABLE Setoran Member
CREATE TABLE SetoranMember(
	id_transaksi INT IDENTITY(1,1) PRIMARY KEY,
	id_member INT FOREIGN KEY REFERENCES Pengguna (id),
	id_sampah INT FOREIGN KEY REFERENCES Sampah (id_sampah),
	kuantitas_sampah INT NOT NULL,
	tgl_transaksi DATE NOT NULL
)


-- CREATE TABLE Setoran Pusat
CREATE TABLE SetoranPusat(
	id_transaksi INT IDENTITY(1,1) PRIMARY KEY,
	id_TPA INT FOREIGN KEY REFERENCES TPA (id_TPA),
	id_sampah INT FOREIGN KEY REFERENCES Sampah (id_sampah),
	kuantitas_sampah INT NOT NULL,
	tgl_transaksi DATE NOT NULL
)


--------------- DUMMY DATA ---------------
-- INSERT KECAMATAN
INSERT INTO Kecamatan (nama)
VALUES
	('Andir'),
	('Astana Anyar'),
	('Antapani'),
	('Arcamanik'),
	('Babakan Ciparay'),
	('Bandung Kidul'),
	('Bandung Kulon'),
	('Bandung Wetan'),
	('Batununggal'),
	('Bojongloa Kaler')

-- INSERT KELURAHAN
INSERT INTO Kelurahan (id_kecamatan, nama)
VALUES
	(1, 'Campaka'),
	(1, 'Ciroyom'),
	(1, 'Garuda'),
	(2, 'Cibadak'),
	(2, 'Karanganyar'),
	(2, 'Karasak'),
	(3, 'Antapani Kidul'),
	(3, 'Antapani Kulon'),
	(3, 'Antapani Tengah'),
	(4, 'Cisaranten Endah'),
	(4, 'Cisaranten Kulon'),
	(4, 'Sukamiskin'),
	(5, 'Babakan'),
	(5, 'Babakan Ciparay'),
	(5, 'Cirangrang'),
	(6, 'Batununggal'),
	(6, 'Kujangsari'),
	(6, 'Mengger'),
	(7, 'Caringin'),
	(7, 'Cibuntu'),
	(7, 'Cijerah'),
	(8, 'Cihapit'),
	(8, 'Citarum'),
	(8, 'Tamansari'),
	(9, 'Binong'),
	(9, 'Cibangkong'),
	(9, 'Gumuruh'),
	(10, 'Babakan Asih'),
	(10, 'Babakan Tarogog'),
	(10, 'Kopo')

-- INSERT SAMPAH
INSERT INTO Sampah (nama, unit)
VALUES
	('Botol plastik', 'pc'),
	('Kertas', 'kg'),
	('Botol kaca', 'pc'),
	('Pakaian', 'pc'),
	('Kardus', 'kg')

-- INSERT HARGA
INSERT INTO Harga (id_sampah, harga, tanggal_perubahan)
VALUES
	(1, 500, '20240524'),
	(2, 1000, '20240524'),
	(3, 1000, '20240524'),
	(4, 2500, '20240524'),
	(5, 1250, '20240524')

-- INSERT PENGGUNA
INSERT INTO Pengguna (nama, email, username, password, peran, no_telp, alamat, id_kelurahan)
VALUES
	('Dodo', 'dodo@gmail.com', 'dodoadmin', 'admindodo', 'admin', '081378522999', 'Jl. Dodo Park no. 12', 1),
	('Wombat', 'wombat@gmail.com', 'wombatadmin', 'adminwombat', 'admin', '081203212218', 'Jl. Wombat Jungle no. 1', 2),
	('Cecep Priyatno', 'cecep@gmail.com', 'cecep', 'cecep123', 'member', '082201233142', 'Jl. Cibadak no. 1', 4),
	('Putri Afifah', 'afifahputri@gmail.com', 'afifahputri', 'afput31', 'member', '081278229031', 'Jl. Antapani no. 25', 7),
	('Ros Purnawati', 'roswati@gmail.com', 'ros', 'rospurna80', 'member', '087531202284', 'Jl. Arcamanik Endah no. 2', 10),
	('Bambang Kusumo', 'bambangkusumo@gmail.com', 'bambangk', 'bambangkus03', 'member', '089272011320', 'Jl. Babakan Ciparay no. 200', 14)

-- INSERT TPA
INSERT INTO TPA (nama)
VALUES	
	('Bersih Sejahtera'),
	('EcoHaven'),
	('Highland Recycling'),
	('Bumi Asri'),
	('Cahaya Timur')

-- INSERT SETORAN MEMBER
INSERT SetoranMember (id_member, id_sampah, kuantitas_sampah, tgl_transaksi)
VALUES
	(3, 1, 5, '20240527'),
	(3, 2, 2, '20240527'),
	(3, 3, 5, '20240527'),
	(4, 4, 1, '20240526'),
	(4, 2, 5, '20240526'),
	(5, 5, 2, '20240526')

-- INSERT SETORAN PUSAT
INSERT SetoranPusat (id_TPA, id_sampah, kuantitas_sampah, tgl_transaksi)
VALUES
	(1, 1, 5, '20240529'),
	(2, 2, 5, '20240529'),
	(3, 2, 2, '20240529'),
	(4, 5, 2, '20240529'),
	(5, 3, 5, '20240529')