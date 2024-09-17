import tkinter as tk
from tkinter import messagebox
import random
import math

bombs = []              # เก็บีะเบิดที่กดได้
score = 0               # คะแนน
bombs_denger = []       # ระเบิดที่เป็นอันตราย

def generate_bombs():
    # ดึงตัวแปล global มาใช้งาน
    global bombs, score, bombs_denger
    try:
        num = int(entry.get())      # ดึงค่าข้อมูลมาจาก entry เพื่อกำหนดเป็นลูกระเบิด
        # รีเซ็ตค่า bombs score bombs_denger
        bombs = []
        score = 0
        bombs_denger = []
        
        # รีเซ็ตระเบิด
        for widget in frame.winfo_children():
            widget.destroy()
        
        # ถ่าลูกระเบิดน้อยกว่า3 หรือ มากกว่า 60 ให้แสดง showerror แล้วหยุดการทำงานโค๊ดด้านล่าง
        if num < 3 or num > 60:
            messagebox.showerror("Error Alert", "Plese enter between 3 to 60")
            return
        
        # สร้าง Label เพื่อแสดง คะแนนของผู้เล่น
        score_label = tk.Label(frame, text=f"score is {score}")
        score_label.grid(row=0, column=0,  padx=20, pady=10)
        
        # ดึงรูปภาพมาเป็นลูกระเบิด
        bomb_image = tk.PhotoImage(file="Bomb.png")
        # ปรับแต่งขนาดรูปภาพเป็น 1 / 5 ของรูปเต็ม
        scaled_bomb_image = bomb_image.subsample(5, 5)
        
        # for เพื่อสร้างลูกระเบิด
        for i in range(1, num + 1):
            # สร้าง Button สำหรับทำเป็นลูกระเบิด
            button = tk.Button(frame, text=f"Bomb {i}", image=scaled_bomb_image)
            button.config(command=lambda i=i, button=button, sl=score_label: click_bomb_button(i, button, sl))  # ถ้าไม่ทำงี้มันบัค
            # ใส่ Image ให้กับลูกระเบิด
            button.image = scaled_bomb_image
            # สร้างตัวแปล row col เพื่อทำให้ลูกระเบิดเรียงต่อกัน
            row, col = divmod(i-1, 10)   # divmod จะคือค่า 2 ค่าคือ a // b | a % b
            # กำหนดว่า Button จะวางที่ row col เท่าไหร่
            button.grid(row=row+1, column=col, padx=5, pady=5)
            # เพิ่มลูกระเบิดเข้าไปใน bombs
            bombs.append(i)
        
        n = math.floor(len(bombs) / 3)      # หาจำนวนลูกระเบิด
        
        # เมื่อ lenของbombs_denger น้อยกว่า n ให้ทำงานต่อไป
        while len(bombs_denger) < n:
            # สุ่มลูกระเบิดที่เป็นอันตราย
            bomb_number = random.choice(bombs)
            # เพิ่มลูกระเบิดที่เป็นอันตรายลงใน bombs_denger
            bombs_denger.append(bomb_number)
            # ลบลูกระเบิดที่เป็นอันตรายออกจาก bombs
            bombs.remove(bomb_number)
        
        #มีไว้สำหรับทดสอบ เพราะคนสร้างเล่นไม่ผ่าน
        print(bombs)
        print(bombs_denger)
    # ถ้าเกิดว่ากรอกค่าที่ไม่ใช่ตัวเลขเข้ามาจะแสดง Error
    except ValueError:
        messagebox.showerror("Error Alert", "Plese enter just integer !!")

def click_bomb_button(number, button, score_label):
    # ดึงตัวแปล global มาใช้งาน
    global score, bombs_denger, bombs
    # ถ้าเกิดว่าลูกระบิดที่ส่งเข้ามาอยู่ใน bombs_denger
    if number in bombs_denger:
        # แสดง Sorry Loser !!
        messagebox.showerror("You Lose", "Sorry Loser !!")
        # ทำการลบข้อมูลทั้งหมด
        for widget in frame.winfo_children():
            widget.destroy()
        bombs = []
        score = 0
        bombs_denger = []
    # ถ้าไม่ใช้
    else:
        # disable ปุ่มที่กดไปแล้ว
        button.config(state=tk.DISABLED)
        # เพิ่ม score ของผู้เล่น
        score+=1
        # ลบลูกระเบิดจาก bombs
        bombs.remove(number)
        # อัพเดท score ของผู้เล่นในหน้าจอ
        score_label.config(text=f"score is {score}")

        # ถ้าเกิดว่า bombs เท่ากับ 0
        if len(bombs) == 0:
            # แสดง Your final score is {score}
            messagebox.showinfo("You Win !!", f"Your final score is {score}")
            # ทำการลบข้อมูลทั้งหมด
            for widget in frame.winfo_children():
                widget.destroy()
            bombs = []
            score = 0
            bombs_denger = []
        else:
            pass

# สร้าง root element
root = tk.Tk()

# เพิ่มชื่อแอพขึ้นมา
root.title("BOMD GAME")     
# กำหนด minimum size ของหน้าจอ
root.minsize(600,600)

# สร้าง Input เพื่อรับค่าของตัวเลขและนำไปใช้ในการสร้าง bomb
label1 = tk.Label(root, text="Enter num of bomb you want to play here :")
label1.grid(row=0, column=0, padx=20, pady=10)

# สร้าง entry สำหรับระบค่าจำนวนระเบิด
entry = tk.Entry(root)
entry.grid(row=0, column=1, padx=20, pady=10)

# สร้างปุ่มสำหรับเพิ่มระเบิด
generate_bomb = tk.Button(root, text="Generate", command=generate_bombs)
generate_bomb.grid(row=0, column=2, padx=20, pady=10)

# สร้าง frame เพื่อเก็บปุ่มที่สร้างขึ้นใหม่
frame = tk.Frame(root)
frame.grid(row=1, column=0, columnspan=3, padx=20, pady=10)

root.mainloop()