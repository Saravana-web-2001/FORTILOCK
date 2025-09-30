import random
import hashlib
import tkinter as tk
from tkinter import messagebox
import webbrowser

# ----------------------------
# Matrix Background Canvas
# ----------------------------
class MatrixCanvas(tk.Canvas):
    def __init__(self, parent, width, height, font_size=15):
        super().__init__(parent, width=width, height=height, bg="black", highlightthickness=0)
        self.width = width
        self.height = height
        self.font_size = font_size
        self.columns = int(self.width / self.font_size)
        self.drops = [0 for _ in range(self.columns)]
        self.chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
        self.after(50, self.draw)

    def draw(self):
        self.delete("all")
        for i in range(len(self.drops)):
            char = random.choice(self.chars)
            x = i * self.font_size
            y = self.drops[i] * self.font_size
            self.create_text(x, y, text=char, fill="#00FF00", font=("Courier", self.font_size, "bold"))
            if y > self.height and random.random() > 0.975:
                self.drops[i] = 0
            self.drops[i] += 1
        self.after(50, self.draw)

# ----------------------------
# OTP + Password Authentication
# ----------------------------
class MFAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Login System")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Add Matrix Background
        self.bg_canvas = MatrixCanvas(root, width=600, height=400, font_size=15)
        self.bg_canvas.place(x=0, y=0)
        
        # Foreground Frame for inputs
        self.frame = tk.Frame(root, bg="black")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.session_otp = None
        
        tk.Label(self.frame, text="Enter Password:", fg="lime", bg="black", font=("Courier", 12)).pack(pady=5)
        self.password_entry = tk.Entry(self.frame, show="*", width=30, font=("Courier", 12))
        self.password_entry.pack(pady=5)
        
        tk.Button(self.frame, text="Login", command=self.login, bg="green", fg="black", font=("Courier", 12)).pack(pady=10)
    
    def login(self):
        password = self.password_entry.get().strip()
        if not password:
            messagebox.showerror("Error", "Password cannot be empty!")
            return
        
        # Hash password (simulate password verification)
        pw_hash = hashlib.sha256(password.encode()).hexdigest()
        print(f"Password hash (debug): {pw_hash}")
        
        # Generate OTP
        self.session_otp = str(random.randint(100000, 999999))
        messagebox.showinfo("OTP Generated", f"Your OTP is: {self.session_otp}")
        
        # Show OTP input
        tk.Label(self.frame, text="Enter OTP:", fg="lime", bg="black", font=("Courier", 12)).pack(pady=5)
        self.otp_entry = tk.Entry(self.frame, width=20, font=("Courier", 12))
        self.otp_entry.pack(pady=5)
        tk.Button(self.frame, text="Verify OTP", command=self.verify_otp, bg="green", fg="black", font=("Courier", 12)).pack(pady=10)
    
    def verify_otp(self):
        otp_input = self.otp_entry.get().strip()
        if otp_input == self.session_otp:
            messagebox.showinfo("Success", "MFA verified! Redirecting to web app...")
            webbrowser.open("https://www.example.com")  # Replace with your web app
            self.root.destroy()
        else:
            messagebox.showerror("Failed", "Invalid OTP. Access denied.")

# ----------------------------
# Run the App
# ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MFAApp(root)
    root.mainloop()
