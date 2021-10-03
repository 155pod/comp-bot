import random

random.seed()

def get_enqueue_response():
    return random.choice([
        "Siiick!",
        ":sweat_drops:",
        ":lfg:",
        "LetsFuckingGallop!",
        "Let's Go!",
        "Sick.",
        "oh shit.",
        ":avrilpizza:",
        ":kravis:",
        ":saminthedark:",
        ":cigmark:",
        ":avsun:",
        ":podmagic2:"
    ])


if __name__ == "__main__":
    print get_enqueue_response()
