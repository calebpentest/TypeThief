
Debugging Guide: finding and reading f_keystroke.txt
If you’re trying to locate and view the f_keystroke.txt file created by the TypeThief keylogger, follow these steps in Command Prompt (CMD) on Windows.

Step 1: Search for the File
Open Command Prompt:
Press Win + R, type cmd, and press Enter.
Navigate to your user directory (replace DELL with your username):
cmd
cd C:\Users\DELL
To find your username, type ECHO %USERNAME% in CMD if unsure.
Search for f_keystroke.txt across all subdirectories:
cmd
dir f_keystroke.txt /s /p
/s: Searches all subfolders.
/p: Pauses output for readability.
Look for the file’s location in the output (e.g., C:\Users\DELL\AppData\Roaming\TypeThief)

Step 2: Read the File
Change to the directory where f_keystroke.txt was found (example path):
cmd
cd C:\Users\DELL\AppData\Roaming\TypeThief
Replace the path with the one from Step 1 if it’s different.
Display the file’s contents:
cmd
type f_keystroke.txt
This shows the logged keystrokes (e.g., [ENTER]h[SPACE]e[SPACE]l[SPACE]l[SPACE]o).
(Optional) Open in Notepad for easier reading:
cmd
notepad f_keystroke.txt

Permissions Issue:
"If you get ‘Access is denied,’ right-click CMD, choose ‘Run as administrator,’ and retry."
Stopping the Keylogger:
"To stop the keylogger, press Esc (if it works) or use Task Manager to end the python.exe process."
