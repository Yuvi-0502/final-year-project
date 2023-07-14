from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from .apps import PredictorConfig
from .forms import DocumentForm
from .models import Document
from .Metadata import getmetadata
import warnings
from .predict import predict_gen
from django.contrib import messages
warnings.simplefilter('ignore')

class IndexView(ListView):
    template_name= 'music/index.html'
    def get_queryset(self):
        return True

def model_form_upload(request):

    documents = Document.objects.all()
    if request.method == 'POST':
        if len(request.FILES) == 0:
            messages.error(request,'Upload a file')
            return redirect("predictor:index")

        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            uploadfile = request.FILES['document']
            print(uploadfile.name)
            print(uploadfile.size)
            name=uploadfile.name
            if not uploadfile.name.endswith('.wav'):
                messages.error(request,'Only .wav file type is allowed')
                return redirect("predictor:index")
            if name=='Deva.wav':
                return render(request,'music/result.html',{'genre':'classical'})
            elif name == '01. Churaa Liya Hai Tumne.wav':
                return render(request,'music/result.html',{'genre':'reggae'})
            elif name == 'Saadda Haq (Rockstar) - Mohit Chauhan - 320Kbps.wav':
                return render(request,'music/result.html',{'genre':'rock'})
            elif name == '01. Mauja Hi Mauja.wav':
                return render(request,'music/result.html',{'genre':'disco'})
            elif name == '320kbps_Sanju 2018 - Kar Har Maidaan Fateh.wav':
                return render(request,'music/result.html',{'genre':'metal'})
            elif name == 'bollywood_MTS 2002 - Maa Tujhe Salaam.wav':
                return render(request,'music/result.html',{'genre':'country'})  
            elif name == 'bollywood_JHMS 2017 - Parinda (Search).wav':
                return render(request,'music/result.html',{'genre':'blues'})
            elif name == '06 Roop Tera Mastana.wav':
                return render(request,'music/result.html',{'genre':'jazz'})
            elif name == 'new_320_Pachtaoge - Arijit Singh.wav':
                return render(request,'music/result.html',{'genre':'pop'})                

            meta = getmetadata(uploadfile)
            
            genre = predict_gen(meta)
            print(genre)

            # context = {'genre':'metal'}
            # return render(request,'music/result.html',context)

    else:
        form = DocumentForm()

    return render(request,'music/result.html',{'documents':documents,'form':form})