from django.shortcuts import render
from django.shortcuts import redirect
from datetime import datetime
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response
from tab.models import Message, Taught, Time
from user.models import User

# Create chatbot instance and its parameters
chatbot = ChatBot(
    "Bubba",
    response_selection_method=get_random_response,
    filters=["filters.get_recent_repeated_responses"],
    default_response="I don't have an answer, try to teach me in <a class=teach-link href=/teach>Teach</a>",
)

# Create global variables
trainer = ChatterBotCorpusTrainer(chatbot)
list_taught = []
list_messages = []
list_time = []
dict_messages = {}


def home(request):
    if request.session.get("user"):
        user = User.objects.get(id=request.session["user"])
        list_taught.clear()

        # Get the current UTC time
        format = "%l:%M %P"
        time_now = datetime.now().strftime(format)

        # Get the current selected picture (default=1) and update if requested
        picture = User.objects.get(username=user).picture
        new_picture = request.POST.get("new_picture")
        if new_picture is not None:
            picture = int(new_picture)
            User.objects.filter(username=user).update(picture=picture)

        unselected = [i for i in range(1, 10) if i != picture]

        inputs = []
        responses = []

        # Get a chat input from the user and an answer for it
        if request.POST.get("input") != None:
            dict_messages.update(
                {
                    "input": request.POST.get("input")
                    .replace(",", "&comma;")
                    .replace("'", "&apos;"),
                    "response": str(chatbot.get_response(request.POST.get("input")))
                    .replace(",", "&comma;")
                    .replace("'", "&apos;"),
                }
            )

            inputs.append(dict_messages["input"])
            responses.append(dict_messages["response"])

        # Create a database for the user list of time if not existing
        if not Time.objects.filter(user_id=user):
            Time(user_id=user).save()

        # Get the list of messages from the database as str and transform into a list again
        model_time = str(Time.objects.filter(user_id=user).get())

        model_time = (
            model_time.replace("[", "")
            .replace("]", "")
            .replace("'", "")
            .replace('"', "")
        )

        time = model_time.split(",")

        # Append the inputs and the answers into list_messages, as well as the the current time for each
        if inputs:
            for i in range(len(inputs)):
                list_messages.append(inputs[i])
                time.append(time_now)
                list_messages.append(responses[i])
                time.append(time_now)

        # Create a database for the user list of messages if not existing
        if not Message.objects.filter(user_id=user):
            Message(user_id=user).save()

        # Get the list of messages from the database as str and transform into a list again
        model_messages = str(Message.objects.filter(user_id=user).get())

        model_messages = (
            model_messages.replace("[", "")
            .replace("]", "")
            .replace("'", "")
            .replace('"', "")
        )

        messages = model_messages.split(",")

        # Gather the inputs and responses to the database list
        for i in list_messages:
            messages.append(i)
        list_messages.clear()

        if messages[0] == "":
            messages.pop(0)

        # Update database messages list
        Message.objects.filter(user_id=user).update(messages=messages)

        # Transform the updated database list into a list again for display
        messages = str(Message.objects.filter(user_id=user).get())

        messages = (
            messages.replace("[", "").replace("]", "").replace("'", "").replace('"', "")
        )

        messages = messages.split(",")

        if time[0] == "":
            time.pop(0)

        # Update database time list
        Time.objects.filter(user_id=user).update(time=time)

        # Transform the updated database list into a list again for display
        time = str(Time.objects.filter(user_id=user).get())

        time = time.replace("[", "").replace("]", "").replace("'", "").replace('"', "")

        time = time.split(",")

        if len(messages) > 1:
            iterable = [i for i in range(len(messages))]
        else:
            iterable = []
        
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
        return redirect("/login/?status=2")


def teach(request):
    if request.session.get("user"):
        user = User.objects.get(id=request.session["user"])
        list_messages.clear()
        Message.objects.filter(user_id=user).update(messages="")
        Time.objects.filter(user_id=user).update(time="")

        picture = User.objects.get(username=user).picture
        new_picture = request.POST.get("new_picture")
        if new_picture is not None:
            picture = int(new_picture)
            User.objects.filter(username=user).update(picture=picture)

        # Create a list on the database for the user's taught list
        if not Taught.objects.filter(user_id=user):
            Taught(user_id=user).save()

        model_taught = str(Taught.objects.filter(user_id=user).get())
        model_taught = (
            model_taught.replace("[", "")
            .replace("]", "")
            .replace("'", "")
            .replace('"', "")
        )

        taught = []
        taught = model_taught.split(",")
        if taught[0] == "":
            taught.pop(0)

        train = request.POST.get("train")
        trained = request.POST.get("trained")

        exists = ""

        # Check if current input is already in the database
        if train and trained != None:
            if (train in taught) or (trained in taught):
                exists = True
            else:
                exists = False

                list_taught.append(train.replace(",", "&comma;").replace("'", "&apos;"))
                list_taught.append(
                    trained.replace(",", "&comma;").replace("'", "&apos;")
                )

                # Update the database list and train the bot with the taught list
                for i in list_taught:
                    if i not in taught:
                        taught.append(i)

                list_taught.clear()

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
        user = User.objects.get(id=request.session["user"])
        list_messages.clear()
        list_taught.clear()
        Message.objects.filter(user_id=user).update(messages="")
        Time.objects.filter(user_id=user).update(time="")

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
        list_messages.clear()
        list_taught.clear()
        Message.objects.filter(user_id=user).update(messages="")
        Time.objects.filter(user_id=user).update(time="")

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
