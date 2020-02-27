import tkinter as tk


window = tk.Tk()

class GUI():
    def RunGUI(self):
    
        l1 = tk.Label(window, text = "Enter Snowpark Here ")
      
        self.entSearch = tk.Entry(window, )
        
        
        self.entSearch.insert(0,"Snowpark")
        
        button = tk.Button(window, text ="Finish", width = 25, command = self.end )


        l1.grid(row = 0, column = 0)
        
        self.entSearch.grid(row = 0, column = 1)
        
        button.grid(row=1, column =1 )

        window.mainloop()
    
    def end(self):
    #stationdictionary.update({elevation : name}) 
    #big credit to Andrew for like.. figuring it out, thanks Java
        window1 = tk.Tk()
        l2 = tk.Label(window1, text = "kitten")
        l2.grid(row = 0, column = 0)
        
        
        
        
        window.destroy()
        
if __name__ == "__main__":
    firstGUI = GUI()
    firstGUI.RunGUI()