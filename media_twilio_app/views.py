from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import requests
from twilio.twiml.messaging_response import MessagingResponse
from django.shortcuts import render
from .models import Image
from django.core.files.base import ContentFile


@csrf_exempt
def message(request):
    user = request.POST.get('From')
    message = request.POST.get('Body')
    media_url = request.POST.get('MediaUrl0')
    print(f'{user} sent {message}')
    print(request.POST)

    response = MessagingResponse()
    if media_url:
        r = requests.get(media_url)
        content_type = r.headers['Content-Type']
        username = user.split(':')[1]  # remove the whatsapp: prefix from the number
        if content_type == 'image/jpeg':
            filename = f'uploads/{username}/{message}.jpg'
        elif content_type == 'image/png':
            filename = f'uploads/{username}/{message}.png'
        elif content_type == 'image/gif':
            filename = f'uploads/{username}/{message}.gif'
        else:
            filename = None
        if filename:
            img = Image()
            img.image.save(name=filename, content=ContentFile(r.content), save=True)
            # if not os.path.exists(f'uploads/{username}'):
            #     os.mkdir(f'uploads/{username}')
            # with open(filename, 'wb') as f:
            #     f.write(r.content)

            print("IMAGE SAVED")
            response.message('Thank you! Your image was received.')
        else:
            response.message('The file that you submitted is not a supported image type.')
    else:
        response.message('Please send an image!')

    return HttpResponse('Hello!')


def view_send_image(request):
    image = Image.objects.all()

    context = {
        'image_list': image,
    }
    return render(request, "index.html", context)