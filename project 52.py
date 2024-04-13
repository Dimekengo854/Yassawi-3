import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt

def melt_time(temperature):
    if temperature <= 0:
        return 0  # Если температура ниже нуля, снег и лед не тают
    else:
        # Простая модель: чем выше температура, тем быстрее происходит таяние
        return 60 / temperature  # Возвращаем время в минутах

def flood_analysis(data):
    risk = 0
    
    # Анализ каждого критерия
    if data['Rainfall (mm)'] > 50:
        risk += 1
    if data['Ice thickness (cm)'] > 20:
        risk += 1
    if data['Snow volume'] > 100:
        risk += 1
    if data['Temperature (C)'] > 5:
        risk += 1
    if melt_time(data['Temperature (C)']) < 60:
        risk += 1
    if melt_time(data['Temperature (C)']) < 60:
        risk += 1
    if data['Number of dams'] > 0:  # Изменили условие на > 0
        for i in range(1, data['Number of dams'] + 1):
            dam_capacity = data.get(f'Dam {i} capacity', 0)  # Получаем значение с ключом 'Dam i capacity', если оно существует
            water_volume = data.get('Water volume in reservoir', 0)  # Получаем значение с ключом 'Water volume in reservoir', если оно существует
            if dam_capacity < water_volume:
                risk += 1
    
    # Рассчитываем вероятность наводнения в процентах
    probability = (risk / 7) * 100
    
    return probability

def open_analysis_window():
    rainfall = float(rainfall_entry.get())
    ice_thickness = float(ice_thickness_entry.get())
    snow_volume = float(snow_volume_entry.get())
    temperature = float(temperature_entry.get())
    num_dams = int(num_dams_entry.get())

    data = {
        'Rainfall (mm)': rainfall,
        'Ice thickness (cm)': ice_thickness,
        'Snow volume': snow_volume,
        'Temperature (C)': temperature,
        'Number of dams': num_dams
    }

    if num_dams > 0:  # Изменили условие на > 0
        for i in range(1, num_dams + 1):
            dam_capacity = float(dam_capacity_entries[i-1].get())
            data[f'Dam {i} capacity'] = dam_capacity
    
    probability = flood_analysis(data)
    
    # Создаем DataFrame для анализа
    df = pd.DataFrame({'Критерий': ['Дождь', 'Толщина льда', 'Объем снега', 'Температура', 'Время таяния', 'Количество дамб', 'Вероятность наводнения'], 'Вероятность': [0.0] * 7})
    df.loc[df.index[:-1], 'Вероятность'] = [1 if probability > 50 else 0 for criterion in df['Критерий'][:-1]]
    df.at[df.index[-1], 'Вероятность'] = probability
    
    # Визуализируем данные
    plt.figure(figsize=(8, 6))
    plt.bar(df['Критерий'], df['Вероятность'], color=['blue' if p == 1 else 'red' for p in df['Вероятность']])
    plt.title('Анализ риска наводнения')
    plt.xlabel('Критерии')
    plt.ylabel('Вероятность наводнения')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Tkinter интерфейс
root = tk.Tk()
root.title("Ввод данных для анализа риска наводнения")

input_frame = ttk.Frame(root, padding="10")
input_frame.grid(row=0, column=0, padx=10, pady=10)

ttk.Label(input_frame, text="Количество дождя (мм):").grid(row=0, column=0, sticky="w")
rainfall_entry = ttk.Entry(input_frame)
rainfall_entry.grid(row=0, column=1)

ttk.Label(input_frame, text="Толщина льда (см):").grid(row=1, column=0, sticky="w")
ice_thickness_entry = ttk.Entry(input_frame)
ice_thickness_entry.grid(row=1, column=1)

ttk.Label(input_frame, text="Объем снега (метр куб):").grid(row=2, column=0, sticky="w")
snow_volume_entry = ttk.Entry(input_frame)
snow_volume_entry.grid(row=2, column=1)

ttk.Label(input_frame, text="Температура (C):").grid(row=3, column=0, sticky="w")
temperature_entry = ttk.Entry(input_frame)
temperature_entry.grid(row=3, column=1)

ttk.Label(input_frame, text="Количество дамб:").grid(row=4, column=0, sticky="w")
num_dams_entry = ttk.Entry(input_frame)
num_dams_entry.grid(row=4, column=1)

dam_capacity_entries = []

def update_dam_entries(event):
    global dam_capacity_entries
    for entry in dam_capacity_entries:
        entry.grid_forget()
        entry.destroy()
    dam_capacity_entries = []
    
    num_dams = int(num_dams_entry.get())
    if num_dams > 0:
        for i in range(1, num_dams + 1):
            ttk.Label(input_frame, text=f"Объем дамбы {i} (млрд литров):").grid(row=5 + i, column=0, sticky="w")
            dam_capacity_entry = ttk.Entry(input_frame)
            dam_capacity_entry.grid(row=5 + i, column=1)
            dam_capacity_entries.append(dam_capacity_entry)

num_dams_entry.bind('<FocusOut>', update_dam_entries)

analyze_button = ttk.Button(input_frame, text="Анализ", command=open_analysis_window)
analyze_button.grid(row=8, column=0, columnspan=2)

root.mainloop()
