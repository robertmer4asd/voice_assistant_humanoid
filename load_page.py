import webview

def open_html_file_in_window(file_path):
    webview.create_window('HTML Viewer', url=file_path)
    webview.start()

open_html_file_in_window("spectrum.html")
