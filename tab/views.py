from django.shortcuts import render
from django.shortcuts import redirect
from datetime import datetime
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response
from user.models import User


chatbot = ChatBot(
    "Bubba",
    response_selection_method=get_random_response,
    filters=["filters.get_recent_repeated_responses"],
    default_response="I have no idea how to respond to that",
)

trainer = ChatterBotCorpusTrainer(chatbot)
taught = []
messages = []
time = []
dict_messages = {}
# Create your views here.
def home(request):
    if request.session.get("user"):
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
                    "response": chatbot.get_response(request.POST.get("input")),
                }
            )

            inputs.append(dict_messages["input"])
            responses.append(dict_messages["response"])

        if inputs:
            for i in range(len(inputs)):
                messages.append(inputs[i])
                time.append(time_now)
                messages.append(responses[i])
                time.append(time_now)

        iterable = [i for i in range(len(messages))]
        trainer.train(
            "tab/data/facts.yml",
            "tab/data/farewell.yml",
            "tab/data/greetings.yml",
            "tab/data/jokes.yml",
            "tab/data/sounds.yml",
            "tab/data/chitchat.yml",
        )
        return render(
            request,
            "home.html",
            {
                "user": user,
                "time": time,
                "messages": messages,
                "picture": picture,
                "unselected": unselected,
                "iterable": iterable,
            },
        )
    else:
        return redirect("/login/?status=2")


def teach(request):
    if request.session.get("user"):
        user = User.objects.get(id=request.session["user"])
        messages.clear()
        time.clear()

        picture = User.objects.get(username=user).picture
        new_picture = request.POST.get("new_picture")
        if new_picture is not None:
            picture = int(new_picture)
            User.objects.filter(username=user).update(picture=picture)

        train = request.POST.get("train")
        trained = request.POST.get("trained")
        exists = ""
        if train and trained != None:
            if (train or trained) in taught:
                exists = True
            else:
                taught.append(train)
                taught.append(trained)
                trainer = ListTrainer(chatbot)
                trainer.train(taught)
                exists = False

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
        return redirect("/login/?status=2")


def about(request):
    if request.session.get("user"):
        user = User.objects.get(id=request.session["user"])
        messages.clear()
        time.clear()

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
        user = User.objects.get(id=request.session["user"])
        messages.clear()
        time.clear()

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
