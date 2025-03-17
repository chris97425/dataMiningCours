def obtenir_appreciation(note):
    if note >= 18:
        return "Excellent ! 🌟"
    elif note >= 16:
        return "Très bien ! 😊"
    elif note >= 14:
        return "Bien 👍"
    elif note >= 12:
        return "Assez bien 🙂"
    elif note >= 10:
        return "Passable 😐"
    else:
        return "Insuffisant 😕"
