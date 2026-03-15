import datetime

# def log(message):
#     ts = datetime.datetime.now()
#     print(f"[{ts}] {message}")

def log(self, message):
    tab = self.window.forge1d_tab
    tab.log_view.append(message)