## NullClass Task4

This task is about creating a feature to translate the audio into Hindi. The system will listen the english audio from user and it will convert into Hindi word. If the system does not understand the audio it will ask repeat one more time to make it better. The audio should be in English only. This translation feature should work on only after 6 PM IST timing and before that it should show message like please try after 6 PM IST as well as it should not translate any english which is start with M and O and apart from that it should translate all other word. The model is stored in the folder `english_to_hindi_lstm_model`. The tokenizers are stored in `english_tokenizer.json` and `hindi_tokenizer.json` respectively. 


In order to run the notebook, follow the steps:

1. Create a conda environment

```bash
conda create --name nullclass python=3.9
```
2. Activate the environment

```bash
conda activate nullclass
```
3. Install cudnn plugin
```bash
conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0
```

4. Install tensorflow
```bash
pip install --upgrade pip
# Anything above 2.10 is not supported on the GPU on Windows Native
pip install "tensorflow<2.11" 
```

5. Install necessary libraries for audio and speech input and identification
```bash
pip install pytz SpeechRecognition pyaudio
```

The same environment `nullclass` can be used for running notebooks for other tasks as well. Now run the notebook named `task4.ipynb`.