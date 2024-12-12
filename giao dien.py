# Welcome to GitHub Desktop!
import tkinter as tk
from tkinter import ttk,messagebox, filedialog
import csv
from datetime import datetime
import pandas as pd

root = tk.Tk()
root.title("Thông tin nhân viên")
# Hàm lưu dữ liệu vào CSV
def save_data(entry_id=None,entry_name=None,entry_title=None,combo_unit=None,entry_dob=None,gender_var=None,entry_id_card=None,entry_issue_date=None,entry_place=None):
    data = {
        "Mã": entry_id.get(),
        "Tên": entry_name.get(),
        "Đơn vị": combo_unit.get(),
        "Chức danh": entry_title.get(),
        "Ngày sinh": entry_dob.get(),
        "Giới tính": "Nam" if gender_var.get() == 1 else "Nữ",
        "Số CMND": entry_id_card.get(),
        "Ngày cấp": entry_issue_date.get(),
        "Nơi cấp": entry_place.get(),
    }

    if not all(data.values()):
        messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
        return

    with open("nhan_vien.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if file.tell() == 0:  # Ghi header nếu file rỗng
            writer.writeheader()
        writer.writerow(data)
    messagebox.showinfo("Thành công", "Đã lưu thông tin nhân viên!")
    clear_fields()


# Hàm làm trống các trường
def clear_fields(entry_id=None,entry_name=None,entry_title=None,combo_unit=None,entry_dob=None,gender_var=None,entry_id_card=None,entry_issue_date=None,entry_place=None):
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    combo_unit.set("")
    entry_title.delete(0, tk.END)
    entry_dob.delete(0, tk.END)
    gender_var.set(0)
    entry_id_card.delete(0, tk.END)
    entry_issue_date.delete(0, tk.END)
    entry_place.delete(0, tk.END)


# Hàm hiển thị danh sách sinh nhật hôm nay
def show_birthdays_today():
    try:
        with open("nhan_vien.csv", mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            today = datetime.now().strftime("%d/%m/%Y")
            birthdays = [
                row["Tên"]
                for row in reader
                if row["Ngày sinh"].split("/")[0:2] == today.split("/")[0:2]
            ]
    except FileNotFoundError:
        birthdays = []

    if birthdays:
        messagebox.showinfo("Sinh nhật hôm nay", "\n".join(birthdays))
    else:
        messagebox.showinfo("Sinh nhật hôm nay", "Không có nhân viên nào sinh nhật hôm nay.")


# Hàm xuất danh sách sắp xếp theo tuổi
def export_sorted_list():
    try:
        data = pd.read_csv("nhan_vien.csv", encoding="utf-8")
        data["Ngày sinh"] = pd.to_datetime(data["Ngày sinh"], format="%d/%m/%Y")
        sorted_data = data.sort_values(by="Ngày sinh", ascending=True)
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            sorted_data.to_excel(file_path, index=False)
            messagebox.showinfo("Thành công", "Xuất file thành công!")
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file dữ liệu!")

# Các trường nhập liệu
# Giao diện chính
root = tk.Tk()
root.title("Thông tin nhân viên")

# Các trường nhập liệu
label_id = tk.Label(root, text="Mã:")
label_id.grid(row=0, column=0)
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1)

label_name = tk.Label(root, text="Tên:")
label_name.grid(row=1, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1)

label_unit = tk.Label(root, text="Đơn vị:")
label_unit.grid(row=2, column=0)
combo_unit = ttk.Combobox(root, values=["Phòng A", "Phòng B", "Phòng C"])
combo_unit.grid(row=2, column=1)

label_title = tk.Label(root, text="Chức danh:")
label_title.grid(row=3, column=0)
entry_title = tk.Entry(root)
entry_title.grid(row=3, column=1)

label_dob = tk.Label(root, text="Ngày sinh (dd/mm/yyyy):")
label_dob.grid(row=4, column=0)
entry_dob = tk.Entry(root)
entry_dob.grid(row=4, column=1)

label_gender = tk.Label(root, text="Giới tính:")
label_gender.grid(row =5, column=0)
gender_var = tk.IntVar()
radio_male = tk.Radiobutton(root, text="Nam", variable=gender_var, value=1)
radio_female = tk.Radiobutton(root, text="Nữ", variable=gender_var, value=2)
radio_male.grid(row=5, column=1, sticky=tk.W)
radio_female.grid(row=5, column=1)

label_id_card = tk.Label(root, text="Số CMND:")
label_id_card.grid(row=6, column=0)
entry_id_card = tk.Entry(root)
entry_id_card.grid(row=6, column=1)

label_issue_date = tk.Label(root, text="Ngày cấp (dd/mm/yyyy):")
label_issue_date.grid(row=7, column=0)
entry_issue_date = tk.Entry(root)
entry_issue_date.grid(row=7, column=1)

label_place = tk.Label(root, text="Nơi cấp:")
label_place.grid(row=8, column=0)
entry_place = tk.Entry(root)
entry_place.grid(row=8, column=1)

# Nút chức năng
btn_save = tk.Button(root, text="Lưu thông tin", command=save_data)
btn_save.grid(row=9, column=0)

btn_clear = tk.Button(root, text="Xóa thông tin", command=clear_fields)
btn_clear.grid(row=9, column=1)

btn_show_birthdays = tk.Button(root, text="Sinh nhật hôm nay", command=show_birthdays_today)
btn_show_birthdays.grid(row=10, column=0)

btn_export = tk.Button(root, text="Xuất danh sách", command=export_sorted_list)
btn_export.grid(row=10, column=1)

root.mainloop()