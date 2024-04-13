import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

def calculate_release(event=None):
    try:
        capacity = float(entry_capacity.get()) * 1e9  
        current_water = float(entry_current.get()) * 1e9  
        water_to_add = float(entry_add.get()) * 1e9  

        target_water_level = capacity * 0.65 
        if current_water + water_to_add <= target_water_level:
            messagebox.showinfo("Нәтиже", "Дамбаны ашу керек емес")
        else:
            water_to_release = current_water + water_to_add - target_water_level

            time = [0, 1, 2]  
            water_level = [current_water / 1e9, (current_water + water_to_add) / 1e9, (current_water + water_to_add - water_to_release) / 1e9]  

            plt.figure(figsize=(8, 5))
            plt.plot(time, water_level, marker='o')
            plt.xlabel('Уақыт (сағат)')
            plt.ylabel('Су деңгейі (млрд литр)')
            plt.title('Су қоймасындағы су деңгейінің динамикасы')
            plt.xticks(time, ['Басы', 'Су қосылғаннан кейін', 'Дамба ашылуы мүмкін болуынан кейін'])
            plt.grid(True)
            plt.savefig("water_level_plot.png")  

            result_text = f"Дамбаны ашып, жіберу керек {water_to_release / 1e9} млрд литр суды"
            messagebox.showinfo("Нәтиже", result_text)

            plt.show()

    except ValueError:
        messagebox.showerror("Қате", "Өтінемін, Дұрыс сандарды енгізіңіз.")

window = tk.Tk()
window.title("Су қоймасынан судың ағуы")
window.geometry("600x250")  
window.configure(bg='light blue')  

label_capacity = tk.Label(window, text="Қойманың сиымдылығы (млрд литр):")
label_capacity.pack()
entry_capacity = tk.Entry(window)
entry_capacity.pack()

label_current = tk.Label(window, text="Дәл қазіргі су мөлшері (млрд литр):")
label_current.pack()
entry_current = tk.Entry(window)
entry_current.pack()

label_add = tk.Label(window, text="Қосқыңыз келетің су мөлшері (млрд литр):")
label_add.pack()
entry_add = tk.Entry(window)
entry_add.pack()

btn_calculate = tk.Button(window, text="Есептеу", command=calculate_release)
btn_calculate.pack()

window.bind('<Return>', calculate_release)

window.mainloop()
