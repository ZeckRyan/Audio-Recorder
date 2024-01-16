import mysql.connector # Koneksi ke Database MySQL
import os # Interaksi dengan sistem operasi, digunakan untuk operasi file.
import wave # Membaca dan menulis file audio format WAV.
import time  # Fungsi terkait waktu, digunakan untuk mengukur durasi.
import tkinter as tk # Antarmuka Pengguna Grafis (GUI) untuk Python.
import pyaudio # Interaksi dengan aliran audio, digunakan untuk merekam audio.
import threading # Dukungan multi-threading untuk menjalankan proses secara bersamaan.
import tkinter.messagebox as messagebox # Kotak pesan dalam Tkinter, untuk menampilkan peringatan


# Koneksi ke Database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_audiorecorder"
)

# Fungsi ini digunakan untuk menyimpan data suara yang direkam ke dalam file audio WAV
def save_audio_to_file(frames, file_path):
    sound_file = wave.open(file_path, "wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(2)  # 16-bit audio
    sound_file.setframerate(44100)
    sound_file.writeframes(b"".join(frames))
    sound_file.close()

# Kelas ini merupakan kelas dasar untuk halaman dalam aplikasi.
class Page(tk.Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)
        self.configure(bg="#ffcae5")
        self.db = None  # Initialize db to None; it will be set in subclasses

# Kelas ini mewakili halaman utama aplikasi. dan Menampilkan tombol untuk registrasi dan login.
class HomePage(Page):
    def __init__(self, db):
        super().__init__("Voice Recorder App")
        self.geometry("600x700")
        self.db = db

        logo_label = tk.Label(self, text="🎤", font=("Arial", 100), bg="#ffcae5")
        logo_label.pack(pady=25)
        logo_label = tk.Label(self, bg="#ffcae5")
        logo_label.pack(pady=10)

        welcome_label = tk.Label(self, text="Welcome to Voice Recorder App", font=("Arial", 18), bg="#ffcae5")
        welcome_label.pack(pady=10)

        self.register_button = tk.Button(
            self, text="Register", command=self.open_register, bg="#4CAF50", fg="white", font=("Arial", 12)
        )
        self.register_button.pack(pady=10)

        self.login_button = tk.Button(
            self, text="Login", command=self.open_login, bg="#3498db", fg="white", font=("Arial", 12)
        )
        self.login_button.pack(pady=10)

        group_label = tk.Label(self, text="UAS PROJECT", font=("Arial", 10), bg="#ffcae5")
        group_label.pack(pady=10)

    def open_register(self):
        self.destroy()
        RegisterPage(self, self.db)

    def open_login(self):
        self.destroy()
        LoginPage(self, self.db)

# Kelas ini mewakili halaman registrasi. Memiliki fungsi untuk mendaftarkan pengguna baru ke dalam database.
class RegisterPage(Page):
    def __init__(self, parent, db):
        super().__init__("Register")
        self.geometry("600x700")
        self.db = db  # Save the database connection

        self.username_label = tk.Label(self, text="Username:", bg="#ffcae5")
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=10)

        self.password_label = tk.Label(self, text="Password:", bg="#ffcae5")
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=10)

        self.confirm_password_label = tk.Label(self, text="Confirm Password:", bg="#ffcae5")
        self.confirm_password_label.pack(pady=10)
        self.confirm_password_entry = tk.Entry(self, show="*")
        self.confirm_password_entry.pack(pady=10)

        self.register_button = tk.Button(
            self, text="Register", command=self.register, bg="#4CAF50", fg="white", font=("Arial", 12)
        )
        self.register_button.pack(pady=20)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if password != confirm_password:
            messagebox.showwarning("Password Mismatch", "Password and Confirm Password do not match.")
        else:
            cursor = self.db.cursor()
            sql = "INSERT INTO login (username, password) VALUES (%s, %s)"
            val = (username, password, )
            cursor.execute(sql, val)
            self.db.commit()
            self.destroy()
            VoiceRecorder(self, username, password, self.db)

# Kelas ini mewakili halaman login. Memiliki fungsi untuk melakukan login dengan memeriksa kecocokan username dan password dalam database.
class LoginPage(Page):
    def __init__(self, parent, db):
        super().__init__("Login")
        self.geometry("600x700")
        self.db = db

        self.username_label = tk.Label(self, text="Username:", bg="#ffcae5")
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=10)

        self.password_label = tk.Label(self, text="Password:", bg="#ffcae5")
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=10)

        self.login_button = tk.Button(
            self, text="Login", command=self.login, bg="#3498db", fg="white", font=("Arial", 12)
        )
        self.login_button.pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        cursor = self.db.cursor()
        sql = "SELECT * FROM login WHERE username=%s AND password=%s"
        val = (username, password,)
        cursor.execute(sql, val)
        result = cursor.fetchall()

        if result:
            self.destroy()
            VoiceRecorder(self, username, password, self.db)
        else:
            messagebox.showwarning("User Not Found", "Username not found. Please register.")

# Kelas ini mewakili jendela popup yang menampilkan riwayat rekaman suara. Menampilkan daftar rekaman suara pengguna
class RecordingHistoryPopup(tk.Toplevel):
    def __init__(self, parent, history):
        super().__init__(parent)
        self.title("Recording History")
        self.geometry("300x200")
        self.configure(bg="#ffc0cb")

        self.history_label = tk.Label(self, text="Recording History:")
        self.history_label.pack(pady=10)

        self.history_listbox = tk.Listbox(self, selectmode=tk.DISABLED)
        for recording in history:
            self.history_listbox.insert(tk.END, recording[0])  # Assuming recording[0] contains the file_path
        self.history_listbox.pack(pady=10)

        self.back_button = tk.Button(self, text="Back to Recording", command=self.destroy)
        self.back_button.pack(pady=10)

        self.selected_file_path = None  # To store the selected file path

# Fungsi ini mengambil riwayat rekaman suara pengguna dari database.
def get_recording_history(username, db):
    cursor = db.cursor()
    sql = "SELECT file_path FROM audio_recordings WHERE username = %s ORDER BY recording_time DESC"
    val = (username,)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    return result

# Kelas ini merupakan inti dari aplikasi perekaman suara. Menangani proses perekaman suara, penghentian rekaman, penyimpanan file audio, dan menampilkan riwayat rekaman
class VoiceRecorder:
    def __init__(self, parent, username, password, db):
        super().__init__()
        self.parent = parent
        self.username = username
        self.password = password
        self.db = db
        self.root = tk.Tk()
        self.root.resizable(False, False)

        # Set the background color to pink
        self.root.configure(bg="#ffc0cb")
        
        self.button = tk.Button(self.root, text="🎤", font=("Arial", 120, "bold"), command=self.toggle_recording, fg="black", bg="#ffc0cb")
        self.button.pack()

        self.history_button = tk.Button(self.root, text="Recording History", command=self.show_history, bg="#3498db", fg="white")
        self.history_button.pack()

        self.label = tk.Label(self.root, text="00:00:00", fg="black")
        self.label.pack()

        self.recording = False
        self.frames = []
        self.start_time = 0

        self.root.mainloop()

    # Fungsi untuk mengganti status perekaman antara aktif dan tidak aktif.
    def toggle_recording(self):
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording()

    # Fungsi untuk memulai proses perekaman suara.
    def start_recording(self):
        self.recording = True
        self.button.config(fg="red")
        self.start_time = time.time()
        self.frames = []  # Reset frames
        threading.Thread(target=self.record).start()

    # Fungsi untuk menghentikan proses perekaman suara.
    def stop_recording(self):
        self.recording = False
        self.button.config(fg="black")
        self.save_audio()

    # Fungsi yang berjalan dalam thread terpisah untuk merekam data suara.
    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100,
                            input=True, frames_per_buffer=1024)
        try:
            while self.recording:
                data = stream.read(1024)
                self.frames.append(data)

                passed = time.time() - self.start_time
                secs = passed % 60
                mins = passed // 60
                hours = mins // 60

                self.root.after(1000, self.update_label, hours, mins, secs)
        except Exception as e:
            print(f"Error during recording: {e}")
            self.show_error_message(f"An error occurred during recording: {e}")
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()

    # Fungsi untuk memperbarui label waktu pada antarmuka pengguna.
    def update_label(self, hours, mins, secs):
        self.label.config(text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")

    # Fungsi untuk menampilkan pesan kesalahan dalam sebuah dialog.
    def show_error_message(self, message):
        # Use update_idletasks() to run the messagebox in the main thread
        self.root.update_idletasks()
        tk.messagebox.showerror("Recording Error", message)

    # Fungsi untuk menyimpan data suara yang direkam ke dalam file audio WAV.
    def save_audio(self):
        exists = True
        i = 1
        while exists:
            if os.path.exists(f"recording{i}.wav"):
                i += 1
            else:
                exists = False

        file_path = f"recording{i}.wav"
        save_audio_to_file(self.frames, file_path)
    
    # Fungsi untuk menampilkan jendela popup riwayat rekaman suara pengguna.
    def show_history(self):
        history = get_recording_history(self.username, self.db)
        if history:
            RecordingHistoryPopup(self.root, history)
        else:
            messagebox.showinfo("Recording History", "You have no recording history.")

if __name__ == "__main__":
    HomePage(db).mainloop()
