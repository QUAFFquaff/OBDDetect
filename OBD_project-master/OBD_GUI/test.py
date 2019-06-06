from OBD_GUI import GUI
import time

def main():
    panel = GUI.Panel()
    panel.drawPanel()
    time.sleep(2)
    panel.addbBar(9)
    time.sleep(2)
    panel.removebBar()
    panel.removebBar()
    panel.removebBar()
    time.sleep(2)
    panel.addbBar(9)
    time.sleep(2)

if __name__ == "__main__":
    main()
