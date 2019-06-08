import threading

from OBD_GUI import GUI
import time

GUI_Bar_flag = False


# this thread for time-window monitor and LDA detection
class Thread_for_GUI_timer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__running = threading.Event()
        self.__running.set()

    def run(self):
        global GUI_Bar_flag
        time.sleep(1)
        GUI_Bar_flag = True
        self.stop()

    def stop(self):
        self.__running.clear()


def main():
    global GUI_Bar_flag
    panel = GUI.Panel()
    panel.drawPanel()
    time.sleep(2)
    panel.addbBar(4)
    while True:
        GUI_timer = Thread_for_GUI_timer()
        GUI_timer.start()
        while True:
            if GUI_Bar_flag:
                panel.clean_bars()
                break
        time.sleep(1)
        panel.addbBar(4)



if __name__ == "__main__":
    main()
