### CompVision_Yolo11

Yolo11 nano version from Ultralytics - training for object detection

Dataset: Visdrone from Ultralytics 

How to run (run on terminal -> choose powershell):
1. Setup virtual environment if it counters conflict
   python -m venn .venv
   pip install ultralytics

2. Run the .venv folder (on terminal) & select the interpreter
   .venv/Scripts/Activate  (then it must show the - greenstatus (venv))

   Select the interpreter python'.venv':venv
   ---------------------------------------------
   If it got execution policy error, run:
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

3. Run the file (on terminal):
   python run.py (ctrl + c on terminal --> to exit)
