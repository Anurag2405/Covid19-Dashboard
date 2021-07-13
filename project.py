import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from tkinter import *
from tkinter import ttk
import numpy as np
from functools import partial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import opendatasets as od


def main():
    '''dataset_url = 'https://www.kaggle.com/sudalairajkumar/covid19-in-india'

    od.download(dataset_url)'''
    root = Tk()
    root.title("Covid-19 Analyser")
    width= root.winfo_screenwidth() 
    height= root.winfo_screenheight()
    #setting tkinter window size
    root.geometry("%dx%d" % (width, height))
    covid_data = pd.read_csv("covid_19_india.csv",parse_dates=['Date'],dayfirst=True)
    covid_data = covid_data[['Date','State/UnionTerritory','Cured','Deaths','Confirmed']]
    covid_data.columns = ['date','state','cured','deaths','confirmed']
    #todays_date = date.today()
    #print(todays_date)
    date_col = covid_data['date']
    #print(type(date_col.max()))
    todays_date = str(date_col.max())


    today = covid_data[covid_data.date==todays_date]
    scrolling = str(today[['state','confirmed']].to_string(index=False))

    my_canvas = Canvas(root,width=width,height=height,bg = "white")
    my_canvas.place(x=0,y=0)
    #my_canvas.create_rectangle(10,50,300,200,fill = "#65adff")
    round_rectangle(my_canvas,60,50,500,200,fill = "#65adff")

    round_rectangle(my_canvas,550,50,1000,200,fill = "#4dddc0")
    round_rectangle(my_canvas,1050,50,1500,200,fill = "#ff6881")
    top_5_label =Label(root, text = "confirmed Cases",bg = "#65adff",fg = "#f6f7fb",font=("Arial", 18))
    top_5_label.place(x=100,y=75)
    confirmed_col = today[['confirmed']]
    covid_affected = confirmed_col.sum(axis =0)
    covid_affected = int(covid_affected)
    top_5_dflabel =Label(root, text = str(covid_affected),bg = "#65adff",fg = "#f6f7fb",font=("Arial", 18))
    top_5_dflabel.place(x=100,y=100)

    top_5_c_label =Label(root, text = "Cured Cases",bg = "#4dddc0",fg = "#f6f7fb",font=("Arial", 18))
    top_5_c_label.place(x=600,y=75)
    cured_col = today[['cured']]
    covid_cured = cured_col.sum(axis =0)
    covid_cured = int(covid_cured)
    top_5_cdflabel =Label(root, text = str(covid_cured),bg = "#4dddc0",fg = "#f6f7fb",font=("Arial", 18))
    top_5_cdflabel.place(x=600,y=100)


    top_5_d_label =Label(root, text = "Deceased",bg = "#ff6881",fg = "#f6f7fb",font=("Arial", 18))
    top_5_d_label.place(x=1100,y=75)
    deceased_col = today[['deaths']]
    covid_deceased = deceased_col.sum(axis =0)
    covid_deceased = int(covid_deceased)
    top_5_ddflabel =Label(root, text = str(covid_deceased),bg = "#ff6881",fg = "#f6f7fb",font=("Arial", 18))
    top_5_ddflabel.place(x=1100,y=100)


    top_5_button = Button(root, text = 'states with most confirmed cases',command=partial(top_5_confirmed,today,root))
    top_5_button.place(x=900,y=700)
    
    top_5_c_button =  Button(root, text = 'States with most cured cases',command=partial(top_5_cured,today,root))
    top_5_c_button.place(x=1100,y=700)
    
    top_5_d_button =  Button(root, text = 'Top 5 states with Maximum deaths',command=partial(top_5_death_states,today,root))
    top_5_d_button.place(x=1270,y=700)
    
    
    options = ["Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telengana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli and Daman and Diu","Delhi","Jammu and Kashmir","Ladakh","Lakshadweep","Puducherry"]
    clicked = StringVar()
  
    # initial menu text
    clicked.set("select State")
  
    # Create Dropdown menu
    drop = OptionMenu( root , clicked , *options )
    drop.place(x=760,y=698)
    selected_op = clicked.get()
    #print(type(selected_op))
    #print(selected_op)
    drop_down_button = Button(root, text = "Show analysis",command=partial(show,root,clicked,covid_data,today))
    drop_down_button.place(x=760,y=750)
    #state_wise_analysis(covid_data)


    total_population = 1392605249
    confirmed_col = today[['confirmed']]
    covid_affected = confirmed_col.sum(axis =0)
    covid_affected = int(covid_affected)
    #print(covid_affected)
    safe_people = total_population - covid_affected
    pie = [covid_affected,total_population]
    plt.axis('equal')
    #plt.pie(pie,labels =["affected people","safe people"],radius=1.5,autopct="%0.2f%%")
    #plt.show()
    fig = Figure(figsize = (5, 5),dpi = 100)
    plot1 = fig.add_subplot(111)
    plot1.pie(pie,labels =["affected","safe people"],autopct="%0.2f%%")
    new_canvas = FigureCanvasTkAgg(fig,root)
    new_canvas.draw()
    new_canvas.get_tk_widget().place(x=50,y=200)

    bottom_text_label = Label(root,text = "Amount of People affected from total population",font=("Arial", 18),bg= "white")
    bottom_text_label.place(x=50,y=700)

    root.mainloop()



def round_rectangle(canvas,x1, y1, x2, y2, r=25, **kwargs):    
    points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
    return canvas.create_polygon(points, **kwargs, smooth=True)



def show(root,clicked,covid_data,today):
    #mylabel = Label(root, text = clicked.get())
    #mylabel.place(x=30,y=150)
    state_wise_analysis(root,covid_data,clicked.get(),today)

def top_5_confirmed(today,root):
    max_cases = today.sort_values(by='confirmed',ascending=False)
    top5 = max_cases[0:5]
    #print("Top 5 States with the most number of confirmed cases are:")
    #print(top5[['state','confirmed']])
    #print(str(top5[['state','confirmed']]))

    top_5_canvas = Canvas(root,width=900,height=300,bg = "#f6f7fb")
    top_5_canvas.place(x=900,y=300)
    top_5_canvas.create_text(210,10,font=("Purisa", 15),text = "Top 5 States with the most number of confirmed cases are:")
    #top_5_canvas.create_text(200,90,font=("Purisa", 15), text = str(top5[['state','confirmed']].to_string(index=False)).strip())
    for_tree = top5[['state','confirmed']]
    my_tree = ttk.Treeview(root)
    my_tree['column']= list(for_tree.columns)
    my_tree['show'] = "headings"
    for column in my_tree['column']:
        my_tree.heading(column, text = column)

    top5_rows = for_tree.to_numpy().tolist()
    for row in top5_rows:
        my_tree.insert("","end",values = row)

    my_tree.place(x=950, y=350)
    
    sns.barplot(x = 'state',y = 'confirmed',data = top5, hue = "state")
    plt.show()


def top_5_cured(today,root):
    max_cured = today.sort_values(by='cured',ascending = False)
    top_cured = max_cured[0:5]
    #print("The states with maximum number of cured cases are: ")
    #print(str(top_cured[['state','cured']]))
    
    top_5_canvas = Canvas(root,width=900,height=300,bg = "#f6f7fb")
    top_5_canvas.place(x=900,y=300)
    top_5_canvas.create_text(210,10,font=("Purisa", 15),text = "states with most number of cured cases: ")
    #top_5_canvas.create_text(200,90,font=("Purisa", 15), text = str(top_cured[['state','cured']].to_string(index=False)).strip())
    for_tree = top_cured[['state','cured']]
    my_tree = ttk.Treeview(root)
    my_tree['column']= list(for_tree.columns)
    my_tree['show'] = "headings"
    for column in my_tree['column']:
        my_tree.heading(column, text = column)

    top5_rows = for_tree.to_numpy().tolist()
    for row in top5_rows:
        my_tree.insert("","end",values = row)

    my_tree.place(x=950, y=350)
    
    sns.barplot(x = 'state',y = 'cured',data = top_cured, hue = "state")
    plt.show()


def top_5_death_states(today,root):
    max_deaths = today.sort_values(by='deaths',ascending=False)
    top_death = max_deaths[0:5]
    #print("The states with most number of deaths are :")
    #print(str(top_death[['state','deaths']]))
    
    top_5_canvas = Canvas(root,width=900,height=300,bg = "#f6f7fb")
    top_5_canvas.place(x=900,y=300)
    top_5_canvas.create_text(210,10,font=("Purisa", 15),text = "states with most number of deaths are :")
    #top_5_canvas.create_text(200,90,font=("Purisa", 15), text = str(top_death[['state','deaths']].to_string(index=False)).strip())
    for_tree = top_death[['state','deaths']]
    my_tree = ttk.Treeview(root)
    my_tree['column']= list(for_tree.columns)
    my_tree['show'] = "headings"
    for column in my_tree['column']:
        my_tree.heading(column, text = column)

    top5_rows = for_tree.to_numpy().tolist()
    for row in top5_rows:
        my_tree.insert("","end",values = row)

    my_tree.place(x=950, y=350)
    
    sns.barplot(x = 'state',y = 'confirmed',data = top_death, hue = 'state')
    plt.show()





def state_wise_analysis(root,covid_data,drop_input,today):
    #state_inp = input("Enter the state whose data you want to check: ")
    
    top_5_canvas = Canvas(root,width=900,height=300,bg = "#f6f7fb")
    top_5_canvas.place(x=900,y=300)
    top_5_canvas.create_text(210,15,font=("Purisa", 18),text = "Data for this state is :")
    index = today.index
    condition = today["state"] == drop_input
    state_indices = index[condition]
    state_indices_list = state_indices.tolist()
    #print(state_indices_list[0])
    #print(today[[drop_input],["state"]])
    #top_5_canvas.create_text(200,90,font=("Purisa", 15), text = str(top_death[['state','deaths']].to_string(index=False)).strip())
    conf = today.at[state_indices_list[0],"confirmed"]
    cure = today.at[state_indices_list[0],"cured"]
    deat = today.at[state_indices_list[0],"deaths"]
    
    top_5_canvas.create_text(210,50,font=("Purisa", 15),text = f"Confirmed Cases : {conf}" )
    top_5_canvas.create_text(210,80,font=("Purisa", 15),text = f"Cured Cases      :{cure} ")
    top_5_canvas.create_text(210,110,font=("Purisa", 15),text = f"Deceased          :{deat} ")
    state_inp = drop_input
    state_data = covid_data[covid_data.state == state_inp]
    sns.lineplot(x = 'date',y = 'confirmed', data = state_data,label = 'confirmed cases', color='y')
    sns.lineplot(x = 'date',y = 'cured', data = state_data,label = 'cured cases', color='g')
    sns.lineplot(x = 'date',y = 'deaths', data = state_data,label = 'deaths', color='r')
    plt.show()

if __name__ == "__main__":
    main()