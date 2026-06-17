import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import json
import random
import requests
from io import BytesIO
import threading
import cv2
import mediapipe as mp
import numpy as np

# ------------------ CONSTANTS ------------------
BG_COLOR = "#f0f2f5"
PRIMARY_COLOR = "#1877f2"
WHITE_COLOR = "#ffffff"
SEPARATOR_COLOR = "#dadde1"
FONT_FAMILY = "Helvetica"
FONT_FAMILY_BOLD = "Helvetica Bold"
GREY_TEXT = "#65676b"
DATA_FILE = "user_data.json"

# ------------------ USER DATA HANDLING ------------------
def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ------------------ PLACEHOLDER ENTRY ------------------
class PlaceholderEntry(tk.Entry):
    def __init__(self, parent, placeholder, is_password=False, **kwargs):
        super().__init__(parent, **kwargs)
        self.placeholder = placeholder
        self.is_password = is_password
        self.config(font=("Arial", 12), bd=1, relief="solid", highlightthickness=1, highlightcolor=SEPARATOR_COLOR)
        self.insert(0, self.placeholder)
        self.config(fg="grey")
        if self.is_password:
            self.config(show="")
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

    def _on_focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg="black")
            if self.is_password:
                self.config(show="*")

    def _on_focus_out(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg="grey")
            if self.is_password:
                self.config(show="")

    def get_value(self):
        val = self.get()
        return val if val != self.placeholder else ""

# ------------------ PLACEHOLDER TEXT ------------------
class PlaceholderText(tk.Text):
    def __init__(self, parent, placeholder, **kwargs):
        super().__init__(parent, **kwargs)
        self.placeholder = placeholder
        self.config(font=("Arial", 12), fg="grey", relief="flat")
        self.insert("1.0", self.placeholder)
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

    def _on_focus_in(self, event):
        if self.get("1.0", "end-1c").strip() == self.placeholder:
            self.delete("1.0", tk.END)
            self.config(fg="black")

    def _on_focus_out(self, event):
        if not self.get("1.0", "end-1c").strip():
            self.insert("1.0", self.placeholder)
            self.config(fg="grey")

    def get_value(self):
        val = self.get("1.0", "end-1c").strip()
        return val if val != self.placeholder else ""

# ------------------ REGISTRATION WINDOW ------------------
class RegistrationWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Sign Up for Facebook")
        self.geometry("430x400")
        self.config(bg=WHITE_COLOR)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        header_frame = tk.Frame(self, bg=WHITE_COLOR)
        header_frame.pack(pady=(10, 5), padx=20, fill="x")
        tk.Label(header_frame, text="Sign Up", font=(FONT_FAMILY_BOLD, 24), bg=WHITE_COLOR).pack(anchor="w")
        tk.Label(header_frame, text="It's quick and easy.", font=(FONT_FAMILY, 12), bg=WHITE_COLOR, fg=GREY_TEXT).pack(anchor="w")
        tk.Frame(self, height=1, bg=SEPARATOR_COLOR).pack(fill="x", padx=20)

        form_frame = tk.Frame(self, bg=WHITE_COLOR)
        form_frame.pack(pady=15, padx=20)

        self.email_entry = PlaceholderEntry(form_frame, "Email address")
        self.email_entry.pack(pady=8, ipady=6, fill="x")

        self.password_entry = PlaceholderEntry(form_frame, "New password", is_password=True)
        self.password_entry.pack(pady=8, ipady=6, fill="x")

        self.confirm_password_entry = PlaceholderEntry(form_frame, "Confirm password", is_password=True)
        self.confirm_password_entry.pack(pady=8, ipady=6, fill="x")

        tk.Button(form_frame, text="Sign Up", bg="#42b72a", fg=WHITE_COLOR, font=(FONT_FAMILY_BOLD, 14),
                  relief="flat", cursor="hand2", command=self.register_user).pack(pady=20, ipady=5, fill="x")

    def register_user(self):
        email = self.email_entry.get_value()
        password = self.password_entry.get_value()
        confirm_password = self.confirm_password_entry.get_value()

        if not email or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required.", parent=self)
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.", parent=self)
            return

        users = load_users()
        if email in users:
            messagebox.showerror("Error", "An account with this email already exists.", parent=self)
            return

        users[email] = password
        save_users(users)
        messagebox.showinfo("Success", "Account created successfully! You can now log in.", parent=self)
        self.destroy()

# ------------------ LOGIN WINDOW ------------------
class FacebookLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Login")
        self.root.geometry("400x420")
        self.root.config(bg=BG_COLOR)

        main_frame = tk.Frame(root, bg=WHITE_COLOR, highlightbackground=SEPARATOR_COLOR, highlightthickness=1)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(main_frame, text="facebook", font=(FONT_FAMILY_BOLD, 32), fg=PRIMARY_COLOR, bg=WHITE_COLOR).pack(pady=(20, 10))

        self.email_entry = PlaceholderEntry(main_frame, "Email or Phone", width=35)
        self.email_entry.pack(pady=5, ipady=6)
        self.password_entry = PlaceholderEntry(main_frame, "Password", is_password=True, width=35)
        self.password_entry.pack(pady=5, ipady=6)

        tk.Button(main_frame, text="Log In", bg=PRIMARY_COLOR, fg=WHITE_COLOR, width=30, font=(FONT_FAMILY_BOLD, 12),
                  relief="flat", cursor="hand2", command=self.login).pack(pady=10, ipady=8)
        tk.Frame(main_frame, height=1, bg=SEPARATOR_COLOR).pack(fill="x", padx=30, pady=20)
        tk.Button(main_frame, text="Create New Account", bg="#42b72a", fg=WHITE_COLOR, font=(FONT_FAMILY_BOLD, 11),
                  relief="flat", cursor="hand2", command=self.open_registration_window).pack(pady=10, ipady=8)

    def open_registration_window(self):
        RegistrationWindow(self.root)

    def login(self):
        email = self.email_entry.get_value()
        password = self.password_entry.get_value()
        if not email or not password:
            messagebox.showwarning("Error", "Please enter both email and password!")
            return
        users = load_users()
        if email in users and users[email] == password:
            self.root.destroy()
            FacebookHome(email)
        else:
            messagebox.showerror("Invalid Login", "The email or password you entered is incorrect.")

# ------------------ FACEBOOK HOME ------------------
class FacebookHome:
    def __init__(self, user_email):
        self.root = tk.Tk()
        self.root.title("Facebook - Home")
        self.root.geometry("950x600")
        self.root.config(bg=BG_COLOR)

        self.user_email = user_email
        self.user_name = user_email.split('@')[0]
        self.all_posts = []
        self.active_tab = None

        top_frame = tk.Frame(self.root, bg=WHITE_COLOR, height=60, highlightbackground=SEPARATOR_COLOR, highlightthickness=1)
        top_frame.pack(fill="x")
        tk.Label(top_frame, text="facebook", font=(FONT_FAMILY_BOLD, 24), fg=PRIMARY_COLOR, bg=WHITE_COLOR).place(x=20, y=10)
        self.create_search_bar(top_frame)

        self.menu_buttons = {}
        menu_items = {
            "Home": self.show_home,
            "About": self.show_about,
            "Help": self.show_help,
            "Account": self.show_account,
            "Snake Game": self.open_snake_game  # 🐍 Added Game Button
        }
        x_pos = 600
        for item, func in menu_items.items():
            btn = tk.Button(top_frame, text=item, bg=WHITE_COLOR, fg="black", bd=0, font=(FONT_FAMILY, 12),
                            cursor="hand2", activebackground=BG_COLOR, command=lambda f=func, b=item: self.switch_tab(f, b))
            btn.place(x=x_pos, y=18)
            self.menu_buttons[item] = btn
            x_pos += 100

        left_frame = tk.Frame(self.root, bg=BG_COLOR, width=250)
        left_frame.place(x=0, y=60, relheight=1, anchor="nw")
        self.create_sidebar(left_frame, user_email)

        feed_container = tk.Frame(self.root, bg=BG_COLOR)
        feed_container.place(x=260, y=70, width=670, height=520)

        self.canvas = tk.Canvas(feed_container, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar = ttk.Scrollbar(feed_container, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.feed_frame = tk.Frame(self.canvas, bg=BG_COLOR)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.feed_frame, anchor="nw", width=650)
        self.canvas.bind('<Configure>', lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))
        self.root.bind("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        self.switch_tab(self.show_home, "Home")
        self.root.mainloop()

    # ---------- UI COMPONENTS ----------
    def create_search_bar(self, parent):
        search_frame = tk.Frame(parent, bg=BG_COLOR, relief="flat")
        search_frame.place(x=80, y=12)
        tk.Label(search_frame, text="🔍", font=("Arial", 12), bg=BG_COLOR).pack(side="left", padx=(5, 0))
        self.search_entry = PlaceholderEntry(search_frame, "Search Facebook", bd=0, highlightthickness=0, bg=BG_COLOR, width=25)
        self.search_entry.pack(side="left", ipady=5)
        self.search_entry.bind("<Return>", self.perform_search)

    def create_sidebar(self, parent, user_email):
        items = {"🧑‍🤝‍🧑": "Friends", "👥": "Groups", "🏪": "Marketplace", "📺": "Watch", "🕒": "Memories"}
        tk.Label(parent, text=f"👤 {user_email}", bg=BG_COLOR, font=(FONT_FAMILY_BOLD, 12)).pack(pady=20, padx=15, anchor="w")
        for icon, text in items.items():
            tk.Label(parent, text=f"{icon}  {text}", bg=BG_COLOR, font=(FONT_FAMILY, 12)).pack(pady=8, padx=15, anchor="w")

    # ---------- NAVIGATION ----------
    def switch_tab(self, view_func, tab_name):
        if self.active_tab:
            self.active_tab.config(font=(FONT_FAMILY, 12), fg="black")
        view_func()
        self.active_tab = self.menu_buttons[tab_name]
        self.active_tab.config(font=(FONT_FAMILY_BOLD, 12), fg=PRIMARY_COLOR)

    # ---------- FEED ----------
    def show_home(self):
        self.all_posts = [
            {'text': "Look at this cute dog!", 'image_url': "https://loremflickr.com/600/400/dog", 'author': 'jane.doe@example.com'},
            {'text': "Nature is beautiful 🌿", 'image_url': "https://loremflickr.com/600/400/nature", 'author': 'john.smith@example.com'},
            {'text': "Coding is fun!", 'image_url': None, 'author': 'coder@example.com'},
        ]
        self.render_feed(self.all_posts)

    def render_feed(self, posts):
        self.clear_feed()
        self.create_post_box()
        if not posts:
            tk.Label(self.feed_frame, text="No results found.", bg=BG_COLOR, font=(FONT_FAMILY_BOLD, 14), fg=GREY_TEXT).pack(pady=50)
        else:
            for p in posts:
                self.show_post(p['author'], p['text'], p['image_url'])
        self.feed_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def create_post_box(self):
        post_frame = tk.Frame(self.feed_frame, bg=WHITE_COLOR, highlightbackground=SEPARATOR_COLOR, highlightthickness=1)
        post_frame.pack(pady=10, padx=20, fill="x")
        placeholder = f"What's on your mind, {self.user_name}?"
        self.post_entry = PlaceholderText(post_frame, placeholder, height=3)
        self.post_entry.pack(pady=10, padx=15, fill="x")
        tk.Frame(post_frame, height=1, bg=SEPARATOR_COLOR).pack(fill="x", padx=15)
        tk.Button(post_frame, text="Post", bg=PRIMARY_COLOR, fg=WHITE_COLOR, font=(FONT_FAMILY_BOLD, 11),
                  cursor="hand2", relief="flat", command=self.add_post).pack(pady=(10, 15), ipady=4, ipadx=20)

    def add_post(self):
        post_text = self.post_entry.get_value()
        if not post_text:
            messagebox.showwarning("Empty Post", "Write something before posting!")
            return
        new_post = {'text': post_text, 'image_url': None, 'author': self.user_email}
        if messagebox.askyesno("Add Image", "Do you want to add an image to your post?"):
            filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
            if filepath:
                new_post['image_url'] = filepath
        self.all_posts.insert(0, new_post)
        self.render_feed(self.all_posts)

    def show_post(self, author, text, image_url=None):
        post = tk.Frame(self.feed_frame, bg=WHITE_COLOR, highlightbackground=SEPARATOR_COLOR, highlightthickness=1)
        post.pack(pady=10, padx=20, fill="x")
        tk.Label(post, text=author, bg=WHITE_COLOR, font=(FONT_FAMILY_BOLD, 12)).pack(anchor="w", padx=15, pady=(10, 0))
        tk.Label(post, text=text, bg=WHITE_COLOR, font=("Arial", 12), wraplength=600, justify="left").pack(anchor="w", padx=15, pady=(8, 10))
        if image_url:
            img_label = tk.Label(post, bg=WHITE_COLOR)
            img_label.pack(pady=(0, 10), padx=15)
            if image_url.startswith('http'):
                threading.Thread(target=self.load_web_image, args=(image_url, img_label), daemon=True).start()
            else:
                self.load_local_image(image_url, img_label)

    def load_web_image(self, url, label):
        try:
            response = requests.get(url, stream=True, timeout=5)
            response.raise_for_status()
            img_data = response.content
            image = Image.open(BytesIO(img_data))
            image.thumbnail((600, 400))
            photo = ImageTk.PhotoImage(image)
            self.root.after(0, lambda: self.update_image_label(label, photo))
        except Exception as e:
            print(f"Failed to load web image {url}: {e}")

    def load_local_image(self, path, label):
        try:
            image = Image.open(path)
            image.thumbnail((600, 400))
            photo = ImageTk.PhotoImage(image)
            label.image = photo
            label.configure(image=photo)
        except Exception as e:
            print(f"Error loading local image: {e}")

    def update_image_label(self, label, photo):
        label.configure(image=photo)
        label.image = photo

    def clear_feed(self):
        for widget in self.feed_frame.winfo_children():
            widget.destroy()

    # ---------- OTHER TABS ----------
    def show_about(self):
        self.clear_feed()
        tk.Label(self.feed_frame, text="About Facebook Clone", bg=BG_COLOR, font=(FONT_FAMILY_BOLD, 18)).pack(pady=20)
        tk.Label(self.feed_frame, text="This is a simulated Facebook clone built using Tkinter.\nCreated by AI 💻",
                 bg=BG_COLOR, font=(FONT_FAMILY, 12), justify="center").pack(pady=10)

    def show_help(self):
        self.clear_feed()
        tk.Label(self.feed_frame, text="Help & Support", bg=BG_COLOR, font=(FONT_FAMILY_BOLD, 18)).pack(pady=20)
        tk.Label(self.feed_frame, text="For assistance, contact support@facebookclone.com", bg=BG_COLOR, font=(FONT_FAMILY, 12)).pack(pady=10)

    def show_account(self):
        self.clear_feed()
        tk.Label(self.feed_frame, text="Account Settings", bg=BG_COLOR, font=(FONT_FAMILY_BOLD, 18)).pack(pady=20)
        tk.Label(self.feed_frame, text=f"Logged in as: {self.user_email}", bg=BG_COLOR, font=(FONT_FAMILY, 12)).pack(pady=10)
        tk.Button(self.feed_frame, text="Log Out", bg="#e53935", fg=WHITE_COLOR, font=(FONT_FAMILY_BOLD, 11),
                  relief="flat", cursor="hand2", command=self.logout).pack(pady=15, ipady=4, ipadx=20)

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        FacebookLogin(root)
        root.mainloop()

    def perform_search(self, event=None):
        query = self.search_entry.get_value().lower()
        if not query:
            self.render_feed(self.all_posts)
            return
        filtered_posts = [p for p in self.all_posts if query in p['text'].lower()]
        self.render_feed(filtered_posts)

    # ---------- 🐍 SNAKE GAME (Embedded with OpenCV + MediaPipe) ----------
    def open_snake_game(self):
        self.clear_feed()
        tk.Label(self.feed_frame, text="🎮 Gesture-Controlled Snake Game", font=(FONT_FAMILY_BOLD, 18), bg=BG_COLOR).pack(pady=10)
        self.video_label = tk.Label(self.feed_frame, bg="black")
        self.video_label.pack(pady=10)

        self.running_game = True
        threading.Thread(target=self.run_snake_game, daemon=True).start()

    def run_snake_game(self):
        mp_hands = mp.solutions.hands
        mp_draw = mp.solutions.drawing_utils
        hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

        cap = cv2.VideoCapture(0)
        snake = [(250, 250)]
        snake_length = 1
        direction = np.array([0, 0])
        food = (random.randint(50, 590), random.randint(50, 430))
        score = 0
        speed = 10

        def distance(p1, p2): return np.linalg.norm(np.array(p1) - np.array(p2))

        while self.running_game:
            success, img = cap.read()
            if not success:
                break

            img = cv2.flip(img, 1)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)
            h, w, _ = img.shape
            index_tip = None

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    lm_list = [(int(lm.x * w), int(lm.y * h)) for lm in handLms.landmark]
                    mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
                    index_tip = lm_list[8]

            if index_tip:
                head_x, head_y = snake[-1]
                target_x, target_y = index_tip
                dir_vec = np.array([target_x - head_x, target_y - head_y])
                if np.linalg.norm(dir_vec) > 10:
                    direction = dir_vec / np.linalg.norm(dir_vec) * speed
                new_head = (snake[-1][0] + direction[0], snake[-1][1] + direction[1])
                snake.append(new_head)
                if len(snake) > snake_length:
                    snake.pop(0)

            cv2.circle(img, food, 8, (0, 0, 255), -1)
            for i in range(1, len(snake)):
                cv2.line(img, (int(snake[i - 1][0]), int(snake[i - 1][1])),
                         (int(snake[i][0]), int(snake[i][1])), (0, 255, 0), 10)

            if distance(snake[-1], food) < 20:
                score += 1
                snake_length += 5
                food = (random.randint(50, 590), random.randint(50, 430))

            head_x, head_y = snake[-1]
            if head_x < 0 or head_x > w or head_y < 0 or head_y > h:
                cv2.putText(img, f"Game Over! Score: {score}", (100, 240),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                self.running_game = False

            cv2.putText(img, f"Score: {score}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            imgtk = ImageTk.PhotoImage(image=img_pil)
            self.video_label.configure(image=imgtk)
            self.video_label.image = imgtk

            if not self.running_game:
                break

        cap.release()
        cv2.destroyAllWindows()
        self.video_label.config(text="Game Over! Restart or close tab.")

# ------------------ MAIN ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = FacebookLogin(root)
    root.mainloop()
