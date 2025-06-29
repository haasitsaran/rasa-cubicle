to run the rasa need Anaconda installed on the pc if python version is above 3.10.5

if you have adavnaced python version use these commands

conda create -n rasa-env python=3.10

to activate the environment

conda activate rasa-env 

to deactivate the environment

conda deactivate

after activate then run 

pip install rasa

to train the rasa

rasa train
rasa train --verbose

to run the actions use

rasa run actions --port 5055
rasa run -m models --enable-api --cors "*" --debug --endpoints endpoints.yml

this to mainly run the rasa

 rasa run --enable-api --cors "*"
rasa run actions --cors "*" --debug

use this to clean the previously trained data

rasa clean

delete the modals manual direactly use this command

rmdir /s /q models
