from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import FileUploadForm
import os
from django.conf import settings
import joblib
from glob import glob
import pandas as pd
import mne
from tensorflow.keras.models import load_model
import numpy as np

def index(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            eeg_files_path = os.path.join(settings.MEDIA_ROOT, 'eeg_files')
            existing_files = glob(os.path.join(eeg_files_path, '*'))
            for file in existing_files:
                os.remove(file)
                
            fdt_file = form.cleaned_data['fifFile']

            with open(os.path.join(settings.MEDIA_ROOT, 'eeg_files', fdt_file.name), 'wb+') as destination:
                for chunk in fdt_file.chunks():
                    destination.write(chunk)
            file_path = glob(r'pictures\eeg_files\*.fif')
            for i in file_path:
                epochs = mne.read_epochs(i, preload=True)
            epochs=epochs.get_data()[:, :40, :]
            loaded_scaler = joblib.load(r'scaler_2.joblib')
            epochs=np.moveaxis(epochs,1,2)
            epochs = loaded_scaler.transform(epochs.reshape(-1, epochs.shape[-1])).reshape(epochs.shape)
            model_path = r"CNN_2.h5"
            loaded_model = load_model(model_path)
            val_predictions = loaded_model.predict(epochs)
            predctions = (val_predictions > 0.5).astype(int) 
            num_ones = np.sum(predctions == 1)

            total_predictions = len(predctions)
            percentage_ones = int((num_ones / total_predictions) * 100)


            return render(request, 'index.html', {'form': form, 'percentage_ones': percentage_ones})  
    else:
        form = FileUploadForm()

    return render(request, 'index.html', {'form': form, 'percentage_ones': None})


def success(request):
    return render(request, 'success.html') 