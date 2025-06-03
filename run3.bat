@echo off
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
call .\AiTOMM\Scripts\activate.bat
python ImageGenarator.py a_curious,_friendly,_and_humorous_person_with_interests_in_geography,_history,_pop_culture,_and_multimedia_content,_located_in_Rajpur_Sonarpur,_West_Bengal,_India
pause
