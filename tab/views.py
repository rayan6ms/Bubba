from django.shortcuts import render
from django.shortcuts import redirect
import json
from datetime import datetime
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response
from tab.models import Message, Taught
from user.models import User


chatbot = ChatBot(
    "Bubba",
    response_selection_method=get_random_response,
    filters=["filters.get_recent_repeated_responses"],
    default_response="I don't know how to answer that",
)

trainer = ChatterBotCorpusTrainer(chatbot)
list_taught = []
list_messages = []
jsonDec = json.decoder.JSONDecoder()
time = []
dict_messages = {}
# Create your views here.
def home(request):
    if request.session.get("user"):
        list_taught.clear()
        user = User.objects.get(id=request.session["user"])

        format = "%l:%M %p"
        time_now = datetime.now().strftime(format)

        picture = User.objects.get(username=user).picture
        new_picture = request.POST.get("new_picture")
        if new_picture is not None:
            picture = int(new_picture)
            User.objects.filter(username=user).update(picture=picture)

        unselected = [i for i in range(1, 10) if i != picture]

        inputs = []
        responses = []
        if request.POST.get("input") != None:
            dict_messages.update(
                {
                    "input": request.POST.get("input"),
                    "response": str(chatbot.get_response(request.POST.get("input"))),
                }
            )

            inputs.append(dict_messages["input"])
            responses.append(dict_messages["response"])

        if inputs:
            for i in range(len(inputs)):
                list_messages.append(inputs[i])
                time.append(time_now)
                list_messages.append(responses[i])
                time.append(time_now)

        iterable = [i for i in range(len(list_messages))]

        model_messages = Message(user_id=user)
        model_messages.messages = json.dumps(list_messages)

        if not Message.objects.filter(user_id=user):
            model_messages.save()
        else:
            Message.objects.filter(user_id=user).update(
                messages=json.dumps(list_messages)
            )

        messages = jsonDec.decode(model_messages.messages)

        return render(
            request,
            "home.html",
            {
                "user": user,
                "time": time,
                "list_messages": list_messages,
                "picture": picture,
                "unselected": unselected,
                "iterable": iterable,
                "messages": messages,
            },
        )
    else:
        list_messages.clear()
        time.clear()
        return redirect("/login/?status=2")


def teach(request):
    if request.session.get("user"):
        list_messages.clear()
        time.clear()
        user = User.objects.get(id=request.session["user"])

        picture = User.objects.get(username=user).picture
        new_picture = request.POST.get("new_picture")
        if new_picture is not None:
            picture = int(new_picture)
            User.objects.filter(username=user).update(picture=picture)

        if not Taught.objects.filter(user_id=user):
            Taught(user_id=user).save()

        model_taught = str(Taught.objects.filter(user_id=user).get())
        model_taught = model_taught.replace("[", "").replace("]", "").replace("\'", "").replace("\"", "").replace(",", "")
        
        taught = []
        taught = model_taught.split(" ")
        if taught[0] == "":
            taught.pop(0)

        train = request.POST.get("train")
        trained = request.POST.get("trained")
        exists = ""
        if train and trained != None:
            if train in taught or trained in taught:
                exists = True
            else:
                exists = False

                list_taught.append(train)
                list_taught.append(trained)

                for i in list_taught:
                    if i not in taught:
                        taught.append(i)

                Taught.objects.filter(user_id=user).update(taught=taught)

                trainer = ListTrainer(chatbot)
                trainer.train(taught)

        unselected = [i for i in range(1, 10) if i != picture]

        return render(
            request,
            "teach.html",
            {
                "user": user,
                "picture": picture,
                "unselected": unselected,
                "trained": trained,
                "exists": exists,
            },
        )
    else:
        list_taught.clear()
        return redirect("/login/?status=2")


def about(request):
    if request.session.get("user"):
        list_messages.clear()
        time.clear()
        list_taught.clear()
        user = User.objects.get(id=request.session["user"])

        picture = User.objects.get(username=user).picture
        new_picture = request.POST.get("new_picture")
        if new_picture is not None:
            picture = int(new_picture)
            User.objects.filter(username=user).update(picture=picture)

        unselected = [i for i in range(1, 10) if i != picture]

        return render(
            request,
            "about.html",
            {"user": user, "picture": picture, "unselected": unselected},
        )
    else:
        return redirect("/login/?status=2")


def more(request):
    if request.session.get("user"):
        list_messages.clear()
        time.clear()
        list_taught.clear()
        user = User.objects.get(id=request.session["user"])

        picture = User.objects.get(username=user).picture
        new_picture = request.POST.get("new_picture")
        if new_picture is not None:
            picture = int(new_picture)
            User.objects.filter(username=user).update(picture=picture)

        unselected = [i for i in range(1, 10) if i != picture]

        return render(
            request,
            "more.html",
            {"user": user, "picture": picture, "unselected": unselected},
        )

    else:
        return redirect("/login/?status=2")
