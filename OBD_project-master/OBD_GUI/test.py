from OBD_GUI import GUI
import time

def main():
    panel = GUI.Panel()
    panel.drawPanel()
    time.sleep(2)
    panel.addBar()
    time.sleep(2)
    panel.removeBar()
    time.sleep(2)

if __name__ == "__main__":
    main()
