from aeneas.executetask import ExecuteTask
from aeneas.task import Task
from aeneas.textfile import TextFileFormat
from aeneas.textfile import TextFragment

# Path to the text file
text_file = "lyrics_train/pop/Closer.txt"

# Path to the audio file
audio_file = "lyrics_train/pop/Closer(vocal).wav"

# Create a Task object
config_string = "task_language=eng|is_text_type=plain|os_task_file_format=json"
task = Task(config_string=config_string)

# Assign the audio file to the task
task.audio_file_path_absolute = audio_file
task.text_file_path_absolute = text_file
# Create a TextFragment for each word and add it to the task

# Create a sync map
task.sync_map_file_path_absolute = "lyrics_json/pop/Closer.json"

# Execute the task
ExecuteTask(task).execute()

# Output the alignment result
task.output_sync_map_file()